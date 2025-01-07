from ninja import PatchDict, Router
from django.contrib.auth import get_user_model
from settings.schema import *
from typing import *
from employee.models import *
from settings.models import *
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

setting_api = Router(tags=['settings'])
User = get_user_model()

@setting_api.post('/general',response={201: GeneralSchema, 400: Message})
async def general_setting(request, data: GeneralSchema):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        _data=data.dict()
        gen=await General.objects.acreate(**_data, organization=user.organization,crtd_by=user)
        await gen.asave()
        return 201, GeneralSchema.from_orm(gen)
    return 400,{"message":"organization doesnot exist"}

@setting_api.put("/general/{id}",response={201: GeneralSchema, 400: Message})
async def update_general(request,data:GeneralSchema):
    user= request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        gen = await General.objects.aget(id=id) 
        for field, value in data.dict(exclude_unset=True).items():
            setattr(gen, field, value)        
        await gen.asave()
        return 200, GeneralSchema.from_orm(gen)
    return 400,{"message":"organization doesnot exist"}

@setting_api.get("/general/{id}",response={201:GeneralSchema,400:Message})
async def get_general(request,data:GeneralSchema):
    user=request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        gen = await General.objects.aget(id=id)
        return 200, GeneralSchema.from_orm(gen)
    return 400,{"message":"organization doesn't exist"}

###########################  DEPARTMENT  ####################################

@setting_api.post("/department",response={201:DepartmentSchema,400:Message})
async def add_department(request,data:DepartmentInputSchema):
    user=request.auth
    if user and await sync_to_async(lambda:user.role == 'admin' and user.organization)():
        _data=data.dict(exclude={"department_head"})
        user_data=await sync_to_async(Employee.objects.get)(user=user)
        department_head = None
        if data.department_head:
            department_head = await sync_to_async(Employee.objects.get)(id=data.department_head)
        dept = await sync_to_async(Department.objects.create)(**_data,department_head=department_head,updated_by=user_data)
        dept.department_head = department_head
        dept.updated_by = user_data
        return 201,DepartmentSchema.from_orm(dept) 
    return 400,{"message":"organization not found"}

@setting_api.get("/department", response={200: Union[List[DepartmentSchema], DepartmentSchema], 400: Message})
async def get_departments(request, id: Optional[int] = None):
    user = request.auth
    if user and await sync_to_async(lambda: user.organization)():
        base_query = Department.objects.select_related('department_head__user','updated_by__user').filter(updated_by__user__organization=user.organization)
        if id is not None:
            department = await sync_to_async(base_query.get)(id=id)
            return 200, DepartmentSchema.from_orm(department)
        else:
            departments = await sync_to_async(list)(base_query)
            return 200, departments
    return 400, {"message": "organization not found"}

@setting_api.put("/department", response={200: DepartmentSchema, 400: Message})
async def update_department(request, id: int, data: DepartmentInputSchema):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        department = await sync_to_async(Department.objects.select_related('department_head__user','updated_by__user').get)(id=id,updated_by__user__organization=user.organization)
        _data = data.dict(exclude={"department_head"})
        for key, value in _data.items():
            setattr(department, key, value)
        if data.department_head:
            department_head = await sync_to_async(Employee.objects.get)(id=data.department_head)
            department.department_head = department_head
        user_data = await sync_to_async(Employee.objects.get)(user=user)
        department.updated_by = user_data
        await sync_to_async(department.save)()
        department = await sync_to_async(Department.objects.select_related('department_head__user','updated_by__user').get)(id=department.id)
        return 200, DepartmentSchema.from_orm(department)
    return 400, {"message": "Unauthorized or organization not found"}

@setting_api.delete("/department", response={200: Message, 404: Message, 400: Message})
async def delete_department(request, id: int):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        department = await sync_to_async(Department.objects.get)(id=id,updated_by__user__organization=user.organization)
        await sync_to_async(department.delete)()
        return 200, {"message": "Department deleted successfully"}
    return 400, {"message": "Unauthorized or organization not found"}

#############################  DESIGNATION   #################################

@setting_api.get("/designation", response={200: Union[List[DesignationSchema], DesignationSchema], 404: Message, 400: Message})
async def get_designations(request, id: Optional[int] = None):
    user = request.auth
    if user and await sync_to_async(lambda: user.organization)():
        try:
            base_query = Designation.objects.select_related(
                'updated_by__user'
            ).filter(updated_by__user__organization=user.organization)

            if id is not None:
                designation = await sync_to_async(base_query.get)(id=id)
                return 200, DesignationSchema.from_orm(designation)
            else:
                designations = await sync_to_async(list)(base_query)
                return 200, designations
        except Designation.DoesNotExist:
            return 404, {"message": "Designation not found"}
    return 400, {"message": "organization not found"}

@setting_api.post("/designation", response={201: DesignationSchema, 400: Message})
async def add_designation(request, data: DesignationSchema):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        _data = data.dict(exclude={"updated"})
        user_data = await sync_to_async(Employee.objects.get)(user=user)
        designation = await sync_to_async(Designation.objects.create)(
            **_data,
            updated_by=user_data
        )
        designation = await sync_to_async(Designation.objects.select_related(
            'updated_by__user'
        ).get)(id=designation.id)
        return 201, DesignationSchema.from_orm(designation)
    return 400, {"message": "Unauthorized or organization not found"}

@setting_api.put("/designation", response={200: DesignationSchema, 404: Message, 400: Message})
async def update_designation(request, id: int, data: DesignationSchema):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        designation = await sync_to_async(Designation.objects.select_related(
            'updated_by__user'
        ).get)(
            id=id,
            updated_by__user__organization=user.organization
        )
        _data = data.dict(exclude={"updated"})
        for key, value in _data.items():
            setattr(designation, key, value)
        user_data = await sync_to_async(Employee.objects.get)(user=user)
        designation.updated_by = user_data
        await sync_to_async(designation.save)()
        designation = await sync_to_async(Designation.objects.select_related(
            'updated_by__user'
        ).get)(id=designation.id)
        return 200, DesignationSchema.from_orm(designation)
    return 400, {"message": "Unauthorized or organization not found"}

@setting_api.delete("/designation", response={200: Message, 404: Message, 400: Message})
async def delete_designation(request, id: int):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        designation = await sync_to_async(Designation.objects.get)(
            id=id,
            updated_by__user__organization=user.organization
        )
        await sync_to_async(designation.delete)()
        return 200, {"message": "Designation deleted successfully"}
    return 400, {"message": "Unauthorized or organization not found"}


@setting_api.post("/employee_setting",response={201:EmployeeSchema,400:Message})
async def add_employee_setting(request,data:EmployeeSchema):
    user=request.auth
    if user and await sync_to_async(lambda:user.role == 'admin' and user.organization)():
        _data=data.dict()
        gen=await employee_setting.objects.acreate(**_data, organization=user.organization)
        await gen.asave()
        return 201, EmployeeSchema.from_orm(gen)
    return 400,{"message":"organization doesnot exist"}

@setting_api.get("/employee_setting/{id}",response={201:EmployeeSchema,400:Message})
async def get_employee_setting(request,data:EmployeeSchema):
    user=request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        gen = await employee_setting.objects.aget(id=id)
        return 200, EmployeeSchema.from_orm(gen)
    return 400,{"message":"organization doesn't exist"}

@setting_api.put("/employee_setting",response={201:EmployeeSchema,400:Message})
async def update_employee_setting(request,data:EmployeeSchema):
    user=request.authj
    if user and await sync_to_async(lambda:user.role=='admin' and user.organization)():
        emp = await Employee.objects.aget(id=id) 
        for field, value in data.dict(exclude_unset=True).items():
            setattr(emp, field, value)        
        await emp.asave()
        return 200, EmployeeSchema.from_orm(emp)
    return 400,{"message":"organization doesnot exist"}












