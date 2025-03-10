from django.db import models

# Create your models here.

class AttendaceSettings(models.Model):
    ATTENDANCE_STATUS_CHOICES = [
        ("absent", "Absent"),
        ("present", "Present")
    ]
    enable_attendance = models.BooleanField(default=True)
    default_attendance_status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS_CHOICES, default="absent",)
    deduct_salary_for_absent_days = models.CharField(max_length=20, default="yes")
    company_start_time = models.TimeField()
    company_end_time = models.TimeField()
    hide_total_hours = models.BooleanField(default=False)
    hide_attendance_punches = models.BooleanField(default=False)
    disable_web_attendance = models.BooleanField(default=False)
    enable_ip_restrictions = models.BooleanField(default=False)
    disable_mobile_attendance = models.BooleanField(default=False)

class RosterShiftSettings(models.Model):
    enable_roster_shifts = models.BooleanField(default=False)
    allow_managers_assign_shifts = models.BooleanField(default=False)
    restrict_shift_change_days = models.PositiveIntegerField(default=0)
    restrict_week_off_per_month = models.PositiveIntegerField(default=1)
    restrict_week_off_per_week = models.PositiveIntegerField(default=1)

class ShiftChangeSettings(models.Model):
    approval_status_choices = [
        ("Manager Approved", "Manager Approved"),
        ("Approved", "Approved"),
    ]
    allow_employee_shift_change_request = models.BooleanField(default=False)
    enable_manager_approval = models.BooleanField(default=False)
    default_approval_status = models.CharField(max_length=20,choices=approval_status_choices,default="Pending")

class SandwichRulesSettings(models.Model):
    enable_sandwich_rules = models.BooleanField(default=False)
    week_off_holidays_between_absents = models.BooleanField(default=False)
    week_off_holidays_after_absent = models.BooleanField(default=False)
    week_off_holidays_before_absent = models.BooleanField(default=False)
    absent_week_offs_holidays_beginning_month = models.BooleanField(default=False)
    absent_week_offs_holidays_end_month = models.BooleanField(default=False)

class RegularizationPolicies(models.Model):
    PUNCH_APPROVAL_CHOICES = [
        ("Manager Approved", "Manager Approved"),
        ("Approved", "Approved"),
    ]
    enable_justify_punch = models.BooleanField(default=False)
    restrict_attendance_justification_days = models.IntegerField(default=0)
    enable_request_punch = models.BooleanField(default=False)
    enable_multiple_punches = models.BooleanField(default=False)
    restrict_punch_request_days = models.IntegerField(default=0)
    punch_approval_status = models.CharField(max_length=20, choices=PUNCH_APPROVAL_CHOICES, default="Manager Approved")
    # Restrictions for Employee Attendance Actions
    restrict_duty_punch_employee = models.IntegerField(default=0)
    restrict_real_time_justify_employee = models.IntegerField(default=0)
    # Restrictions for Manager Attendance Actions
    restrict_punch_request_manager = models.IntegerField(default=0)
    restrict_attendance_approval_manager = models.IntegerField(default=0)
    restrict_late_justify_manager = models.IntegerField(default=0)
    restrict_early_exit_justify_manager = models.IntegerField(default=0)
    restrict_total_time_justify_manager = models.IntegerField(default=0)

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
    enable_overtime = models.BooleanField(default=False)   
    overtime_approval_status = models.CharField(max_length=20, choices=OVERTIME_APPROVAL_CHOICES, default="Manager Approved")
    round_off_minutes = models.BooleanField(default=False)
    rounding_method = models.CharField(max_length=20, choices=ROUNDING_OPTIONS, default="Standard")
    rounding_value = models.IntegerField(default=1)
    convert_overtime_to_compensation = models.BooleanField(default=False)
    comp_off_request_on_overtime = models.BooleanField(default=False)
    default_overtime_rule = models.CharField(max_length=20, choices=DEFAULT_RULES_CHOICES, default="Compensation")
    enable_undertime = models.BooleanField(default=False)
    enable_attendance_rules = models.BooleanField(default=False)

class CalculationPolicy(models.Model):
    enable_attendance_unit = models.BooleanField(default=False)
    number_of_unit_for_absent = models.IntegerField(default=1)
    deduct_break_hours = models.BooleanField(default=False)   
    daily_auto_attendance_calculation = models.BooleanField(default=True)
    enable_leave_based_rules = models.BooleanField(default=True)
    auto_assign_shift = models.BooleanField(default=False)
  

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

    weekday = models.CharField(max_length=10, choices=WEEKDAYS)
    all_weeks = models.BooleanField(default=False)
    second_week = models.BooleanField(default=False)
    fifth_week = models.BooleanField(default=False)
    alternate_weeks = models.BooleanField(default=False)
    all_but_last = models.BooleanField(default=False)
    third_week = models.BooleanField(default=False)
    last_two_weeks = models.BooleanField(default=False)
    first_week = models.BooleanField(default=False)
    fourth_week = models.BooleanField(default=False)
    last_week = models.BooleanField(default=False)

    def __str__(self):
        return f"Weekly Off on {self.weekday}"


      

    


