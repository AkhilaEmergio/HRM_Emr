from django.db import models
from django.contrib.auth import get_user_model
from settings.general_settings.models import *

User = get_user_model()

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE,null=True,blank=True,related_name='User')
    created_by = models.ForeignKey(User, on_delete = models.CASCADE,null=True,blank=True,related_name='employee_created')
    employee_code = models.CharField(max_length=100)
    profile = models.FileField(upload_to='profiles/',null=True)
    reporting_manager = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True, related_name='manager')
    business_unit = models.ForeignKey(BusinessUnitSettings, on_delete = models.CASCADE)
    department = models.ForeignKey(DepartmentSettings, on_delete = models.CASCADE)
    designation = models.ForeignKey(DesignationSettings, on_delete = models.CASCADE)
    date_of_joining = models.CharField(max_length=100,null=True)
    employment_type = models.CharField(max_length=100,null=True)
    service_status = models.CharField(max_length=100,null=True)
    workmode = models.CharField(max_length=100,null=True)
    probation = models.CharField(max_length=100,null=True)
    extension = models.CharField(max_length=100,null=True)
    notice_period = models.CharField(max_length=100,null=True)
    enrollment_no = models.CharField(max_length=50,null=True)
    trigger_onboarding = models.BooleanField(default=False,null=True)
    send_mail = models.BooleanField(default=True,null=True)
    weekly_offs = models.JSONField(null=True)
    permissions = models.JSONField(null=True)

    def __str__(self):
        return f"{self.name} ({self.username})"

class PersonalDetail(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    fullname = models.JSONField()
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    bloodgroup = models.CharField(max_length=100)
    domicile = models.CharField(max_length=100)
    citizenship = models.CharField(max_length=100)
    religion = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=100)
    marriage_date = models.DateField(null=True)
    workphone = models.CharField(max_length=20,null=True)
    personal_email = models.CharField(max_length=100,null=True)
    linkedin = models.CharField(max_length=100,null=True)
    slackuser = models.CharField(max_length=100,null=True)
    permanent_address = models.TextField()
    present_address = models.TextField()
    drivinglicense = models.CharField(max_length=100,null=True)
    passport = models.CharField(max_length=100,null=True)
    aadhar_number = models.CharField(max_length=100)
    pan = models.CharField(max_length=100,null=True)
    uan = models.CharField(max_length=100,null=True)
    skills = models.JSONField(null=True, blank=True)
    total_experiance = models.IntegerField(null=True)

    def __str__(self):
        return f"Personal Details of {self.employee.user.name}"