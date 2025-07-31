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
# @attendance_settings_api.post("/regularization_policies", response={201: Message, 403: Message, 409: Message})
# async def create_regularization_policies(request, data: RegularizationPoliciesSchema):
#     user = request.auth
#     if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
#         return 403, {"message": "Unauthorized access"}

#     org = await sync_to_async(lambda: user.organization)()
#     exists = await sync_to_async(RegularizationPolicies.objects.filter(organization=org).exists)()
#     if exists:
#         return 409, {"message": "Regularization Policies already exist for this organization"}

#     await sync_to_async(RegularizationPolicies.objects.create)(organization=org, **data.dict())
#     return 201, {"message": "Regularization Policies created successfully."}

# @attendance_settings_api.get("/regularization_policies", response={200: RegularizationPoliciesOutSchema, 404: Message})
# async def get_regularization_policies(request):
#     user = request.auth
#     org = await sync_to_async(getattr)(user, "organization")
    
#     if not org:
#         return 404, {"message": "Organization not found."}

#     try:
#         policies = await sync_to_async(
#             RegularizationPolicies.objects.select_related("organization").get
#         )(organization=org)

#         data = {
#             "organization": org.id,  # Only the organization ID
#             **{field: getattr(policies, field) for field in [
#                 "enable_justify_punch",
#                 "restrict_attendance_justification_days",
#                 "enable_request_punch",
#                 "enable_multiple_punches",
#                 "restrict_punch_request_days",
#                 "punch_approval_status",
#                 "restrict_duty_punch_employee",
#                 "restrict_real_time_justify_employee",
#                 "restrict_punch_request_manager",
#                 "restrict_attendance_approval_manager",
#                 "restrict_late_justify_manager",
#                 "restrict_early_exit_justify_manager",
#                 "restrict_total_time_justify_manager",
#             ]},
#         }
#         return 200, data

#     except RegularizationPolicies.DoesNotExist:
#         return 404, {"message": "Regularization Policies not found."}

# @attendance_settings_api.put("/regularization_policies", response={200: Message, 403: Message, 404: Message})
# async def update_regularization_policies(request, data: RegularizationPoliciesSchema):
#     user = request.auth
#     if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
#         return 403, {"message": "Unauthorized access"}

#     try:
#         policies = await sync_to_async(RegularizationPolicies.objects.get)(organization=user.organization)
#         for key, value in data.dict().items():
#             setattr(policies, key, value)
#         await sync_to_async(policies.save)()
#         return 200, {"message": "Regularization Policies updated successfully."}
#     except RegularizationPolicies.DoesNotExist:
#         return 404, {"message": "Regularization Policies not found."}

@attendance_settings_api.put("/general_policy", response={200: Message, 403: Message})
async def update_or_create_general_policy(request, data: GeneralPolicySchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == "admin" and user.organization)():
        return 403, {"message": "Unauthorized access"}

    org = await sync_to_async(lambda: user.organization)()

    policy, created = await sync_to_async(
        lambda: RegularizationPolicies.objects.get_or_create(organization=org)
    )()

    # Update only the general fields
    for key, value in data.dict().items():
        setattr(policy, key, value)

    await sync_to_async(policy.save)()
    msg = "created" if created else "updated"
    return 200, {"message": f"General policy {msg} successfully."}

    
@attendance_settings_api.get("/general_policy", response={200: GeneralPolicyOutSchema, 404: Message})
async def get_general_policy(request):
    user = request.auth
    org = await sync_to_async(getattr)(user, "organization")
    if not org:
        return 404, {"message": "Organization not found."}
    
    try:
        policy = await sync_to_async(RegularizationPolicies.objects.get)(organization=org)
        return 200, {
            "organization": {
                "id": org.id,
                "name": org.organization_name,
            },
            "enable_justify_punch": policy.enable_justify_punch,
            "restrict_attendance_justification_days": policy.restrict_attendance_justification_days,
            "enable_request_punch": policy.enable_request_punch,
            "enable_multiple_punches": policy.enable_multiple_punches,
            "restrict_punch_request_days": policy.restrict_punch_request_days,
            "punch_approval_status": policy.punch_approval_status,
        }
    except RegularizationPolicies.DoesNotExist:
        return 404, {"message": "Policy not found."}
    

@attendance_settings_api.put("/attendance_restriction_policy", response={200: Message, 403: Message})
async def update_or_create_attendance_restriction_policy(request, data: AttendanceRestrictionPolicySchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == "admin" and user.organization)():
        return 403, {"message": "Unauthorized access"}

    org = await sync_to_async(lambda: user.organization)()

    policy, created = await sync_to_async(
        lambda: RegularizationPolicies.objects.get_or_create(organization=org)
    )()

    # Update only the attendance restriction fields
    for key, value in data.dict().items():
        setattr(policy, key, value)

    await sync_to_async(policy.save)()
    msg = "created" if created else "updated"
    return 200, {"message": f"Attendance restriction policy {msg} successfully."}

@attendance_settings_api.get("/attendance_restriction_policy", response={200: AttendanceRestrictionPolicyOutSchema, 404: Message})
async def get_attendance_restriction_policy(request):
    user = request.auth
    org = await sync_to_async(getattr)(user, "organization")
    if not org:
        return 404, {"message": "Organization not found."}
    
    try:
        policy = await sync_to_async(RegularizationPolicies.objects.get)(organization=org)
        return 200, {
            "organization": {
                "id": org.id,
                "name": org.organization_name,
            },
            "enable_duty_punch_employee": policy.enable_duty_punch_employee,
            "restrict_duty_punch_employee": policy.restrict_duty_punch_employee,
            "enable_real_time_justify_employee": policy.enable_real_time_justify_employee,
            "restrict_real_time_justify_employee": policy.restrict_real_time_justify_employee,
            "enable_punch_request_manager": policy.enable_punch_request_manager,
            "restrict_punch_request_manager": policy.restrict_punch_request_manager,
            "enable_attendance_approval_manager": policy.enable_attendance_approval_manager,
            "restrict_attendance_approval_manager": policy.restrict_attendance_approval_manager,
            "enable_late_justify_manager": policy.enable_late_justify_manager,
            "restrict_late_justify_manager": policy.restrict_late_justify_manager,
            "enable_early_exit_justify_manager": policy.enable_early_exit_justify_manager,
            "restrict_early_exit_justify_manager": policy.restrict_early_exit_justify_manager,
            "enable_total_time_justify_manager": policy.enable_total_time_justify_manager,
            "restrict_total_time_justify_manager": policy.restrict_total_time_justify_manager,
        }
    except RegularizationPolicies.DoesNotExist:
        return 404, {"message": "Policy not found."}

################### SHIFT MANAGEMENT ######################
    
@attendance_settings_api.post("/manage_shift", response={201: Message, 403: Message, 409: Message})
async def create_shift(request, data: ShiftSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    org = await sync_to_async(lambda: user.organization)()
    exists = await sync_to_async(Shift.objects.filter(organization=org, shift_code=data.shift_code).exists)()
    if exists:
        return 409, {"message": "Shift with this code already exists for this organization"}

    await sync_to_async(Shift.objects.create)(organization=org, **data.dict())
    return 201, {"message": "Shift created successfully."}

@attendance_settings_api.get("/manage_shift", response={200: ShiftOutSchema, 404: Message})
async def get_shift(request):
    user = request.auth
    org = await sync_to_async(getattr)(user, "organization")
    
    if not org:
        return 404, {"message": "Organization not found."}

    try:
        shift = await sync_to_async(Shift.objects.get)(organization=org)

        data = {
            "organization": {
                "id": org.id,
                "name": org.organization_name,
            },
            "shift_type": shift.shift_type,
            "shift_code": shift.shift_code,
            "shift_title": shift.shift_title,
            "description": shift.description,
            "timein": shift.timein.strftime("%H:%M") if shift.timein else None,
            "timeout": shift.timeout.strftime("%H:%M") if shift.timeout else None,
            "make_default_shift": shift.make_default_shift,
        }

        return 200, data

    except Shift.DoesNotExist:
        return 404, {"message": "Shift not found."}
    
@attendance_settings_api.put("/manage_shift", response={200: Message, 403: Message, 404: Message})
async def update_shift(request, data: ShiftSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    try:
        shift = await sync_to_async(Shift.objects.get)(organization=user.organization, shift_code=data.shift_code)
        for key, value in data.dict().items():
            setattr(shift, key, value)
        await sync_to_async(shift.save)()
        return 200, {"message": "Shift updated successfully."}
    except Shift.DoesNotExist:
        return 404, {"message": "Shift not found."}

################### CALCULATION SETTINGS ######################

@attendance_settings_api.post("/calculation_settings", response={201: Message, 403: Message, 409: Message})
async def create_calculation_settings(request, data: CalculationSettingsSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    org = await sync_to_async(lambda: user.organization)()
    exists = await sync_to_async(CalculationPolicy.objects.filter(organization=org).exists)()
    if exists:
        return 409, {"message": "Calculation Settings already exist for this organization"}

    await sync_to_async(CalculationPolicy.objects.create)(organization=org, **data.dict())
    return 201, {"message": "Calculation Settings created successfully."}

@attendance_settings_api.get("/calculation_settings", response={200: CalculationSettingsOutSchema, 404: Message})
async def get_calculation_settings(request):
    user = request.auth
    org = await sync_to_async(getattr)(user, "organization")

    if not org:
        return 404, {"message": "Organization not found."}

    try:
        settings = await sync_to_async(CalculationPolicy.objects.get)(organization=org)

        data = {
            "organization": org.id,
            **{field: getattr(settings, field) for field in [
                "enable_attendance_unit",
                "number_of_unit_for_absent",
                "deduct_break_hours",
                "daily_auto_attendance_calculation",
                "enable_leave_based_rules",
                "auto_assign_shift",
            ]}
        }
        return 200, data

    except CalculationPolicy.DoesNotExist:
        return 404, {"message": "Calculation Settings not found."}

    
@attendance_settings_api.put("/calculation_settings", response={200: Message, 403: Message, 404: Message})
async def update_calculation_settings(request, data: CalculationSettingsSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    try:
        settings = await sync_to_async(CalculationPolicy.objects.get)(organization=user.organization)
        for key, value in data.dict().items():
            setattr(settings, key, value)
        await sync_to_async(settings.save)()
        return 200, {"message": "Calculation Settings updated successfully."}
    except CalculationPolicy.DoesNotExist:
        return 404, {"message": "Calculation Settings not found."}
    
########### sandwich rules settings ######################
@attendance_settings_api.post("/sandwich_rules_settings", response={201: Message, 403: Message, 409: Message})
async def create_sandwich_rules_settings(request, data: SandwichRulesSettingsSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    org = await sync_to_async(lambda: user.organization)()
    exists = await sync_to_async(SandwichRulesSettings.objects.filter(organization=org).exists)()
    if exists:
        return 409, {"message": "Sandwich Rules Settings already exist for this organization"}

    await sync_to_async(SandwichRulesSettings.objects.create)(organization=org, **data.dict())
    return 201, {"message": "Sandwich Rules Settings created successfully."}
@attendance_settings_api.get("/sandwich_rules_settings", response={200: SandwichRulesSettingsOutSchema, 404: Message})
async def get_sandwich_rules_settings(request):
    user = request.auth
    org = await sync_to_async(getattr)(user, "organization")

    if not org:
        return 404, {"message": "Organization not found."}

    try:
        settings = await sync_to_async(SandwichRulesSettings.objects.get)(organization=org)

        data = {
            "organization": org.id,
            **{field: getattr(settings, field) for field in [
                "enable_sandwich_rules",
                "week_off_holidays_between_absents",
                "week_off_holidays_after_absent",
                "week_off_holidays_before_absent",
                "absent_week_offs_holidays_beginning_month",
                "absent_week_offs_holidays_end_month",
            ]}
        }
        return 200, data

    except SandwichRulesSettings.DoesNotExist:
        return 404, {"message": "Sandwich Rules Settings not found."}
@attendance_settings_api.put("/sandwich_rules_settings", response={200: Message, 403: Message, 404: Message})
async def update_sandwich_rules_settings(request, data: SandwichRulesSettingsSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    try:
        settings = await sync_to_async(SandwichRulesSettings.objects.get)(organization=user.organization)
        for key, value in data.dict().items():
            setattr(settings, key, value)
        await sync_to_async(settings.save)()
        return 200, {"message": "Sandwich Rules Settings updated successfully."}
    except SandwichRulesSettings.DoesNotExist:
        return 404, {"message": "Sandwich Rules Settings not found."}
    
################### TIME MANAGEMENT POLICY ######################
@attendance_settings_api.post("/time_management_policy", response={201: Message, 403: Message, 409: Message})
async def create_time_management_policy(request, data: TimeManagementPolicySchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    org = await sync_to_async(lambda: user.organization)()
    exists = await sync_to_async(TimeManagementPolicy.objects.filter(organization=org).exists)()
    if exists:
        return 409, {"message": "Time Management Policy already exists for this organization"}

    await sync_to_async(TimeManagementPolicy.objects.create)(organization=org, **data.dict())
    return 201, {"message": "Time Management Policy created successfully."}
@attendance_settings_api.get("/time_management_policy", response={200: TimeManagementPolicyOutSchema, 404: Message})
async def get_time_management_policy(request):
    user = request.auth
    org = await sync_to_async(getattr)(user, "organization")

    if not org:
        return 404, {"message": "Organization not found."}

    try:
        policy = await sync_to_async(TimeManagementPolicy.objects.get)(organization=org)
        data = {
            "organization": org.id,
            **{field: getattr(policy, field) for field in [
                "enable_overtime",
                "overtime_approval_status",
                "round_off_minutes",
                "rounding_method",
                "rounding_value",
                "convert_overtime_to_compensation",
                "comp_off_request_on_overtime",
                "default_overtime_rule",
                "enable_undertime",
                "enable_attendance_rules",
            ]}
        }
        return 200, data

    except TimeManagementPolicy.DoesNotExist:
        return 404, {"message": "Time Management Policy not found."}
@attendance_settings_api.put("/time_management_policy", response={200: Message, 403: Message, 404: Message})
async def update_time_management_policy(request, data: TimeManagementPolicySchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    try:
        policy = await sync_to_async(TimeManagementPolicy.objects.get)(organization=user.organization)
        for key, value in data.dict().items():
            setattr(policy, key, value)
        await sync_to_async(policy.save)()
        return 200, {"message": "Time Management Policy updated successfully."}
    except TimeManagementPolicy.DoesNotExist:
        return 404, {"message": "Time Management Policy not found."}
    
#################  weeklyoff settings ######################

@attendance_settings_api.post("/weekly_off", response={201: Message, 403: Message, 409: Message})
async def create_weekly_off(request, data: WeeklyOffSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    org = await sync_to_async(lambda: user.organization)()
    exists = await sync_to_async(WeeklyOff.objects.filter(organization=org, weekday=data.weekday).exists)()
    if exists:
        return 409, {"message": f"Weekly Off for {data.weekday} already exists."}

    await sync_to_async(WeeklyOff.objects.create)(organization=org, **data.dict())
    return 201, {"message": "Weekly Off created successfully."}
@attendance_settings_api.get("/weekly_off", response={200: list[WeeklyOffOutSchema], 404: Message})
async def get_weekly_off(request):
    user = request.auth
    org = await sync_to_async(getattr)(user, "organization")
    
    if not org:
        return 404, {"message": "Organization not found."}

    weekly_offs = await sync_to_async(list)(
    WeeklyOff.objects.select_related("organization").filter(organization=org).all() 
    )


    data = [
        WeeklyOffOutSchema(
            organization=wo.organization.id,
            weekday=wo.weekday,
            all_weeks=wo.all_weeks,
            second_week=wo.second_week,
            fifth_week=wo.fifth_week,
            alternate_weeks=wo.alternate_weeks,
            all_but_last=wo.all_but_last,
            third_week=wo.third_week,
            last_two_weeks=wo.last_two_weeks,
            first_week=wo.first_week,
            fourth_week=wo.fourth_week,
            last_week=wo.last_week,
        )
        for wo in weekly_offs
    ]
    return 200, data
@attendance_settings_api.put("/weekly_off/{weekday}", response={200: Message, 403: Message, 404: Message})
async def update_weekly_off(request, weekday: str, data: WeeklyOffSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    try:
        weekly_off = await sync_to_async(WeeklyOff.objects.get)(organization=user.organization, weekday=weekday)
        for key, value in data.dict().items():
            setattr(weekly_off, key, value)
        await sync_to_async(weekly_off.save)()
        return 200, {"message": f"Weekly Off for {weekday} updated successfully."}
    except WeeklyOff.DoesNotExist:
        return 404, {"message": f"Weekly Off for {weekday} not found."}
    
############### ALLOWED IP SETTINGS ######################
@attendance_settings_api.post("/allowed_ips", response={201: Message, 403: Message, 409: Message})
async def add_allowed_ip(request, data: AllowedIPSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    org = await sync_to_async(lambda: user.organization)()
    exists = await sync_to_async(AllowedIP.objects.filter(organization=org, ip_address=data.ip_address).exists)()
    if exists:
        return 409, {"message": "IP address already allowed for this organization"}

    await sync_to_async(AllowedIP.objects.create)(
        organization=org,
        ip_address=data.ip_address,
        addedby=user,
        added_from_ip=data.added_from_ip
    )
    return 201, {"message": "IP address added successfully."}
@attendance_settings_api.get("/allowed_ips", response={200: list[AllowedIPOutSchema], 404: Message})
async def get_allowed_ips(request):
    user = request.auth
    org = await sync_to_async(lambda: user.organization)()
    if not org:
        return 404, {"message": "Organization not found"}

    allowed_ips = await sync_to_async(list)(
        AllowedIP.objects.filter(organization=org)
    )

    data = [
        AllowedIPOutSchema(
            organization=ip.organization.id,
            ip_address=ip.ip_address,
            addedby=ip.addedby.id if ip.addedby else None,
            addedon=ip.addedon,
            added_from_ip=ip.added_from_ip
        )
        for ip in allowed_ips
    ]
    return 200, data
@attendance_settings_api.put("/allowed_ips/{ip_id}", response={200: Message, 403: Message, 404: Message})
async def update_allowed_ip(request, ip_id: int, data: AllowedIPSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    try:
        ip_record = await sync_to_async(AllowedIP.objects.get)(id=ip_id, organization=user.organization)
        ip_record.ip_address = data.ip_address
        ip_record.added_from_ip = data.added_from_ip
        await sync_to_async(ip_record.save)()
        return 200, {"message": "IP address updated successfully."}
    except AllowedIP.DoesNotExist:
        return 404, {"message": "IP address not found."}
    
#########  COMPENSATION RULES SETTINGS ######################

@attendance_settings_api.post("/compensation_rules", response={201: Message, 403: Message, 409: Message})
async def create_compensation_rules(request, data: CompensationRulesSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    org = await sync_to_async(lambda: user.organization)()
    exists = await sync_to_async(CompensationRules.objects.filter(organization=org).exists)()
    if exists:
        return 409, {"message": "Compensation Rules already exist for this organization"}

    await sync_to_async(CompensationRules.objects.create)(organization=org, **data.dict())
    return 201, {"message": "Compensation Rules created successfully."}

@attendance_settings_api.get("/compensation_rules", response={200: CompensationRulesOutSchema, 404: Message})
async def get_compensation_rules(request):
    user = request.auth
    org = await sync_to_async(lambda: user.organization)()
    if not org:
        return 404, {"message": "Organization not found"}

    try:
        rules = await sync_to_async(CompensationRules.objects.get)(organization=org)
        return 200, CompensationRulesOutSchema(
            organization=org.id,
            daily_eligiibility=rules.daily_eligiibility,
            weekoff_eligiibility=rules.weekoff_eligiibility,
            holiday_eligiibility=rules.holiday_eligiibility,
            daily_rule=rules.daily_rule,
            weekoff_rule=rules.weekoff_rule,
            holiday_rule=rules.holiday_rule,
        )
    except CompensationRules.DoesNotExist:
        return 404, {"message": "Compensation Rules not found."}

@attendance_settings_api.put("/compensation_rules", response={200: Message, 403: Message, 404: Message})
async def update_compensation_rules(request, data: CompensationRulesSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    try:
        rules = await sync_to_async(CompensationRules.objects.get)(organization=user.organization)
        for key, value in data.dict().items():
            setattr(rules, key, value)
        await sync_to_async(rules.save)()
        return 200, {"message": "Compensation Rules updated successfully."}
    except CompensationRules.DoesNotExist:
        return 404, {"message": "Compensation Rules not found."}

##################  compoff settings ######################
@attendance_settings_api.post("/comp_off_rules", response={201: Message, 403: Message, 409: Message})
async def create_comp_off_rules(request, data: CompOffRulesSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    org = await sync_to_async(lambda: user.organization)()
    exists = await sync_to_async(CompOffRules.objects.filter(organization=org).exists)()
    if exists:
        return 409, {"message": "Comp Off Rules already exist for this organization"}

    await sync_to_async(CompOffRules.objects.create)(organization=org, **data.dict())
    return 201, {"message": "Comp Off Rules created successfully."}

@attendance_settings_api.get("/comp_off_rules", response={200: CompOffRulesOutSchema, 404: Message})
async def get_comp_off_rules(request):
    user = request.auth
    org = await sync_to_async(lambda: user.organization)()
    if not org:
        return 404, {"message": "Organization not found"}

    try:
        rules = await sync_to_async(CompOffRules.objects.get)(organization=org)
        return 200, CompOffRulesOutSchema(
            organization=org.id,
            daily_eligiibility=rules.daily_eligiibility,
            weekoff_eligiibility=rules.weekoff_eligiibility,
            holiday_eligiibility=rules.holiday_eligiibility,
            daily_rule=rules.daily_rule,
            weekoff_rule=rules.weekoff_rule,
            holiday_rule=rules.holiday_rule,
        )
    except CompOffRules.DoesNotExist:
        return 404, {"message": "Comp Off Rules not found."}

@attendance_settings_api.put("/comp_off_rules", response={200: Message, 403: Message, 404: Message})
async def update_comp_off_rules(request, data: CompOffRulesSchema):
    user = request.auth
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    try:
        rules = await sync_to_async(CompOffRules.objects.get)(organization=user.organization)
        for key, value in data.dict().items():
            setattr(rules, key, value)
        await sync_to_async(rules.save)()
        return 200, {"message": "Comp Off Rules updated successfully."}
    except CompOffRules.DoesNotExist:
        return 404, {"message": "Comp Off Rules not found."}

############### undertime settings ######################
@attendance_settings_api.post("/under_time_rule", response={201: Message, 403: Message, 409: Message})
async def create_under_time_rule(request, data: UnderTimeRuleSchema):
    user = request.auth
    # Admin + org check
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    org = await sync_to_async(lambda: user.organization)()
    exists = await sync_to_async(UnderTimeRule.objects.filter(organization=org).exists)()
    if exists:
        return 409, {"message": "UnderTimeRule already exists for this organization"}

    await sync_to_async(UnderTimeRule.objects.create)(organization=org, **data.dict())
    return 201, {"message": "UnderTimeRule created successfully."}

@attendance_settings_api.get("/under_time_rule", response={200: UnderTimeRuleOutSchema, 404: Message})
async def get_under_time_rule(request):
    user = request.auth
    org = await sync_to_async(lambda: getattr(user, "organization", None))()
    if not org:
        return 404, {"message": "Organization not found."}

    try:
        rule = await sync_to_async(UnderTimeRule.objects.get)(organization=org)
        return 200, UnderTimeRuleOutSchema(
            organization=org.id,
            eligiblity_hours=rule.eligiblity_hours,
            consider_absent=rule.consider_absent,
            conside_half_day=rule.conside_half_day,
        )
    except UnderTimeRule.DoesNotExist:
        return 404, {"message": "UnderTimeRule not found."}

@attendance_settings_api.put("/under_time_rule", response={200: Message, 403: Message, 404: Message})
async def update_under_time_rule(request, data: UnderTimeRuleSchema):
    user = request.auth
    # Admin + org check
    if not user or not await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        return 403, {"message": "Unauthorized access"}

    try:
        rule = await sync_to_async(UnderTimeRule.objects.get)(organization=user.organization)
        for key, value in data.dict().items():
            setattr(rule, key, value)
        await sync_to_async(rule.save)()
        return 200, {"message": "UnderTimeRule updated successfully."}
    except UnderTimeRule.DoesNotExist:
        return 404, {"message": "UnderTimeRule not found."}








