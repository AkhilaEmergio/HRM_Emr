from django.contrib import admin
from employee.basic_details.models import *
from employee.additional_details.models import *
# Register your models here.

admin.site.register(Education)
admin.site.register(Bank)
admin.site.register(Emergency)
admin.site.register(References)
admin.site.register(Family)
admin.site.register(Jobhistory)
admin.site.register(Employee)
admin.site.register(PersonalDetail) 