from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(AttendaceSettings)
admin.site.register(RegularizationPolicies)
admin.site.register(WeeklyOff)
admin.site.register(Shift)
admin.site.register(RosterShiftSettings)
admin.site.register(ShiftChangeSettings)
admin.site.register(SandwichRulesSettings)
admin.site.register(TimeManagementPolicy)
admin.site.register(CalculationPolicy)
admin.site.register(WeeklyOff)
admin.site.register(AllowedIP)
admin.site.register(CompOffRules)
admin.site.register(CompensationRules)
