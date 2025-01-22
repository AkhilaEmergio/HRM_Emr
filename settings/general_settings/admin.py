from django.contrib import admin
from settings.general_settings.models import *

# Register your models here.

admin.site.register(EmployeeSettings)
admin.site.register(DepartmentSettings)
admin.site.register(BandsSettings)
admin.site.register(BusinessUnitSettings)
admin.site.register(DesignationSettings)
admin.site.register(BillingSettings)