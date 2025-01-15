from ninja import PatchDict, Router
from django.contrib.auth import get_user_model
from settings.general_settings.schema import *
from typing import *
from user.models import *
from employee.basic_details.models import *
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


########################   EMPLOYEEE  ##############################
employee_setting_api = Router(tags=['employee_settings'])
user=get_user_model()

@employee_setting_api.post("/employee_setting",response={201:EmployeeSchema,400:Message})
async def add_employee_setting(request,data:EmployeeSchema):
    user=request.auth
    if user and await sync_to_async(lambda:user.role == 'admin' and user.organization)():
        _data=data.dict()
        gen=await employee_setting.objects.acreate(**_data, organization=user.organization)
        await gen.asave()
        return 201, EmployeeSchema.from_orm(gen)
    return 400,{"message":"organization doesnot exist"}

@employee_setting_api.get("/employee_setting/{id}",response={201:EmployeeSchema,400:Message})
async def get_employee_setting(request,data:EmployeeSchema):
    user=request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        gen = await employee_setting.objects.aget(id=id)
        return 200, EmployeeSchema.from_orm(gen)
    return 400,{"message":"organization doesn't exist"}

@employee_setting_api.put("/employee_setting",response={201:EmployeeSchema,400:Message})
async def update_employee_setting(request,data:EmployeeSchema):
    user=request.authj
    if user and await sync_to_async(lambda:user.role=='admin' and user.organization)():
        emp = await Employee.objects.aget(id=id) 
        for field, value in data.dict(exclude_unset=True).items():
            setattr(emp, field, value)        
        await emp.asave()
        return 200, EmployeeSchema.from_orm(emp)
    return 400,{"message":"organization doesnot exist"}












