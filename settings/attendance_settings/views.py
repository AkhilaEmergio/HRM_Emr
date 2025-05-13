from django.shortcuts import render
from ninja import Router
from settings.attendance_settings.schema import *
from settings.attendance_settings.models import *
from asgiref.sync import sync_to_async
# Create your views here.

attendance_settings_api = Router(tags=['attendance_settings'])

@attendance_settings_api.post("/attendance_settings", response={201: Message, 403: Message, 409: Message})
async def create_attendance_settings(request, data: AttendenceSettingSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    org = await sync_to_async(lambda: user.organization)()
    exists = await sync_to_async(AttendaceSettings.objects.filter(organization=org).exists)()
    if exists:
        return 409, {"message": "Attendance Settings already exist for this organization"}

    await sync_to_async(AttendaceSettings.objects.create)(organization=org, **data.dict())
    return 201, {"message": "Attendance Settings created successfully."}

@attendance_settings_api.get("/attendance_settings", 
    response={200: AttendenceSettingOutSchema, 404: Message})
async def get_attendance_settings(request):
    user = request.auth
    org = await sync_to_async(getattr)(user, "organization")
    
    if not org:
        return 404, {"message": "Organization not found."}

    try:
        settings = await sync_to_async(
            AttendaceSettings.objects.select_related("organization").get
        )(organization=org)

        data = {
            "organization": {
                "id": org.id,
                "name": org.organization_name,
            },
            **{field: getattr(settings, field) for field in [
                "enable_attendance",
                "default_attendance_status",
                "deduct_salary_for_absent_days",
                "hide_total_hours",
                "hide_attendance_punches",
                "disable_web_attendance",
                "enable_ip_restrictions",
                "disable_mobile_attendance",
            ]},
            "company_start_time": settings.company_start_time.strftime("%H:%M") if settings.company_start_time else None,
            "company_end_time": settings.company_end_time.strftime("%H:%M") if settings.company_end_time else None,
        }
        return 200, data

    except AttendaceSettings.DoesNotExist:
        return 404, {"message": "Attendance Settings not found."}


@attendance_settings_api.put("/attendance_settings", response={200: Message, 403: Message, 404: Message})
async def update_attendance_settings(request, data: AttendenceSettingSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    try:
        settings = await sync_to_async(AttendaceSettings.objects.get)(organization=user.organization)
        for key, value in data.dict().items():
            setattr(settings, key, value)
        await sync_to_async(settings.save)()
        return 200, {"message": "Attendance Settings updated successfully."}
    except AttendaceSettings.DoesNotExist:
        return 404, {"message": "Attendance Settings not found."}

##############  ROSTER SHIFTS #############################

@attendance_settings_api.post("/roster_shift_settings", response={201: Message, 403: Message, 409: Message})
async def create_roster_shift_settings(request, data: RosterShiftSettingsSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    org = await sync_to_async(lambda: user.organization)()
    exists = await sync_to_async(RosterShiftSettings.objects.filter(organization=org).exists)()
    if exists:
        return 409, {"message": "Roster Shift Settings already exist for this organization"}

    await sync_to_async(RosterShiftSettings.objects.create)(organization=org, **data.dict())
    return 201, {"message": "Roster Shift Settings created successfully."}



@attendance_settings_api.get("/roster_shift_settings", response={200: RosterShiftSettingsOutSchema, 404: Message})
async def get_roster_shift_settings(request):
    user = request.auth
    org = await sync_to_async(getattr)(user, "organization")
    
    if not org:
        return 404, {"message": "Organization not found."}

    try:
        settings = await sync_to_async(RosterShiftSettings.objects.select_related("organization").get)(organization=org)

        data = {
    "organization": {
                "id": org.id,
                "name": org.organization_name,
            },  # Only the organization ID is needed here
    **{field: getattr(settings, field) for field in [
        "enable_roster_shifts",
        "allow_managers_assign_shifts",
        "restrict_shift_change_days",
        "restrict_week_off_per_month",
        "restrict_week_off_per_week",
    ]},
}
        return 200, data

    except RosterShiftSettings.DoesNotExist:
        return 404, {"message": "Roster Shift Settings not found."}

@attendance_settings_api.put("/roster_shift_settings", response={200: Message, 403: Message, 404: Message})
async def update_roster_shift_settings(request, data: RosterShiftSettingsSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    try:
        settings = await sync_to_async(RosterShiftSettings.objects.get)(organization=user.organization)
        for key, value in data.dict().items():
            setattr(settings, key, value)
        await sync_to_async(settings.save)()
        return 200, {"message": "Roster Shift Settings updated successfully."}
    except RosterShiftSettings.DoesNotExist:
        return 404, {"message": "Roster Shift Settings not found."}

################### SHIFT CHANGE SETTINGS ######################
@attendance_settings_api.post("/shift_change_settings", response={201: Message, 403: Message, 409: Message})
async def create_shift_change_settings(request, data: ShiftChangeSettingsSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    org = await sync_to_async(lambda: user.organization)()
    exists = await sync_to_async(ShiftChangeSettings.objects.filter(organization=org).exists)()
    if exists:
        return 409, {"message": "Shift Change Settings already exist for this organization"}

    await sync_to_async(ShiftChangeSettings.objects.create)(organization=org, **data.dict())
    return 201, {"message": "Shift Change Settings created successfully."}

@attendance_settings_api.get("/shift_change_settings", response={200: ShiftChangeSettingsOutSchema, 404: Message})
async def get_shift_change_settings(request):
    user = request.auth
    org = await sync_to_async(getattr)(user, "organization")
    
    if not org:
        return 404, {"message": "Organization not found."}

    try:
        settings = await sync_to_async(
            ShiftChangeSettings.objects.select_related("organization").get
        )(organization=org)

        data = {
            "organization": {
                "id": org.id,
                "name": org.organization_name,
            },
            **{field: getattr(settings, field) for field in [
                "allow_employee_shift_change_request",
                "enable_manager_approval",
                "default_approval_status",
            ]},
        }
        return 200, data

    except ShiftChangeSettings.DoesNotExist:
        return 404, {"message": "Shift Change Settings not found."}

    
@attendance_settings_api.put("/shift_change_settings", response={200: Message, 403: Message, 404: Message})
async def update_shift_change_settings(request, data: ShiftChangeSettingsSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    try:
        settings = await sync_to_async(ShiftChangeSettings.objects.get)(organization=user.organization)
        for key, value in data.dict().items():
            setattr(settings, key, value)
        await sync_to_async(settings.save)()
        return 200, {"message": "Shift Change Settings updated successfully."}
    except ShiftChangeSettings.DoesNotExist:
        return 404, {"message": "Shift Change Settings not found."}

################### REGULARIZATION POLICIES ######################
@attendance_settings_api.post("/regularization_policies", response={201: Message, 403: Message, 409: Message})
async def create_regularization_policies(request, data: RegularizationPoliciesSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    org = await sync_to_async(lambda: user.organization)()
    exists = await sync_to_async(RegularizationPolicies.objects.filter(organization=org).exists)()
    if exists:
        return 409, {"message": "Regularization Policies already exist for this organization"}

    await sync_to_async(RegularizationPolicies.objects.create)(organization=org, **data.dict())
    return 201, {"message": "Regularization Policies created successfully."}

@attendance_settings_api.get("/regularization_policies", response={200: RegularizationPoliciesOutSchema, 404: Message})
async def get_regularization_policies(request):
    user = request.auth
    org = await sync_to_async(getattr)(user, "organization")
    
    if not org:
        return 404, {"message": "Organization not found."}

    try:
        policies = await sync_to_async(
            RegularizationPolicies.objects.select_related("organization").get
        )(organization=org)

        data = {
            "organization": org.id,  # Only the organization ID
            **{field: getattr(policies, field) for field in [
                "enable_justify_punch",
                "restrict_attendance_justification_days",
                "enable_request_punch",
                "enable_multiple_punches",
                "restrict_punch_request_days",
                "punch_approval_status",
                "restrict_duty_punch_employee",
                "restrict_real_time_justify_employee",
                "restrict_punch_request_manager",
                "restrict_attendance_approval_manager",
                "restrict_late_justify_manager",
                "restrict_early_exit_justify_manager",
                "restrict_total_time_justify_manager",
            ]},
        }
        return 200, data

    except RegularizationPolicies.DoesNotExist:
        return 404, {"message": "Regularization Policies not found."}

@attendance_settings_api.put("/regularization_policies", response={200: Message, 403: Message, 404: Message})
async def update_regularization_policies(request, data: RegularizationPoliciesSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    try:
        policies = await sync_to_async(RegularizationPolicies.objects.get)(organization=user.organization)
        for key, value in data.dict().items():
            setattr(policies, key, value)
        await sync_to_async(policies.save)()
        return 200, {"message": "Regularization Policies updated successfully."}
    except RegularizationPolicies.DoesNotExist:
        return 404, {"message": "Regularization Policies not found."}

################### SHIFT MANAGEMENT ######################
    
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
    
@attendance_settings_api.post("/calculate_attendance", response={200: Message, 404: Message})
async def create_calculation_settings(request, data: CalculationSettingsSchema):
    created_by = request.auth 
    if CalculationSettingsSchema.objects.filter(organization=data.organization).exists():
        return 409, {"message": "Calculation Settings already exists for this organization"}
    CalculationSettingsSchema.objects.create(**data.dict())
    return 201, {"message": "Calculation Settings created successfully."}

@attendance_settings_api.get("/calculate_attendance", response={200: CalculationSettingsSchema, 404: Message})
async def get_calculation_settings(request, organization:int):
    try:
        calculation_settings = CalculationSettingsSchema.objects.get(organization=organization)
        return 200, calculation_settings
    except CalculationSettingsSchema.DoesNotExist:
        return 404, {"message": "Calculation Settings not found."}
    
@attendance_settings_api.put("/calculate_attendance", response={200: Message, 404: Message})
async def update_calculation_settings(request, data: CalculationSettingsSchema):
    try:
        calculation_settings = CalculationSettingsSchema.objects.get(organization=data.organization)
        for key, value in data.dict().items():
            setattr(calculation_settings, key, value)
        calculation_settings.save()
        return 200, {"message": "Calculation Settings updated successfully."}
    except CalculationSettingsSchema.DoesNotExist:  
        return 404, {"message": "Calculation Settings not found."}

