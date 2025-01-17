from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class EmployeeProfileSettings(models.Model):
    manage_employee_profile = models.CharField(max_length=50, choices=[('allowed', 'allowed'), ('limited', 'limited'), ('blocked', 'blocked')])
    unique_fields = models.JSONField()
    employee_skills = models.CharField(max_length=50, choices=[('1-3', '1-3'), ('1-5', '1-5'), ('1-10', '1-10'), ('custom', 'custom')])
    custom_skills = models.JSONField(null=True, blank=True)
    approve_required = models.BooleanField(default=False)
    employees_addable = models.BooleanField(default=False)
    filter_search = models.BooleanField(default=False) ## Show only active employees
    generally_showable_fields = models.JSONField(default={"email": False, "employee_status": False, "profile_image":False})
    officially_showable_fields = models.JSONField(default={"employee_code": False, "department": False, "designation":False,
        "location": False, "joining_date": False, "reporting_manager": False})
    contacts_showable_fields = models.JSONField(default={"mobile": False, "address": False, "email":False, "linked": False})
    other_showable_fields = models.JSONField(default={"about_me": False, "skills": False, "attendance_status":False,
        "employment_type": False, "service_status": False})
    mandatory_inputable_fields = models.JSONField(default={"job_history": False, "education_details": False, "family_details": False,
        "bank_details": False, "documents": False, "emergency_contact": False, "certifications": False, "profile_image":False})
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="updated")

class DocumentSetting(models.Model):
    title = models.CharField(max_length=50)
    module = models.CharField(max_length=50,choices=[('payroll','payrole'),('generic','generic') ])
    description = models.TextField()
    applicable_to = models.CharField(max_length=50,choices=[('anyone','anyone'),('employee','employee'),('admin','admin')])
    no_of_document = models.IntegerField()
    expiry_date = models.BooleanField()
    mandatory = models.BooleanField()
    identification = models.BooleanField()
    issue_date = models.BooleanField()
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="updated_by")


