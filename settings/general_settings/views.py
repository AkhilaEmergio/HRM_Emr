from ninja import PatchDict, Router
from django.contrib.auth import get_user_model
from settings.general_settings.schema import *
from typing import *
from employee.basic_details.models import *
from settings.general_settings.models import *
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
from user.models import UserProfile

general_setting_api = Router(tags=['general_settings'])
User = get_user_model()

@general_setting_api.put("/general",response={200: GeneralSchema, 400: Message})
async def update_general(request,data:GeneralSchema):
    user= request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        gen = await Organization.objects.aget(id=user.organization.id) 
        for field, value in data.dict(exclude_unset=True).items():
            setattr(gen, field, value)        
        await gen.asave()
        return 200, GeneralSchema.from_orm(gen)
    return 400,{"message":"organization doesnot exist"}

@general_setting_api.get("/general",response={200:GeneralSchema,400:Message})
async def get_general(request):
    user=request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        gen = await Organization.objects.aget(id=user.organization.id)
        return 200, GeneralSchema.from_orm(gen)
    return 400,{"message":"organization doesn't exist"}

###########################  DEPARTMENT  ####################################

@general_setting_api.post("/department",response={201:DepartmentSchema,400:Message})
async def add_department(request,data:DepartmentInputSchema):
    user=request.auth
    if user and await sync_to_async(lambda:user.role == 'admin' and user.organization)():
        _data=data.dict(exclude={"department_head"})
        user_data=await sync_to_async(UserProfile.objects.get)(id=user.id) 
        department_head = None
        if data.department_head:
            department_head = await sync_to_async(UserProfile.objects.get)(id=data.department_head)
        dept = await sync_to_async(DepartmentSettings.objects.create)(**_data,department_head=department_head,updated_by=user_data)
        dept.department_head = department_head
        dept.updated_by = user_data
        return 201,DepartmentSchema.from_orm(dept) 
    return 400,{"message":"organization not found"}

@general_setting_api.get("/department", response={200: Union[List[DepartmentSchema], DepartmentSchema], 400: Message})
async def get_departments(request, id: Optional[int] = None):
    user = request.auth
    if user and await sync_to_async(lambda: user.organization)():
        base_query = DepartmentSettings.objects.select_related('department_head','updated_by').filter(updated_by__organization=user.organization)
        if id is not None:
            department = await sync_to_async(base_query.get)(id=id)  
            return 200, DepartmentSchema.from_orm(department)
        else:
            departments = await sync_to_async(list)(base_query)
            return 200, [DepartmentSchema.from_orm(dept) for dept in departments]
    return 400, {"message": "organization not found"}

@general_setting_api.put("/department", response={200: DepartmentSchema, 400: Message})
async def update_department(request, id: int, data: DepartmentInputSchema):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        department = await sync_to_async(DepartmentSettings.objects.select_related('department_head','updated_by').get)(id=id)
        _data = data.dict(exclude={"department_head"})
        for key, value in _data.items():
            setattr(department, key, value)
        if data.department_head:
            department_head = await sync_to_async(UserProfile.objects.get)(id=data.department_head)
            department.department_head = department_head
        user_data = await sync_to_async(UserProfile.objects.get)(id=user.id)
        department.updated_by = user_data
        await sync_to_async(department.save)()
        department = await sync_to_async(DepartmentSettings.objects.select_related('department_head','updated_by').get)(id=department.id)
        return 200, DepartmentSchema.from_orm(department)
    return 400, {"message": "Unauthorized or organization not found"}

@general_setting_api.delete("/department", response={200: Message, 404: Message, 400: Message})
async def delete_department(request, id: int):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        department = await sync_to_async(DepartmentSettings.objects.get)(id=id,department_head__organization=user.organization)
        await sync_to_async(department.delete)()
        return 200, {"message": "Department deleted successfully"}
    return 400, {"message": "Unauthorized or organization not found"}

#############################  DESIGNATION   #################################

@general_setting_api.get("/designation", response={200: Union[List[DesignationSchema], DesignationSchema],400: Message})
async def get_designations(request, id: Optional[int] = None):
    user = request.auth
    if user and await sync_to_async(lambda: user.organization)():
        base_query = DesignationSettings.objects.select_related('updated_by').filter(updated_by__organization=user.organization)
        if id is not None:
            designation = await sync_to_async(base_query.get)(id=id)
            return 200, DesignationSchema.from_orm(designation)
        else:
            designations = await sync_to_async(list)(base_query)
            return 200, designations
    return 400, {"message": "organization not found"}

@general_setting_api.post("/designation", response={201: DesignationSchema, 400: Message})
async def add_designation(request, data: DesignationInputSchema):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        _data = data.dict(exclude={"updated"})
        user_data = await sync_to_async(UserProfile.objects.get)(id=user.id)
        designation = await sync_to_async(DesignationSettings.objects.create)(**_data,updated_by=user_data)
        designation = await sync_to_async(DesignationSettings.objects.select_related('updated_by').get)(id=designation.id)
        return 201, DesignationSchema.from_orm(designation)
    return 400, {"message": "Unauthorized or organization not found"}

@general_setting_api.put("/designation", response={200: DesignationSchema,400: Message})
async def update_designation(request, id: int, data: DesignationInputSchema):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        designation = await sync_to_async(DesignationSettings.objects.select_related('updated_by').get)(id=id)
        _data = data.dict(exclude={"updated"})
        for key, value in _data.items():
            setattr(designation, key, value)
        user_data = await sync_to_async(UserProfile.objects.get)(id=user.id)
        designation.updated_by = user_data
        await sync_to_async(designation.save)()
        designation = await sync_to_async(DesignationSettings.objects.select_related('updated_by').get)(id=designation.id)
        return 200, DesignationSchema.from_orm(designation)
    return 400, {"message": "Unauthorized or organization not found"}

@general_setting_api.delete("/designation", response={200: Message,400: Message})
async def delete_designation(request, id: int):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        designation = await sync_to_async(DesignationSettings.objects.get)(id=id)
        await sync_to_async(designation.delete)()
        return 200, {"message": "Designation deleted successfully"}
    return 400, {"message": "Unauthorized or organization not found"}

################################ BANDS/GRADES  ###########################

@general_setting_api.get("/band", response={200: Union[List[Bandschema], Bandschema], 400: Message})
async def get_bands(request, id: Optional[int] = None):
    user = request.auth
    if user and await sync_to_async(lambda: user.organization)():
        base_query = BandsSettings.objects.select_related('updated_by').filter(updated_by__organization=user.organization)
        if id is not None:
            band = await sync_to_async(base_query.get)(id=id)
            return 200, Bandschema.from_orm(band)
        else:
            bands = await sync_to_async(list)(base_query)
            return 200, bands
    return 400, {"message": "organization not found"}

@general_setting_api.post("/band", response={201: Bandschema, 400: Message})
async def add_band(request, data: BandInputschema):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        _data = data.dict(exclude={"updated_by"})
        user_data = await sync_to_async(UserProfile.objects.get)(id=user.id)
        band = await sync_to_async(BandsSettings.objects.create)(**_data,updated_by=user_data)
        band = await sync_to_async(BandsSettings.objects.select_related('updated_by').get)(id=band.id)
        return 201, Bandschema.from_orm(band)
    return 400, {"message": "Unauthorized or organization not found"}

@general_setting_api.put("/band", response={200: Bandschema, 400: Message})
async def update_band(request, id: int, data: BandInputschema):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        band = await sync_to_async(BandsSettings.objects.select_related('updated_by').get)(id=id,updated_by__organization=user.organization)
        _data = data.dict(exclude={"updated_by"})
        for key, value in _data.items():
            setattr(band, key, value)
        user_data = await sync_to_async(UserProfile.objects.get)(id=user.id)
        band.updated_by = user_data
        await sync_to_async(band.save)()
        band = await sync_to_async(BandsSettings.objects.select_related('updated_by').get)(id=band.id)
        return 200, Bandschema.from_orm(band)
    return 400, {"message": "Unauthorized or organization not found"}

@general_setting_api.delete("/band", response={200: Message, 400: Message})
async def delete_band(request, id: int):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        band = await sync_to_async(BandsSettings.objects.get)(id=id)
        await sync_to_async(band.delete)()
        return 200, {"message": "Band deleted successfully"}
    return 400, {"message": "Unauthorized or organization not found"}

###############################   BUSINESS UNIT ######################################

@general_setting_api.get("/business-unit", response={200: Union[List[BusinessUnitSchema], BusinessUnitSchema], 400: Message})
async def get_business_units(request, id: Optional[int] = None):
    user = request.auth
    if user and await sync_to_async(lambda: user.organization)():
        base_query = BusinessUnitSettings.objects.select_related('unit_head','updated_by').filter(updated_by__organization=user.organization)
        if id is not None:
            business_unit = await sync_to_async(base_query.get)(id=id)
            return 200, BusinessUnitSchema.from_orm(business_unit)
        else:
            business_units = await sync_to_async(list)(base_query)
            return 200, business_units
    return 400, {"message": "organization not found"}

@general_setting_api.post("/business-unit", response={201: BusinessUnitSchema, 400: Message})
async def add_business_unit(request, data: BusinessUnitInputSchema):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        _data = data.dict(exclude={"unit_head", "updated_by"})
        user_data = await sync_to_async(UserProfile.objects.get)(id=user.id)
        unit_head = None
        if data.unit_head:
            unit_head = await sync_to_async(UserProfile.objects.get)(id=data.unit_head)
        business_unit = await sync_to_async(BusinessUnitSettings.objects.create)(**_data,unit_head=unit_head,updated_by=user_data)
        business_unit = await sync_to_async(BusinessUnitSettings.objects.select_related('unit_head', 'updated_by').get)(id=business_unit.id)
        return 201, BusinessUnitSchema.from_orm(business_unit)
    return 400, {"message": "Unauthorized or organization not found"}

@general_setting_api.put("/business-unit", response={200: BusinessUnitSchema, 400: Message})
async def update_business_unit(request, id: int, data: BusinessUnitInputSchema):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        business_unit = await sync_to_async(BusinessUnitSettings.objects.select_related('unit_head','updated_by').get)(id=id,updated_by__organization=user.organization )
        _data = data.dict(exclude={"unit_head", "updated_by"})
        for key, value in _data.items():
            setattr(business_unit, key, value)
        if data.unit_head:
            unit_head = await sync_to_async(UserProfile.objects.get)(id=data.unit_head)
            business_unit.unit_head = unit_head
        user_data = await sync_to_async(UserProfile.objects.get)(id=user.id)
        business_unit.updated_by = user_data
        await sync_to_async(business_unit.save)()
        business_unit = await sync_to_async(BusinessUnitSettings.objects.select_related('unit_head','updated_by').get)(id=business_unit.id)
        return 200, BusinessUnitSchema.from_orm(business_unit)
    return 400, {"message": "Unauthorized or organization not found"}

@general_setting_api.delete("/business-unit", response={200: Message,400: Message})
async def delete_business_unit(request, id: int):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        business_unit = await sync_to_async(BusinessUnitSettings.objects.get)(id=id)
        await sync_to_async(business_unit.delete)()
        return 200, {"message": "Business Unit deleted successfully"}
    return 400, {"message": "Unauthorized or organization not found"}

###########################  BILLING DETAILS ########################################

@general_setting_api.get("/billing-info", response={200: Union[List[BillingInfoSchema], BillingInfoSchema], 400: Message})
async def get_billing_info(request, id: Optional[int] = None):
    user = request.auth
    if user and await sync_to_async(lambda: user.organization)():
        base_query = BillingSettings.objects.select_related('updated_by').filter(updated_by__organization=user.organization)
        if id is not None:
            billing_info = await sync_to_async(base_query.get)(id=id)
            return 200, BillingInfoSchema.from_orm(billing_info)
        else:
            billing_infos = await sync_to_async(list)(base_query)
            return 200, billing_infos
    return 400, {"message": "organization not found"}

@general_setting_api.post("/billing-info", response={201: BillingInfoSchema, 400: Message})
async def add_billing_info(request, data: BillingInfoInputSchema):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        _data = data.dict(exclude={"updated_by"})
        user_data = await sync_to_async(UserProfile.objects.get)(id=user.id)
        billing_info = await sync_to_async(BillingSettings.objects.create)(**_data,updated_by=user_data)
        billing_info = await sync_to_async(BillingSettings.objects.select_related('updated_by').get)(id=billing_info.id)
        return 201, BillingInfoSchema.from_orm(billing_info)
    return 400, {"message": "Unauthorized or organization not found"}

@general_setting_api.put("/billing-info", response={200: BillingInfoSchema, 400: Message})
async def update_billing_info(request, id: int, data: BillingInfoSchema):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        billing_info = await sync_to_async(BillingSettings.objects.select_related('updated_by').get)(id=id,updated_by__organization=user.organization)
        _data = data.dict(exclude={"updated_by"})
        if not isinstance(_data['address'], dict):
            return 400, {"message": "Address must be a dictionary"}
        for key, value in _data.items():
            setattr(billing_info, key, value)
        user_data = await sync_to_async(UserProfile.objects.get)(id=user.id)
        billing_info.updated_by = user_data
        await sync_to_async(billing_info.save)()
        billing_info = await sync_to_async(BillingSettings.objects.select_related('updated_by').get)(id=billing_info.id)
        return 200, BillingInfoSchema.from_orm(billing_info)
    return 400, {"message": "Unauthorized or organization not found"}

@general_setting_api.delete("/billing-info", response={200: Message,400: Message})
async def delete_billing_info(request, id: int):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        billing_info = await sync_to_async(BillingSettings.objects.get)(id=id)
        await sync_to_async(billing_info.delete)()
        return 200, {"message": "Billing Info deleted successfully"}
    return 400, {"message": "Unauthorized or organization not found"}

