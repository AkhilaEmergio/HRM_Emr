from ninja import PatchDict, Router
from django.contrib.auth import get_user_model
from organization.schema import *
from typing import *
from employee.models import *
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
from ninja.responses import codes_4xx
from ninja_jwt.authentication import AsyncJWTAuth
from asgiref.sync import sync_to_async
from ninja_jwt.tokens import RefreshToken, AccessToken
from ninja_jwt.tokens import RefreshToken
from ninja.errors import HttpError

org_api = Router(tags=['organization'])
User = get_user_model()

@org_api.post("/create_organization_and_user")
def create_organization_and_user(request, org_data: OrganizationSchema, user_data: UserProfileSchema):
    # Create organization
    org = Organization.objects.create(
        name=org_data.name,
        domain=org_data.domain,
        logo=org_data.logo,
        address=org_data.address
    )
    
    # Create the first user
    user = UserProfile.objects.create(
        username=user_data.username,
        email=user_data.email,
        name=user_data.name,
        phone=user_data.phone,
        organization=org,
        role=user_data.role,
        is_staff=True,  # First user is an admin
    )

    
    # Set password (don't forget to hash it)
    user.set_password(user_data.password)
    user.save()
    employee = Employee.objects.create(
        user=user,
        created_by=user,  
        employee_code=f"EMP-{user.id:05}",  
        business_unit="Default Unit",  
        department="Default Department",  
        designation="Admin",  
        date_of_joining="2025-01-01", 
        employment_type="Full-Time",  
        service_status="Active",  
        workmode="On-Site",  
        probation="No",  
        extension="No",  
        notice_period="30 Days",  
        enrollment_no=f"ENR-{user.id:05}",  
        trigger_onboarding=True, 
        send_mail=True,  
        weekly_offs=["Saturday", "Sunday"]
    )
    

    return ({"message": "Organization and first user created successfully."})