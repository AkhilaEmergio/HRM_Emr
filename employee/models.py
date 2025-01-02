from django.db import models
from django.contrib.auth.models import AbstractUser

class Organization(models.Model):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True) 
    logo=models.FileField(upload_to='logos/',null=True,blank=True)

class UserProfile(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('employee', 'Employee')])
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, unique=True)
    employee_code=models.CharField(max_length=100)
    profile=models.FileField(upload_to='profiles/',null=True)
    reporting_manager = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='manager')
    business_unit=models.CharField(max_length=100,null=True)
    department=models.CharField(max_length=100,null=True)
    designation=models.CharField(max_length=100,null=True)
    date_of_joining=models.CharField(max_length=100,null=True)
    employment_type=models.CharField(max_length=100,null=True)
    service_status=models.CharField(max_length=100,null=True)
    workmode=models.CharField(max_length=100,null=True)
    probation=models.CharField(max_length=100,null=True)
    extension=models.CharField(max_length=100,null=True)
    notice_period=models.CharField(max_length=100,null=True)
    enrollment_no=models.CharField(max_length=50,null=True)
    trigger_onboarding=models.BooleanField(default=False,null=True)
    send_mail=models.BooleanField(default=True,null=True)
    weekly_offs=models.JSONField(null=True)
    total_hr_spend = models.FloatField(default=0.0)
    active_from = models.DateTimeField(null=True, blank=True)
    inactive_from = models.DateTimeField(null=True, blank=True)
    deactivate = models.BooleanField(default=False)
    deactivated_on = models.DateField(null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='userprofile_set',  # Custom related_name
        help_text='The groups this user belongs to.'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='userprofile_set',  # Custom related_name
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return f"{self.name} ({self.username})"

class PersonalDetail(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    fullname=models.JSONField()
    date_of_birth=models.DateField()
    place_of_birth=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    bloodgroup=models.CharField(max_length=100)
    domicile=models.CharField(max_length=100)
    citizenship=models.CharField(max_length=100)
    religion=models.CharField(max_length=100)
    marital_status=models.CharField(max_length=100)
    marriage_date=models.DateField(null=True)
    mobile=models.CharField(max_length=20)
    workphone=models.CharField(max_length=20,null=True)
    personal_email=models.CharField(max_length=100,null=True)
    linkedin=models.CharField(max_length=100,null=True)
    slackuser=models.CharField(max_length=100,null=True)
    permanent_address=models.TextField()
    present_address=models.TextField()
    drivinglicense=models.CharField(max_length=100,null=True)
    passport=models.CharField(max_length=100,null=True)
    Aadhar_number=models.CharField(max_length=100)
    pan=models.CharField(max_length=100,null=True)
    UAN=models.CharField(max_length=100,null=True)
    skills=models.CharField(max_length=100,null=True)
    previous_exp=models.CharField(max_length=100,null=True)
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"Personal Details of {self.user.name}"
    
class General(models.Model):
    company_name=models.CharField(max_length=255)
    company_logo=models.FileField(upload_to='logos/')
    website_url=models.CharField(max_length=100)
    email_id=models.CharField(max_length=100)
    employee_code=models.CharField(max_length=100)
    address=models.TextField(max_length=100)
    state=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)
    fax=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    timezone=models.CharField(max_length=100)

    def __str__(self):
        return self.company_name

class employee_setting(models.Model):
    pan=models.BooleanField(default=False,null=True)
    aadhar=models.BooleanField(default=False,null=True)
    job_history=models.BooleanField(default=False,null=True)
    education=models.BooleanField(default=False,null=True)
    family=models.BooleanField(default=False,null=True)
    access_control=models.CharField(max_length=100,null=True)

class Education(models.Model):
    degree=models.CharField(max_length=100)
    specialization=models.CharField(max_length=100)
    college=models.CharField(max_length=100)
    university=models.CharField(max_length=100)
    year_of_passing=models.CharField(max_length=100)
    gpa=models.CharField(max_length=100)
    document=models.FileField(upload_to='education/')
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return f"educational Details of {self.user.name}"

class Emergency(models.Model):
    name=models.CharField(max_length=100)
    relationship=models.CharField(max_length=100)
    dob=models.CharField(max_length=100,null=True)
    phone_number=models.CharField(max_length=20,null=True)
    occupation=models.CharField(max_length=100,null=True)
    phone_number=models.CharField(max_length=100)
    address=models.TextField()
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"emergency Details of {self.user.name}"
    
class Family(models.Model):
    name=models.CharField(max_length=100)
    relationship=models.CharField(max_length=100)
    date_of_birth=models.DateField()
    gender=models.CharField(max_length=100)
    occupation=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    address=models.TextField()
    isdependent=models.BooleanField(default=False)
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"family details of {self.user.name}"
    
class Jobhistory(models.Model):
    employer=models.CharField(max_length=100)
    job_title=models.CharField(max_length=100)
    employee_code=models.CharField(max_length=100,null=True)
    joining_date=models.DateField()
    relieving_date=models.DateField()
    last_CTC=models.CharField(max_length=100)
    reason=models.TextField(null=True)
    document=models.FileField(upload_to='job/',null=True)
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"jobhistory of {self.user.name}"
    
class References(models.Model):
    name=models.CharField(max_length=100)
    jobtitle=models.CharField(max_length=100)
    company=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    mobile_no=models.CharField(max_length=100)
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"references of {self.user.name}"
    
class Bank(models.Model):
    name_of_bank=models.CharField(max_length=100)
    account_no=models.CharField(max_length=100)
    IFSC=models.CharField(max_length=50)
    branch=models.CharField(max_length=100)
    account_type=models.CharField(max_length=100)
    payment_mode=models.CharField(max_length=100) 
    document=models.FileField(upload_to='bank/',null=True)
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"bank details of {self.user.name}"



