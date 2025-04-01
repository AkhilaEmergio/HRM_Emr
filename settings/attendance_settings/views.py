from django.shortcuts import render
from ninja import Router
from schema import *
from settings.attendance_settings.models import *
# Create your views here.

attendance_settings_api = Router(tags=['attendance_settings'])

@attendance_settings_api.post("/attendance_settings", response={201: Message, 403: Message, 409: Message})
async def create_attendance_settings(request, data: AttendenceSettingSchema):
    created_by = request.auth
    if AttendaceSettings.objects.filter(organization=data.organization).exists():
        return 409, {"message": "Attendance Settings already exists for this organization"}
    AttendaceSettings.objects.create(**data.dict())
    return 201, {"message": "Attendance Settings created successfully."}

@attendance_settings_api.get("/attendance_settings", response={200: AttendenceSettingSchema, 404: Message})
async def get_attendance_settings(request, organization:int):
    try:
        attendance_settings = AttendaceSettings.objects.get(organization=organization)
        return 200, attendance_settings
    except AttendaceSettings.DoesNotExist:
        return 404, {"message": "Attendance Settings not found."}
    
@attendance_settings_api.put("/attendance_settings", response={200: Message, 404: Message})
async def update_attendance_settings(request, data: AttendenceSettingSchema):
    try:
        attendance_settings = AttendaceSettings.objects.get(organization=data.organization)
        for key, value in data.dict().items():
            setattr(attendance_settings, key, value)
        attendance_settings.save()
        return 200, {"message": "Attendance Settings updated successfully."}
    except AttendaceSettings.DoesNotExist:
        return 404, {"message": "Attendance Settings not found."}

@attendance_settings_api.post("/roster_shift_settings", response={201: Message, 403: Message, 409: Message})
async def roster_shift_settings(request, data: RosterShiftSettingsSchema):
    created_by = request.auth
    if RosterShiftSettings.objects.filter(organization=data.organization).exists():
        return 409, {"message": "Roster Shift Settings already exists for this organization"}
    RosterShiftSettings.objects.create(**data.dict())
    return 201, {"message": "Roster Shift Settings created successfully."}

@attendance_settings_api.get("/roster_shift_settings", response={200: RosterShiftSettingsSchema, 404: Message})
async def get_roster_shift_settings(request, organization:int):
    try:
        roster_shift_settings = RosterShiftSettings.objects.get(organization=organization)
        return 200, roster_shift_settings
    except RosterShiftSettings.DoesNotExist:
        return 404, {"message": "Roster Shift Settings not found."}
    
@attendance_settings_api.put("/roster_shift_settings", response={200: Message, 404: Message})
async def update_roster_shift_settings(request, data: RosterShiftSettingsSchema):
    try:
        roster_shift_settings = RosterShiftSettings.objects.get(organization=data.organization)
        for key, value in data.dict().items():
            setattr(roster_shift_settings, key, value)
        roster_shift_settings.save()
        return 200, {"message": "Roster Shift Settings updated successfully."}
    except RosterShiftSettings.DoesNotExist:
        return 404, {"message": "Roster Shift Settings not found."}

   
@attendance_settings_api.post("/shift_change_settings", response={201: Message, 403: Message, 409: Message})
async def shift_change_settings(request, data: ShiftChangeSettingsSchema):
    created_by = request.auth
    if ShiftChangeSettings.objects.filter(organization=data.organization).exists():
        return 409, {"message": "Shift Change Settings already exists for this organization"}
    ShiftChangeSettings.objects.create(**data.dict())
    return 201, {"message": "Shift Change Settings created successfully."}

@attendance_settings_api.get("/shift_change_settings", response={200: ShiftChangeSettingsSchema, 404: Message})
async def get_shift_change_settings(request, organization:int):
    try:
        shift_change_settings = ShiftChangeSettings.objects.get(organization=organization)
        return 200, shift_change_settings
    except ShiftChangeSettings.DoesNotExist:
        return 404, {"message": "Shift Change Settings not found."}
    
@attendance_settings_api.put("/shift_change_settings", response={200: Message, 404: Message})
async def update_shift_change_settings(request, data: ShiftChangeSettingsSchema):
    try:
        shift_change_settings = ShiftChangeSettings.objects.get(organization=data.organization)
        for key, value in data.dict().items():
            setattr(shift_change_settings, key, value)
        shift_change_settings.save()
        return 200, {"message": "Shift Change Settings updated successfully."}
    except ShiftChangeSettings.DoesNotExist:
        return 404, {"message": "Shift Change Settings not found."} 
    
@attendance_settings_api.post("/regularization_policies", response={201: Message, 403: Message, 409: Message})
async def regularization_policies(request, data: RegularizationPoliciesSchema):
    created_by = request.auth
    if RegularizationPolicies.objects.filter(organization=data.organization).exists():
        return 409, {"message": "Regularization Policies already exists for this organization"}
    RegularizationPolicies.objects.create(**data.dict())
    return 201, {"message": "Regularization Policies created successfully."}

@attendance_settings_api.get("/regularization_policies", response={200: RegularizationPoliciesSchema, 404: Message})
async def get_regularization_policies(request, organization:int):
    try:
        regularization_policies = RegularizationPolicies.objects.get(organization=organization)
        return 200, regularization_policies
    except RegularizationPolicies.DoesNotExist:
        return 404, {"message": "Regularization Policies not found."}
    
@attendance_settings_api.put("/regularization_policies", response={200: Message, 404: Message})
async def update_regularization_policies(request, data: RegularizationPoliciesSchema):
    try:
        regularization_policies = RegularizationPolicies.objects.get(organization=data.organization)
        for key, value in data.dict().items():
            setattr(regularization_policies, key, value)
        regularization_policies.save()
        return 200, {"message": "Regularization Policies updated successfully."}
    except RegularizationPolicies.DoesNotExist:
        return 404, {"message": "Regularization Policies not found."}
    
@attendance_settings_api.post("/manage_shift", response={201: Message, 403: Message, 409: Message})
async def manage_shift(request, data: ShiftSchema):
    created_by = request.auth
    if Shift.objects.filter(organization=data.organization,shift_code=data.shift_code).exists():
        return 409, {"message": "Shift already exists for this organization"}
    Shift.objects.create(**data.dict())
    return 201, {"message": "Shift created successfully."}

@attendance_settings_api.get("/manage_shift", response={200: ShiftSchema, 404: Message})
async def get_shift(request, organization:int):
    try:
        shift = Shift.objects.get(organization=organization)
        return 200, shift
    except Shift.DoesNotExist:
        return 404, {"message": "Shift not found."}
    
@attendance_settings_api.put("/manage_shift", response={200: Message, 404: Message})
async def update_shift(request, data: ShiftSchema):
    try:
        shift = Shift.objects.get(organization=data.organization)
        for key, value in data.dict().items():
            setattr(shift, key, value)
        shift.save()
        return 200, {"message": "Shift updated successfully."}
    except Shift.DoesNotExist:
        return 404, {"message": "Shift not found."}
    