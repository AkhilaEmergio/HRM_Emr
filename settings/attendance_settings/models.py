from django.db import models
from user.models import Organization,UserProfile

# Create your models here.

class AttendaceSettings(models.Model):
    ATTENDANCE_STATUS_CHOICES = [
        ("absent", "Absent"),
        ("present", "Present")
    ]
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    enable_attendance = models.BooleanField(default=True,null=True)
    default_attendance_status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS_CHOICES, default="absent",null=True)
    deduct_salary_for_absent_days = models.CharField(max_length=20, default="yes",null=True)
    company_start_time = models.TimeField(null=True)
    company_end_time = models.TimeField(null=True)
    hide_total_hours = models.BooleanField(default=False,null=True)
    hide_attendance_punches = models.BooleanField(default=False,null=True)
    disable_web_attendance = models.BooleanField(default=False,null=True)
    enable_ip_restrictions = models.BooleanField(default=False,null=True)
    disable_mobile_attendance = models.BooleanField(default=False,null=True)

class RosterShiftSettings(models.Model):
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    enable_roster_shifts = models.BooleanField(default=False,null=True)
    allow_managers_assign_shifts = models.BooleanField(default=False,null=True)
    restrict_shift_change_days = models.PositiveIntegerField(default=0,null=True)
    restrict_week_off_per_month = models.PositiveIntegerField(default=1,null=True)
    restrict_week_off_per_week = models.PositiveIntegerField(default=1,null=True)

class ShiftChangeSettings(models.Model):
    approval_status_choices = [
        ("Manager Approved", "Manager Approved"),
        ("Approved", "Approved"),
    ]
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    allow_employee_shift_change_request = models.BooleanField(default=False,null=True)
    enable_manager_approval = models.BooleanField(default=False,null=True)
    default_approval_status = models.CharField(max_length=20,choices=approval_status_choices,default="Pending",null=True)

class SandwichRulesSettings(models.Model):
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    enable_sandwich_rules = models.BooleanField(default=False,null=True)
    week_off_holidays_between_absents = models.BooleanField(default=False,null=True)
    week_off_holidays_after_absent = models.BooleanField(default=False,null=True)
    week_off_holidays_before_absent = models.BooleanField(default=False,null=True)
    absent_week_offs_holidays_beginning_month = models.BooleanField(default=False,null=True)
    absent_week_offs_holidays_end_month = models.BooleanField(default=False,null=True)

class RegularizationPolicies(models.Model):
    PUNCH_APPROVAL_CHOICES = [
        ("Manager Approved", "Manager Approved"),
        ("Approved", "Approved"),
    ]
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    enable_justify_punch = models.BooleanField(default=False, null=True)
    restrict_attendance_justification_days = models.IntegerField(default=0, null=True)
    enable_request_punch = models.BooleanField(default=False, null=True)
    enable_multiple_punches = models.BooleanField(default=False, null=True)
    restrict_punch_request_days = models.IntegerField(default=0, null=True)
    punch_approval_status = models.CharField(max_length=20, choices=PUNCH_APPROVAL_CHOICES, default="Manager Approved",null=True)
    # Restrictions for Employee Attendance Actions
    restrict_duty_punch_employee = models.IntegerField(default=0, null=True)
    restrict_real_time_justify_employee = models.IntegerField(default=0, null=True)
    # Restrictions for Manager Attendance Actions
    restrict_punch_request_manager = models.IntegerField(default=0, null=True)
    restrict_attendance_approval_manager = models.IntegerField(default=0, null=True)
    restrict_late_justify_manager = models.IntegerField(default=0, null=True)
    restrict_early_exit_justify_manager = models.IntegerField(default=0, null=True)
    restrict_total_time_justify_manager = models.IntegerField(default=0, null=True)

class TimeManagementPolicy(models.Model):
    OVERTIME_APPROVAL_CHOICES = [
        ("Manager Approved", "Manager Approved"),
        ("Approved", "Approved"),
    ]
    ROUNDING_OPTIONS = [
        ("Standard", "Standard"),
        ("Ceiling", "Ceiling"),
        ("Floor", "Floor"),
        ("No_Round_Off", "No Round Off"),
    ]
    DEFAULT_RULES_CHOICES = [
        ("Compensation", "Convert Approved Overtime into Compensation"),
        ("CompOff", "Automatically raise CompOff request"),
    ]
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    enable_overtime = models.BooleanField(default=False,null=True)   
    overtime_approval_status = models.CharField(max_length=20, choices=OVERTIME_APPROVAL_CHOICES, default="Manager Approved",null=True)
    round_off_minutes = models.BooleanField(default=False,null=True)
    rounding_method = models.CharField(max_length=20, choices=ROUNDING_OPTIONS, default="Standard",null=True)
    rounding_value = models.IntegerField(default=1,null=True)
    convert_overtime_to_compensation = models.BooleanField(default=False,null=True)
    comp_off_request_on_overtime = models.BooleanField(default=False,null=True)
    default_overtime_rule = models.CharField(max_length=20, choices=DEFAULT_RULES_CHOICES, default="Compensation",null=True)
    enable_undertime = models.BooleanField(default=False,null=True)
    enable_attendance_rules = models.BooleanField(default=False,null=True)

class CalculationPolicy(models.Model):
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    enable_attendance_unit = models.BooleanField(default=False)
    number_of_unit_for_absent = models.IntegerField(default=1,null=True)
    deduct_break_hours = models.BooleanField(default=False,null=True)   
    daily_auto_attendance_calculation = models.BooleanField(default=True,null=True)
    enable_leave_based_rules = models.BooleanField(default=True,null=True)
    auto_assign_shift = models.BooleanField(default=False,null=True)
  

class WeeklyOff(models.Model):
    WEEKDAYS = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    weekday = models.CharField(max_length=10, choices=WEEKDAYS)
    all_weeks = models.BooleanField(default=False,null=True)
    second_week = models.BooleanField(default=False,null=True)
    fifth_week = models.BooleanField(default=False,null=True)
    alternate_weeks = models.BooleanField(default=False,null=True)
    all_but_last = models.BooleanField(default=False,null=True)
    third_week = models.BooleanField(default=False,null=True)
    last_two_weeks = models.BooleanField(default=False,null=True)
    first_week = models.BooleanField(default=False,null=True)
    fourth_week = models.BooleanField(default=False,null=True)
    last_week = models.BooleanField(default=False,null=True)

    def __str__(self):
        return f"Weekly Off on {self.weekday}"


class AllowedIP(models.Model):
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    ip_address = models.CharField(max_length=100,null=True)
    addedby = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True,blank=True,related_name='ip_added_by')
    addedon = models.DateTimeField(auto_now_add=True,null=True)
    added_from_ip = models.CharField(max_length=100, null=True, blank=True)


class CompensationRules(models.Model):
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    daily_eligiibility = models.CharField(max_length=100,null=True)
    weekoff_eligiibility = models.CharField(max_length=100,null=True)
    holiday_eligiibility = models.CharField(max_length=100,null=True)
    daily_rule=models.JSONField(null=True)
    weekoff_rule=models.JSONField(null=True)
    holiday_rule=models.JSONField(null=True)

class CompOffRules(models.Model):
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    daily_eligiibility = models.CharField(max_length=100,null=True)
    weekoff_eligiibility = models.CharField(max_length=100,null=True)
    holiday_eligiibility = models.CharField(max_length=100,null=True)
    daily_rule=models.JSONField(null=True)
    weekoff_rule=models.JSONField(null=True)
    holiday_rule=models.JSONField(null=True)

class UnderTimeRule(models.Model):
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    eligiblity_hours = models.IntegerField(null=True)
    consider_absent=models.BooleanField(default=False,null=True)
    conside_half_day=models.BooleanField(default=False,null=True)

class Shift(models.Model):
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    shift_type=models.CharField(max_length=100,choices=[('Fixed','Fixed'),('Flexible','Flexible')],null=True)
    shift_code=models.CharField(max_length=100,null=True)
    shift_title=models.CharField(max_length=100,null=True)
    description=models.TextField(null=True)
    timein=models.TimeField(null=True)
    timeout=models.TimeField(null=True)
    make_default_shift=models.BooleanField(default=False,null=True)

    


