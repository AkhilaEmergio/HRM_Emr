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
        is_superuser=True,  # First user is superuser
    )
    
    # Set password (don't forget to hash it)
    user.set_password(user_data.password)
    user.save()

    return ({"message": "Organization and first user created successfully."})