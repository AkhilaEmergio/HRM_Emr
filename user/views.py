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
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from employee.basic_details.models import Employee

user_api = Router(tags=['user'])
User = get_user_model()

@user_api.post("/create_organization_and_user", response={201: Message, 403: Message, 409:Message})
def create_organization_and_user(request, data: OrganizationSchema):
    created_by = request.auth
    if User.objects.filter(username=data.username).exists() or User.objects.filter(email=data.email).exists():
        org = Organization.objects.create(name=data.organisation_name, **data.dict())
        user = User.objects.create(**data.dict())
        user.set_password(data.password)
        user.save()
        employee = Employee.objects.create(user=user, created_by=created_by)
        return 201, {"message": "Organization created successfully."}
    return 403, {"message": "Organisation with same username/ Email already exists"}

@user_api.post("/login", auth=None, response={200: TokenSchema, 401: Message})
async def login(request, data: LoginSchema):
    user = await sync_to_async(authenticate)(username=data.username, password=data.password)
    if not user:
        return 401, {"message": "Invalid credentials"}
    # Fetch related fields asynchronously
    organization = await sync_to_async(lambda: user.organization)()
    role = await sync_to_async(lambda:user.role)()
    refresh = RefreshToken.for_user(user)
    return 200, { 
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "role": role,
        "organization": str(organization.id) if user.role =='superadmin' else ''
    }

@user_api.post("/refresh", auth=None, response={200: TokenSchema, 401: Message})
def refresh_token(request, token_data: TokenRefreshSchema):
    try:
        refresh = RefreshToken(token_data.refresh)   
        return 200, {'access': str(refresh.access_token),'refresh': str(refresh)}
    except Exception: 
        return 401, {"message": "Invalid refresh token"}

@user_api.get("/", response={200: UserData, 401: Message})
async def user(request):
    user = request.auth
    return 200, user