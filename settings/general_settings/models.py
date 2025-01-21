from django.db import models
from employee.basic_details.models import *
from django.contrib.auth import get_user_model
from user.models import Organization

User = get_user_model()

class EmployeeSettings(models.Model):
    created=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='emp_created')
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    pan=models.BooleanField(default=False,null=True)
    aadhar=models.BooleanField(default=False,null=True)
    job_history=models.BooleanField(default=False,null=True)
    education=models.BooleanField(default=False,null=True)
    family=models.BooleanField(default=False,null=True)
    access_control=models.CharField(max_length=100,null=True)

class DepartmentSettings(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, blank=True,)
    department_head = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="departments_head")
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="departments_updated_by")
    created_on = models.DateTimeField(auto_now=True)

class DesignationSettings(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, blank=True)
    rank = models.CharField(max_length=50, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,related_name="designations_updated_by")
    created_on = models.DateTimeField(auto_now=True)

class BandsSettings(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    rank = models.CharField(max_length=50, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,related_name="bands_updated"  )
    created_on = models.DateTimeField(auto_now=True)

class BusinessUnitSettings(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, blank=True)
    unit_head = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,related_name="business_units_headed")
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,related_name="business_units_updated")
    created_on = models.DateTimeField(auto_now=True)

class BillingSettings(models.Model):
    name = models.CharField(max_length=100)
    address=models.JSONField()
    gstin = models.CharField(max_length=100, null=True)
    pan = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    created_on = models.DateTimeField(auto_now=True)