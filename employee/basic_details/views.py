from ninja import PatchDict, Router
from django.contrib.auth import get_user_model
from employee.basic_details.schema import *
from typing import *
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

employee_basic_api = Router(tags=['employee_basic'])
User = get_user_model()

@employee_basic_api.post("/employee", response={201: EmployeeSchema, 400: Message})
async def create_employee(request, data: EmployeeInputSchema):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        try:
            employee_data = data.dict()
            user_obj = await sync_to_async(User.objects.create)(name=data.name,username=data.username,email=data.email,phone=data.phone)
            reporting_manager = await sync_to_async(User.objects.get)(id=data.reporting_manager_id) if data.reporting_manager_id else None
            business_unit = await sync_to_async(BusinessUnitSettings.objects.get)(id=data.business_unit_id) if data.business_unit_id else None
            department = await sync_to_async(DepartmentSettings.objects.get)(id=data.department_id) if data.department_id else None
            designation = await sync_to_async(DesignationSettings.objects.get)(id=data.designation_id) if data.designation_id else None
            for field in ['user_id', 'reporting_manager_id', 'business_unit_id', 'department_id', 'designation_id']:
                employee_data.pop(field, None)
            employee = await sync_to_async(Employee.objects.create)(user=user_obj,created_by=user,reporting_manager=reporting_manager,business_unit=business_unit,department=department,designation=designation,**employee_data)
            return 201, EmployeeSchema.from_orm(employee)
        except Exception as e:
            return 400, {"message": str(e)}
    return 400, {"message": "Unauthorized access"}

@employee_basic_api.get("/employee", response={200: List[EmployeeSchema], 404: Message})
async def get_employees(request, id: Optional[int] = None):
    user = request.auth 
    if user and await sync_to_async(lambda: user.organization)():
        try:
            base_query = Employee.objects.select_related('user','created_by','reporting_manager','business_unit','department','designation').filter(created_by__organization=user.organization)
            if id:
                employee = await sync_to_async(base_query.get)(id=id)
                return 200, EmployeeSchema.from_orm(employee)
            employees = await sync_to_async(list)(base_query)
            return 200, [EmployeeSchema.from_orm(emp) for emp in employees]
        except Employee.DoesNotExist:
            return 404, {"message": "Employee not found"}
        except Exception as e:
            return 400, {"message": str(e)}
    return 400, {"message": "Unauthorized access"}

@employee_basic_api.put("/employee/{id}", response={200: EmployeeSchema, 404: Message})
async def update_employee(request, id: int, data: EmployeeInputSchema):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        try:
            employee = await sync_to_async(Employee.objects.select_related('user','created_by','reporting_manager','business_unit','department','designation').get)(id=id, created_by__organization=user.organization)
            # Update related fields if provided
            if data.user_id:
                employee.user = await sync_to_async(User.objects.get)(id=data.user_id)
            if data.reporting_manager_id:
                employee.reporting_manager = await sync_to_async(User.objects.get)(id=data.reporting_manager_id)
            if data.business_unit_id:
                employee.business_unit = await sync_to_async(BusinessUnitSettings.objects.get)(id=data.business_unit_id)
            if data.department_id:
                employee.department = await sync_to_async(DepartmentSettings.objects.get)(id=data.department_id)
            if data.designation_id:
                employee.designation = await sync_to_async(DesignationSettings.objects.get)(id=data.designation_id)
            # Update other fields
            update_data = data.dict(exclude={'user_id', 'reporting_manager_id', 'business_unit_id', 'department_id', 'designation_id'})
            for key, value in update_data.items():
                if value is not None:
                    setattr(employee, key, value)
            await sync_to_async(employee.save)()
            return 200, EmployeeSchema.from_orm(employee)
        except Employee.DoesNotExist:
            return 404, {"message": "Employee not found"}
        except Exception as e:
            return 400, {"message": str(e)}
    return 400, {"message": "Unauthorized access"}

@employee_basic_api.delete("/employee/{id}", response={200: Message, 404: Message})
async def delete_employee(request, id: int):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        try:
            employee = await sync_to_async(Employee.objects.get)(id=id, created_by__organization=user.organization)
            await sync_to_async(employee.delete)()
            return 200, {"message": "Employee deleted successfully"}
        except Employee.DoesNotExist:
            return 404, {"message": "Employee not found"}
        except Exception as e:
            return 400, {"message": str(e)}
    return 400, {"message": "Unauthorized access"}

# Profile image upload endpoint
@employee_basic_api.post("/employee/{id}/upload-profile", response={200: Message, 404: Message})
async def upload_profile_image(request, id: int):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        try:
            employee = await sync_to_async(Employee.objects.get)(id=id, created_by__organization=user.organization)
            data = await request.form()
            file = data.get('profile')
            if file:
                employee.profile = file
                await sync_to_async(employee.save)()
                return 200, {"message": "Profile image uploaded successfully"}
            return 400, {"message": "No profile image provided"}
        except Employee.DoesNotExist:
            return 404, {"message": "Employee not found"}
        except Exception as e:
            return 400, {"message": str(e)}
    return 400, {"message": "Unauthorized access"} 