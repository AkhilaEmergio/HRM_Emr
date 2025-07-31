from django.contrib import admin
from settings.employee_settings.models import *
from settings.attendance_settings.models import *
from settings.general_settings.models import *

# Register your models here.

admin.site.register(EmployeeProfileSettings)
admin.site.register(DocumentSetting)
admin.site.register(AttendaceSettings)
admin.site.register(RegularizationPolicies)
admin.site.register(WeeklyOff)
admin.site.register(Shift)
admin.site.register(RosterShiftSettings)
admin.site.register(ShiftChangeSettings)
admin.site.register(SandwichRulesSettings)
admin.site.register(TimeManagementPolicy)
admin.site.register(CalculationPolicy)
admin.site.register(AllowedIP)
admin.site.register(CompOffRules)
admin.site.register(CompensationRules)
admin.site.register(EmployeeSettings)
admin.site.register(DepartmentSettings)
admin.site.register(BandsSettings)
admin.site.register(BusinessUnitSettings)
admin.site.register(DesignationSettings)
admin.site.register(BillingSettings)
