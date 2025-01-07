from ninja import PatchDict, Router
from django.contrib.auth import get_user_model
from .schema import *
from typing import *
from .models import *
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
from ninja.responses import codes_4xx
from ninja_jwt.authentication import AsyncJWTAuth
from asgiref.sync import sync_to_async
from ninja_jwt.tokens import RefreshToken, AccessToken
from ninja_jwt.tokens import RefreshToken
from ninja.errors import HttpError

employee_api = Router(tags=['employee'])
User = get_user_model()

# @user_api.post("/userprofile", auth=None, response={201: TokenSchema, 409: Message})
# async def register(request, data: UserCreation):
#     if not await User.objects.filter(Q(username=data.username) | Q(email=data.email)).aexists():
#         user = await User.objects.acreate(**data.dict())
#         user.set_password(data.password)
#         await user.asave()
#         refresh = RefreshToken.for_user(user)
#         return 201, {'access': str(refresh.access_token), 'refresh': str(refresh)}
#     return 409, {"message": "User already exists"}

@employee_api.post("/create_employee", response={201: EmployeeCreation, 400: Message})
async def create_employee(request, data: EmployeeCreation):
    user = request.user
    if user.role=='admin' and user.organization:
        if not await UserProfile.objects.filter(Q(username=data.username) | Q(email=data.email), organization=user.organization).aexists():
            employee = await UserProfile.objects.acreate(**data.dict(exclude={"password"}), organization=user.organization)
            employee.set_password(data.password)
            await employee.asave()
            return 201, EmployeeCreation.from_orm(employee)
        raise HttpError(400, "Employee with given username or email already exists in this organization.")
    raise HttpError(400, "You do not have permission to create employees in this organization.")

@employee_api.get("/get_employee/{employee_id}", response={200: EmployeeCreation, 404: Message})
async def get_employee(request, employee_id: int):
    user = request.user
    if user.role=='admin' and user.organization:
        try:
            employee = await UserProfile.objects.aget(id=employee_id, organization=user.organization)
            return 200, EmployeeCreation.from_orm(employee)
        except UserProfile.DoesNotExist:
            raise HttpError(404, "Employee not found in this organization.")
    raise HttpError(400, "You do not have permission to view employee details in this organization.")

@user_api.put("/update_employee/{employee_id}", response={200: EmployeeCreation, 404: Message})
async def update_employee(request, employee_id: int, data: EmployeeCreation):
    user = request.user
    if user.role=='admin' and user.organization:
        try:
            employee = await UserProfile.objects.aget(id=employee_id, organization=user.organization)
            for field, value in data.dict(exclude_unset=True).items():
                if field != "password":
                    setattr(employee, field, value)
            if data.password:
                employee.set_password(data.password)
            await employee.asave()
            return 200, EmployeeCreation.from_orm(employee)
        except UserProfile.DoesNotExist:
            raise HttpError(404, "Employee not found in this organization.")
    raise HttpError(400, "You do not have permission to update employee details in this organization.")
