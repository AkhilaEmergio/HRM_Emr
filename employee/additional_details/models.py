from django.db import models
from django.contrib.auth import get_user_model
from employee.basic_details.models import Employee

User = get_user_model()

class Education(models.Model):
    employee = models.ForeignKey(Employee,on_delete = models.CASCADE,null=True)
    degree = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    college = models.CharField(max_length=100)
    university = models.CharField(max_length=100, null=True, blank=True)
    year_of_passing = models.CharField(max_length=100)
    gpa = models.CharField(max_length=100, null=True, blank=True)
    document = models.FileField(upload_to='education/', null=True, blank=True)
    
    def __str__(self):
        return f"Educational Details of {self.employee.user.name}"

class Emergency(models.Model):
    employee = models.ForeignKey(Employee,on_delete = models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    dob = models.CharField(max_length=100,null=True)
    occupation = models.CharField(max_length=100,null=True)
    phone_number = models.CharField(max_length=10)
    address = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"emergency Details of {self.employee.user.name}"

class Family(models.Model):
    employee = models.ForeignKey(Employee, on_delete = models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    relationship = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    address = models.JSONField(null=True, blank=True)
    isdependent = models.BooleanField(default=False)

    def __str__(self):
        return f"family details of {self.employee.user.name}"

class Jobhistory(models.Model):
    employee = models.ForeignKey(Employee,on_delete = models.CASCADE,null=True)
    employer = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    employee_code = models.CharField(max_length=100,null=True)
    joining_date = models.DateField()
    relieving_date = models.DateField()
    last_CTC = models.CharField(max_length=100)
    reason = models.TextField(null=True)
    document = models.FileField(upload_to='job/',null=True)

    def __str__(self):
        return f"jobhistory of {self.employee.user.name}"

class References(models.Model):
    employee = models.ForeignKey(Employee,on_delete = models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=100)

    def __str__(self):
        return f"references of {self.employee.user.name}"

class Bank(models.Model):
    employee = models.ForeignKey(Employee,on_delete = models.CASCADE,null=True)
    name_of_bank = models.CharField(max_length=100)
    account_no = models.CharField(max_length=100)
    ifsc = models.CharField(max_length=50)
    branch = models.CharField(max_length=100, null=True, blank=True)
    account_type = models.CharField(max_length=100)
    payment_mode = models.CharField(max_length=100, null=True, blank=True) 
    document = models.FileField(upload_to='bank/', null=True, blank=True)

    def __str__(self):
        return f"Bank details of {self.employee.user.name}"