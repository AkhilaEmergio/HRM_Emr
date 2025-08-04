from django.db import models
from django.contrib.auth import get_user_model
from user.models import Organization

User = get_user_model()

def default_generally_showable_fields():
    return {
        "email": False,
        "employee_status": False,
        "profile_image": False
    }

def default_officially_showable_fields():
    return {
        "employee_code": False,
        "department": False,
        "designation": False,
        "location": False,
        "joining_date": False,
        "reporting_manager": False
    }

def default_contacts_showable_fields():
    return {
        "mobile": False,
        "address": False,
        "email": False,
        "linked": False
    }

def default_other_showable_fields():
    return {
        "about_me": False,
        "skills": False,
        "attendance_status": False,
        "employment_type": False,
        "service_status": False
    }

def default_mandatory_inputable_fields():
    return {
        "job_history": False,
        "education_details": False,
        "family_details": False,
        "bank_details": False,
        "documents": False,
        "emergency_contact": False,
        "certifications": False,
        "profile_image": False
    }


class EmployeeProfileSettings(models.Model):
    manage_employee_profile = models.CharField(max_length=50, choices=[('allowed', 'allowed'), ('limited', 'limited'), ('blocked', 'blocked')])
    unique_fields = models.JSONField()
    employee_skills = models.CharField(max_length=50, choices=[('1-3', '1-3'), ('1-5', '1-5'), ('1-10', '1-10'), ('custom', 'custom')])
    custom_skills = models.JSONField(null=True, blank=True)
    approve_required = models.BooleanField(default=False)
    employees_addable = models.BooleanField(default=False)
    filter_search = models.BooleanField(default=False) ## Show only active employees
    generally_showable_fields = models.JSONField(default=default_generally_showable_fields)
    officially_showable_fields = models.JSONField(default=default_officially_showable_fields)
    contacts_showable_fields = models.JSONField(default=default_contacts_showable_fields)
    other_showable_fields = models.JSONField(default=default_other_showable_fields)
    mandatory_inputable_fields = models.JSONField(default=default_mandatory_inputable_fields)

    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="employee_profile_updated_by")



class DocumentSetting(models.Model):
    title = models.CharField(max_length=50)
    module = models.CharField(max_length=50)
    description = models.TextField()
    applicable_to = models.CharField(max_length=50)
    no_of_document = models.IntegerField()
    expiry_date = models.BooleanField()
    mandatory = models.BooleanField()
    identification = models.BooleanField()
    issue_date = models.BooleanField()
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="updated_by")
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)