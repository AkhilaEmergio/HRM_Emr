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
            # Create a User object with user-specific fields
            user_obj = await sync_to_async(User.objects.create)(name=data.name, username=data.username, email=data.email, phone=data.phone,password=data.password)
            user_obj.set_password(data.password)  # Set the password here
            await sync_to_async(user_obj.save)()

            # Create the Employee object
            reporting_manager = await sync_to_async(User.objects.get)(id=data.reporting_manager_id) if data.reporting_manager_id else None
            business_unit = await sync_to_async(BusinessUnitSettings.objects.get)(id=data.business_unit_id) if data.business_unit_id else None
            department = await sync_to_async(DepartmentSettings.objects.get)(id=data.department_id) if data.department_id else None
            designation = await sync_to_async(DesignationSettings.objects.get)(id=data.designation_id) if data.designation_id else None

            # Remove user-related fields from the employee data
            employee_data = data.dict()
            for field in ['username', 'email', 'password', 'name', 'phone', 'role', 'reporting_manager_id', 'business_unit_id', 'department_id', 'designation_id']:
                employee_data.pop(field, None)

            # Create an Employee object using the remaining fields
            employee = await sync_to_async(Employee.objects.create)(user=user_obj, created_by=user, reporting_manager=reporting_manager, business_unit=business_unit, department=department, designation=designation, **employee_data)

            return 201, EmployeeSchema.from_orm(employee)

        except Exception as e:
            return 400, {"message": str(e)}

    return 400, {"message": "Unauthorized access"}


@employee_basic_api.get("/employee", response={200: Union[List[EmployeeSchema], EmployeeSchema], 400: Message})
async def get_employees(request, id: Optional[int] = None):
    user = request.auth
    if user and await sync_to_async(lambda: user.organization)():
        try:
            base_query = Employee.objects.select_related(
                'user',
                'created_by',
                'reporting_manager',
                'business_unit',
                'business_unit__unit_head',
                'business_unit__updated_by',
                'department',
                'department__department_head',
                'department__updated_by',
                'designation',
                'designation__updated_by'
            ).filter(created_by__organization=user.organization)

            if id is not None:
                employee = await sync_to_async(base_query.get)(id=id)
                return 200, EmployeeSchema.from_orm(employee)

            employees = await sync_to_async(list)(base_query)
            return 200, [EmployeeSchema.from_orm(emp) for emp in employees]

        except Exception as e:
            return 400, {"message": str(e)}
    return 400, {"message": "Unauthorized or organization not found"}

@employee_basic_api.put("/employee/{id}", response={200: EmployeeSchema, 400: Message, 404: Message})
async def update_employee(request, id: int, payload: EmployeeUpdateSchema):
    user = request.auth
    if user and await sync_to_async(lambda: user.organization)():
        try:
            base_query = Employee.objects.select_related(
                'user',
                'created_by',
                'reporting_manager',
                'business_unit',
                'business_unit__unit_head',
                'business_unit__updated_by',
                'department',
                'department__department_head',
                'department__updated_by',
                'designation',
                'designation__updated_by'
            ).filter(created_by__organization=user.organization)

            # Get existing employee
            employee = await sync_to_async(base_query.get)(id=id)
            
            # Update fields
            update_data = payload.dict(exclude_unset=True)
            
            # Update basic fields
            basic_fields = [
                'employee_code', 'profile', 'date_of_joining',
                'employment_type', 'service_status', 'workmode',
                'probation', 'extension', 'notice_period',
                'enrollment_no', 'trigger_onboarding', 'send_mail',
                'weekly_offs', 'permissions'
            ]
            
            for field in basic_fields:
                if field in update_data:
                    await sync_to_async(setattr)(employee, field, update_data.get(field))
            
            # Update related fields if provided
            if 'reporting_manager' in update_data:
                reporting_manager_data = update_data.get('reporting_manager')
                if reporting_manager_data:
                    reporting_manager = await sync_to_async(User.objects.get)(
                        email=reporting_manager_data.get('email')
                    )
                    employee.reporting_manager = reporting_manager
            
            if 'business_unit' in update_data:
                business_unit_data = update_data.get('business_unit')
                if business_unit_data:
                    business_unit = await sync_to_async(Business_unit.objects.get)(
                        title=business_unit_data.get('title')
                    )
                    employee.business_unit = business_unit
            
            if 'department' in update_data:
                department_data = update_data.get('department')
                if department_data:
                    department = await sync_to_async(Department.objects.get)(
                        title=department_data.get('title')
                    )
                    employee.department = department
            
            if 'designation' in update_data:
                designation_data = update_data.get('designation')
                if designation_data:
                    designation = await sync_to_async(Designation.objects.get)(
                        title=designation_data.get('title')
                    )
                    employee.designation = designation

            # Save the updated employee
            await sync_to_async(employee.save)()
            
            # Refresh the employee instance to get updated data
            updated_employee = await sync_to_async(base_query.get)(id=id)
            
            return 200, EmployeeSchema.from_orm(updated_employee)

        except Employee.DoesNotExist:
            return 404, {"message": "Employee not found"}
        except User.DoesNotExist:
            return 400, {"message": "Invalid user reference"}
        except Business_unit.DoesNotExist:
            return 400, {"message": "Invalid business unit reference"}
        except Department.DoesNotExist:
            return 400, {"message": "Invalid department reference"}
        except Designation.DoesNotExist:
            return 400, {"message": "Invalid designation reference"}
        except Exception as e:
            return 400, {"message": str(e)}
            
    return 400, {"message": "Unauthorized or organization not found"}

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

@employee_basic_api.post("/personal_detail", response={201: PersonalDetailSchema, 400: dict})
async def create_personal_detail(request, data: PersonalDetailSchema):
    user = request.auth
    try:
        employee = await sync_to_async(Employee.objects.get)(user=user)
        personal_detail = await sync_to_async(PersonalDetail.objects.create)(
            employee=employee,
            **data.dict()
        )
        return 201, PersonalDetailSchema.from_orm(personal_detail)
    except Employee.DoesNotExist:
        return 400, {"message": "Employee profile not found"}
    except Exception as e:
        return 400, {"message": str(e)}

@employee_basic_api.get("/personal_detail", response={200: PersonalDetailSchema, 404: dict})
async def get_personal_detail(request):
    user = request.auth
    try:
        employee = await sync_to_async(Employee.objects.get)(user=user)
        personal_detail = await sync_to_async(PersonalDetail.objects.get)(employee=employee)
        return 200, PersonalDetailSchema.from_orm(personal_detail)
    except PersonalDetail.DoesNotExist:
        return 404, {"message": "Personal details not found"}
    except Employee.DoesNotExist:
        return 404, {"message": "Employee profile not found"}

@employee_basic_api.put("/personal_detail", response={200: PersonalDetailSchema, 400: dict})
async def update_personal_detail(request, data: PersonalDetailSchema):
    user = request.auth
    try:
        employee = await sync_to_async(Employee.objects.get)(user=user)
        personal_detail = await sync_to_async(PersonalDetail.objects.get)(employee=employee)

        for attr, value in data.dict(exclude_unset=True).items():
            setattr(personal_detail, attr, value)
        
        await sync_to_async(personal_detail.save)()
        return 200, PersonalDetailSchema.from_orm(personal_detail)
    except PersonalDetail.DoesNotExist:
        return 400, {"message": "Personal details not found"}
    except Employee.DoesNotExist:
        return 400, {"message": "Employee profile not found"}
