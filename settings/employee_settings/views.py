from ninja import PatchDict, Router
from django.contrib.auth import get_user_model
from settings.employee_settings.schema import *
from typing import *
from settings.employee_settings.models import *
# from employee.basic_details.models import *
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

# Employee Profile Settings endpoints
# @employee_setting_api.post("/employee-profile-settings", response={201: EmployeeProfileSettingsSchema, 400: Message})
# async def add_employee_profile_settings(request, data: EmployeeProfileSettingsInputSchema):
#     user = request.auth
#     if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
#         try:
#             settings = await sync_to_async(EmployeeProfileSettings.objects.create)(**data.dict(),updated_by=user )
#             return 201, EmployeeProfileSettingsSchema.from_orm(settings)
#         except Exception as e:
#             return 400, {"message": str(e)}
#     return 400, {"message": "Unauthorized or organization not found"}
@employee_setting_api.post("/employee-profile-settings", response={201: EmployeeProfileSettingsSchema, 400: Message})
async def add_employee_profile_settings(request, data: EmployeeProfileSettingsInputSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 400, {"message": "Unauthorized or organization not found"}

    org = await sync_to_async(lambda: user.organization)()

    # Prevent duplicate
    exists = await sync_to_async(EmployeeProfileSettings.objects.filter(organization=org).exists)()
    if exists:
        return 400, {"message": "Settings already exist for this organization"}

    try:
        settings = await sync_to_async(EmployeeProfileSettings.objects.create)(
            **data.dict(), organization=org, updated_by=user
        )
        org_detail = organizationDetail.from_orm(settings.organization)
        response_data = EmployeeProfileSettingsSchema.from_orm(settings).dict()
        response_data["organization"] = org_detail

        return 201, response_data
        # return 201, EmployeeProfileSettingsSchema.from_orm(settings)
    except Exception as e:
        return 400, {"message": str(e)}
@employee_setting_api.get("/employee-profile-settings", response={200: EmployeeProfileSettingsSchema, 404: Message, 400: Message})
async def get_employee_profile_settings(request):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.organization)():
        return 400, {"message": "Unauthorized or organization not found"}

    try:
        org = await sync_to_async(lambda: user.organization)()
        settings = await sync_to_async(EmployeeProfileSettings.objects.select_related('organization', 'updated_by').get)(organization=org)

        organization_id = await sync_to_async(lambda: settings.organization.id)()
        organization_name = await sync_to_async(lambda: settings.organization.organization_name)()

        updated_by_id = await sync_to_async(lambda: settings.updated_by.id if settings.updated_by else None)()
        updated_by_name = await sync_to_async(lambda: settings.updated_by.name if settings.updated_by else None)() if updated_by_id else None

        data = {
            "organization": {
                "id": organization_id,
                "name": organization_name
            },
            "manage_employee_profile": settings.manage_employee_profile,
            "unique_fields": settings.unique_fields,
            "employee_skills": settings.employee_skills,
            "custom_skills": settings.custom_skills,
            "approve_required": settings.approve_required,
            "employees_addable": settings.employees_addable,
            "filter_search": settings.filter_search,
            "generally_showable_fields": settings.generally_showable_fields,
            "officially_showable_fields": settings.officially_showable_fields,
            "contacts_showable_fields": settings.contacts_showable_fields,
            "other_showable_fields": settings.other_showable_fields,
            "mandatory_inputable_fields": settings.mandatory_inputable_fields,
            "updated_by": {
                "id": updated_by_id,
                "name": updated_by_name
            } if updated_by_id else None
        }

        return 200, data

    except EmployeeProfileSettings.DoesNotExist:
        return 404, {"message": "Settings not found"}
    except Exception as e:
        return 400, {"message": str(e)}

@employee_setting_api.put("/employee-profile-settings", response={200: EmployeeProfileSettingsSchema, 400: Message})
async def update_employee_profile_settings(request, data: EmployeeProfileSettingsInputSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 400, {"message": "Unauthorized or organization not found"}

    try:
        org = await sync_to_async(lambda: user.organization)()

        # Check if data exists
        existing = await sync_to_async(EmployeeProfileSettings.objects.filter(organization=org).first)()

        if existing:
            for key, value in data.dict().items():
                setattr(existing, key, value)
            existing.updated_by = user
            await sync_to_async(existing.save)()

            response_data = {
                "organization": {"id": org.id, "name": org.organization_name},
                "updated_by": {
                    "id": user.id,
                    "name": user.name
                },
                **{key: getattr(existing, key) for key in data.dict().keys()}
            }

            return 200, response_data

        # Else create new
        new_settings = await sync_to_async(EmployeeProfileSettings.objects.create)(
            **data.dict(), organization=org, updated_by=user
        )

        response_data = {
            "organization": {"id": org.id, "name": org.organization_name},
            "updated_by": {
                "id": user.id,
                "name": user.name  
            },
            **{key: getattr(new_settings, key) for key in data.dict().keys()}
        }

        return 200, response_data

    except Exception as e:
        return 400, {"message": str(e)}



# @employee_setting_api.get("/employee-profile-settings", response={200: Union[List[EmployeeProfileSettingsSchema], EmployeeProfileSettingsSchema], 400: Message})
# async def get_employee_profile_settings(request, id: Optional[int] = None):
#     user = request.auth
#     if user and await sync_to_async(lambda: user.organization)():
#         try:
#             base_query = EmployeeProfileSettings.objects.select_related('updated_by').filter(updated_by=user)
#             if id is not None:
#                 settings = await sync_to_async(base_query.get)(id=id)
#                 return 200, EmployeeProfileSettingsSchema.from_orm(settings)
#             settings_list = await sync_to_async(list)(base_query)
#             return 200, [EmployeeProfileSettingsSchema.from_orm(setting) for setting in settings_list]
#         except Exception as e:
#             return 400, {"message": str(e)}
#     return 400, {"message": "Unauthorized or organization not found"}

# @employee_setting_api.put("/employee-profile-settings", response={200: EmployeeProfileSettingsSchema, 400: Message})
# async def update_employee_profile_settings(request, id: int, data: EmployeeProfileSettingsInputSchema):
#     user = request.auth
#     if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
#         try:
#             settings = await sync_to_async(EmployeeProfileSettings.objects.get)(id=id, updated_by=user)
#             for key, value in data.dict().items():     
#                 setattr(settings, key, value)
#             settings.updated_by = user
#             await sync_to_async(settings.save)()
#             return 200, EmployeeProfileSettingsSchema.from_orm(settings)
#         except Exception as e:
#             return 400, {"message": str(e)}
#     return 400, {"message": "Unauthorized or organization not found"}

# Document Settings endpoints
@employee_setting_api.post("/document-settings", response={201: DocumentSettingSchema, 400: Message})
async def add_document_settings(request, data: DocumentSettingInputSchema):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        try:
            document = await sync_to_async(DocumentSetting.objects.create)(
                **data.dict(),
                updated_by=user
            )
            return 201, DocumentSettingSchema.from_orm(document)
        except Exception as e:
            return 400, {"message": str(e)}
    return 400, {"message": "Unauthorized or organization not found"}

@employee_setting_api.get("/document-settings", response={200: Union[List[DocumentSettingSchema], DocumentSettingSchema], 400: Message})
async def get_document_settings(request, id: Optional[int] = None):
    user = request.auth
    if user and await sync_to_async(lambda: user.organization)():
        try:
            base_query = DocumentSetting.objects.select_related('updated_by').filter(updated_by=user)
            if id is not None:
                document = await sync_to_async(base_query.get)(id=id)
                return 200, DocumentSettingSchema.from_orm(document)
            documents = await sync_to_async(list)(base_query)
            return 200, [DocumentSettingSchema.from_orm(doc) for doc in documents]
        except Exception as e:
            return 400, {"message": str(e)}
    return 400, {"message": "Unauthorized or organization not found"}

@employee_setting_api.put("/document-settings", response={200: DocumentSettingSchema, 400: Message})
async def update_document_settings(request, id: int, data: DocumentSettingInputSchema):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        try:
            document = await sync_to_async(DocumentSetting.objects.get)(id=id, updated_by=user)
            for key, value in data.dict().items():
                setattr(document, key, value)
            document.updated_by = user
            await sync_to_async(document.save)()
            return 200, DocumentSettingSchema.from_orm(document)
        except Exception as e:
            return 400, {"message": str(e)}
    return 400, {"message": "Unauthorized or organization not found"}