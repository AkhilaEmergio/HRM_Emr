from django.db import models
from employee.models import *


# Create your models here.
class Department(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True)
    department_head = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True,related_name="departments_headed")
    updated_by = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True,related_name="departments_updated"   )


class Designation(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True)
    rank = models.CharField(max_length=50, null=True)
    updated_by = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True,related_name="designations_updated")


class Bands(models.Model):
    title = models.CharField(max_length=50)
    rank = models.CharField(max_length=50, null=True)
    updated_by = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True,related_name="bands_updated"  )


class BusinessUnit(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True)
    unit_head = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True,related_name="business_units_headed")
    updated_by = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True,related_name="business_units_updated")


class BillingDetails(models.Model):
    name=models.CharField(max_length=100)
    Address=models.JSONField()
    GSTIN=models.CharField(max_length=100,null=True)
    PAN=models.CharField(max_length=100,null=True)
    country=models.CharField(max_length=100,null=True)
    updated_by=models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)