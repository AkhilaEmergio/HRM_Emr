from ninja import PatchDict, Router
from django.contrib.auth import get_user_model
from employee.basic_details.schema import *
from typing import *
from employee.basic_details.models import *
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
from .models import Attendance
from .schema import *

attendance_api = Router(tags=['attendance'])
user=get_user_model()

# Employee attendance endpoints
@attendance_api.post("/attendance", response={201: Attendance, 400: Message})
async def add_attendance(request, data: Attendance ):
    user = request.auth
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        try:
            attendance = await sync_to_async(Attendance.objects.create)(**data.dict(),user=user )
            return 201, Attendance.from_orm(attendance)
        except Exception as e:
            return 400, {"message": str(e)}
    return 400, {"message": "Unauthorized or organization not found"}
