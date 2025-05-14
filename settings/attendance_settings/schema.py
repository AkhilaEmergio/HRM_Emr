from datetime import date, datetime, time
from ninja import Schema
from typing import *

from pydantic import field_serializer
from employee.basic_details.schema import *

class organizationDetail(Schema):
     id:int
     name:str

class Message(Schema):
    message: str

class AttendenceSettingSchema(Schema):
    enable_attendance: bool
    default_attendance_status:Optional[str]
    deduct_salary_for_absent_days: Optional[str]
    company_start_time:Optional[str]
    company_end_time: Optional[str]
    hide_total_hours: Optional[bool]
    hide_attendance_punches: Optional[bool]
    disable_web_attendance: Optional[bool]
    enable_ip_restrictions: Optional[bool]
    disable_mobile_attendance: Optional[bool]

class AttendenceSettingOutSchema(Schema):
    organization: Optional[organizationDetail]
    enable_attendance: bool
    default_attendance_status: Optional[str]
    deduct_salary_for_absent_days: Optional[str]
    company_start_time: Optional[str]
    company_end_time: Optional[str]
    hide_total_hours: Optional[bool]
    hide_attendance_punches: Optional[bool]
    disable_web_attendance: Optional[bool]
    enable_ip_restrictions: Optional[bool]
    disable_mobile_attendance: Optional[bool]


class RosterShiftSettingsSchema(Schema):
    enable_roster_shifts: Optional[bool]
    allow_managers_assign_shifts: Optional[bool]
    restrict_shift_change_days: Optional[int]
    restrict_week_off_per_month: Optional[int]
    restrict_week_off_per_week: Optional[int]

class RosterShiftSettingsOutSchema(Schema):
    organization: Optional[organizationDetail]
    enable_roster_shifts: Optional[bool]
    allow_managers_assign_shifts: Optional[bool]
    restrict_shift_change_days: Optional[int]
    restrict_week_off_per_month: Optional[int]
    restrict_week_off_per_week: Optional[int]

class ShiftChangeSettingsSchema(Schema):
    allow_employee_shift_change_request: Optional[bool]
    enable_manager_approval: Optional[bool]
    default_approval_status: Optional[str]

class ShiftChangeSettingsOutSchema(Schema):
    organization: Optional[organizationDetail]
    allow_employee_shift_change_request: Optional[bool]
    enable_manager_approval: Optional[bool]
    default_approval_status: Optional[str]

class RegularizationPoliciesSchema(Schema):
    enable_justify_punch: Optional[bool]
    restrict_attendance_justification_days: Optional[int]
    enable_request_punch: Optional[bool]
    enable_multiple_punches: Optional[bool]
    restrict_punch_request_days: Optional[int]
    punch_approval_status: Optional[str]
    restrict_duty_punch_employee: Optional[int]
    restrict_real_time_justify_employee: Optional[int]
    restrict_punch_request_manager: Optional[int]
    restrict_attendance_approval_manager: Optional[int]
    restrict_late_justify_manager: Optional[int]
    restrict_early_exit_justify_manager: Optional[int]
    restrict_total_time_justify_manager: Optional[int]

class RegularizationPoliciesOutSchema(Schema):
    organization: Optional[organizationDetail]
    enable_justify_punch: Optional[bool]
    restrict_attendance_justification_days: Optional[int]
    enable_request_punch: Optional[bool]
    enable_multiple_punches: Optional[bool]
    restrict_punch_request_days: Optional[int]
    punch_approval_status: Optional[str]
    restrict_duty_punch_employee: Optional[int]
    restrict_real_time_justify_employee: Optional[int]
    restrict_punch_request_manager: Optional[int]
    restrict_attendance_approval_manager: Optional[int]
    restrict_late_justify_manager: Optional[int]
    restrict_early_exit_justify_manager: Optional[int]
    restrict_total_time_justify_manager: Optional[int]


class ShiftSchema(Schema):
    shift_type: Optional[str]
    shift_code: Optional[str]
    shift_title:Optional[str]
    description: Optional[str]
    timein: Optional[str]
    timeout: Optional[str]    
    make_default_shift: Optional[bool]

class ShiftOutSchema(Schema):
    organization: Optional[organizationDetail]
    shift_type: Optional[str]
    shift_code: Optional[str]
    shift_title:Optional[str]
    description: Optional[str]
    timein: Optional[str]
    timeout: Optional[str]    
    make_default_shift: Optional[bool]


class CalculationSettingsSchema(Schema):
    enable_attendance_unit: Optional[bool]
    number_of_unit_for_absent: Optional[int]
    deduct_break_hours: Optional[bool]
    daily_auto_attendance_calculation: Optional[bool]
    enable_leave_based_rules: Optional[bool]
    auto_assign_shift_work: Optional[bool]

class CalculationSettingsOutSchema(Schema):
    organization: int
    enable_attendance_unit: Optional[bool]
    number_of_unit_for_absent: Optional[int]
    deduct_break_hours: Optional[bool]
    daily_auto_attendance_calculation: Optional[bool]
    enable_leave_based_rules: Optional[bool]
    auto_assign_shift_work: Optional[bool]

class SandwichRulesSettingsSchema(Schema):
    enable_sandwich_rules: Optional[bool]
    week_off_holidays_between_absents: Optional[bool]
    week_off_holidays_after_absent: Optional[bool]
    week_off_holidays_before_absent: Optional[bool]
    absent_week_offs_holidays_beginning_month: Optional[bool]
    absent_week_offs_holidays_end_month: Optional[bool]

class SandwichRulesSettingsOutSchema(Schema):
    organization: int
    enable_sandwich_rules: Optional[bool]
    week_off_holidays_between_absents: Optional[bool]
    week_off_holidays_after_absent: Optional[bool]
    week_off_holidays_before_absent: Optional[bool]
    absent_week_offs_holidays_beginning_month: Optional[bool]
    absent_week_offs_holidays_end_month: Optional[bool]

class TimeManagementPolicySchema(Schema):
    enable_overtime: Optional[bool]
    overtime_approval_status: Optional[str]
    round_off_minutes: Optional[bool]
    rounding_method: Optional[str]
    rounding_value: Optional[int]
    convert_overtime_to_compensation: Optional[bool]
    comp_off_request_on_overtime: Optional[bool]
    default_overtime_rule: Optional[str]
    enable_undertime: Optional[bool]
    enable_attendance_rules: Optional[bool]

class TimeManagementPolicyOutSchema(Schema):
    organization: int
    enable_overtime: Optional[bool]
    overtime_approval_status: Optional[str]
    round_off_minutes: Optional[bool]
    rounding_method: Optional[str]
    rounding_value: Optional[int]
    convert_overtime_to_compensation: Optional[bool]
    comp_off_request_on_overtime: Optional[bool]
    default_overtime_rule: Optional[str]
    enable_undertime: Optional[bool]
    enable_attendance_rules: Optional[bool]

class WeeklyOffSchema(Schema):
    weekday: Literal['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    all_weeks: Optional[bool]
    second_week: Optional[bool]
    fifth_week: Optional[bool]
    alternate_weeks: Optional[bool]
    all_but_last: Optional[bool]
    third_week: Optional[bool]
    last_two_weeks: Optional[bool]
    first_week: Optional[bool]
    fourth_week: Optional[bool]
    last_week: Optional[bool]

class WeeklyOffOutSchema(Schema):
    organization: int
    weekday: str
    all_weeks: Optional[bool]
    second_week: Optional[bool]
    fifth_week: Optional[bool]
    alternate_weeks: Optional[bool]
    all_but_last: Optional[bool]
    third_week: Optional[bool]
    last_two_weeks: Optional[bool]
    first_week: Optional[bool]
    fourth_week: Optional[bool]
    last_week: Optional[bool]


class AllowedIPSchema(Schema):
    ip_address: str
    added_from_ip: Optional[str] = None

class AllowedIPOutSchema(Schema):
    organization: int
    ip_address: str
    addedby: Optional[int]
    addedon: Optional[datetime]
    added_from_ip: Optional[str]

class CompensationRulesSchema(Schema):
    daily_eligiibility: Optional[str]
    weekoff_eligiibility: Optional[str]
    holiday_eligiibility: Optional[str]
    daily_rule: Optional[Dict[str, Any]]
    weekoff_rule: Optional[Dict[str, Any]]
    holiday_rule: Optional[Dict[str, Any]]

class CompensationRulesOutSchema(Schema):
    organization: int
    daily_eligiibility: Optional[str]
    weekoff_eligiibility: Optional[str]
    holiday_eligiibility: Optional[str]
    daily_rule: Optional[Dict[str, Any]]
    weekoff_rule: Optional[Dict[str, Any]]
    holiday_rule: Optional[Dict[str, Any]]

class CompOffRulesSchema(Schema):
    daily_eligiibility: Optional[str]
    weekoff_eligiibility: Optional[str]
    holiday_eligiibility: Optional[str]
    daily_rule: Optional[Dict[str, Any]]
    weekoff_rule: Optional[Dict[str, Any]]
    holiday_rule: Optional[Dict[str, Any]]

class CompOffRulesOutSchema(Schema):
    organization: int
    daily_eligiibility: Optional[str]
    weekoff_eligiibility: Optional[str]
    holiday_eligiibility: Optional[str]
    daily_rule: Optional[Dict[str, Any]]
    weekoff_rule: Optional[Dict[str, Any]]
    holiday_rule: Optional[Dict[str, Any]]

class UnderTimeRuleSchema(Schema):
    eligiblity_hours: Optional[int]
    consider_absent: Optional[bool]
    conside_half_day: Optional[bool]

class UnderTimeRuleOutSchema(Schema):
    organization: int
    eligiblity_hours: Optional[int]
    consider_absent: Optional[bool]
    conside_half_day: Optional[bool]

    