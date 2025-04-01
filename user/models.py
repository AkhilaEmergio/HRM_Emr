from django.db import models
from django.contrib.auth.models import AbstractUser

class Organization(models.Model):
    organization_name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True) 
    organisation_code = models.CharField(max_length=255)
    logo = models.FileField(upload_to='logos/',null=True,blank=True)
    address = models.JSONField()
    fax = models.CharField(max_length=100)
    timezone=models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now=True)

class UserProfile(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('employee', 'Employee'),('superadmin','Superadmin')])
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, unique=True)