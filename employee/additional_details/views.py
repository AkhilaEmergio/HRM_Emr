from ninja import PatchDict, Router
from django.contrib.auth import get_user_model
from .schema import *
from typing import *
from employee.basic_details.models import *
from employee.additional_details.models import *
from user import *
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

employee_additional_api = Router(tags=['employee_additional'])
User = get_user_model()

# Education endpoints
@employee_additional_api.post("/education", response={201: EducationSchema, 400: Message})
async def add_education(request, employee_id: int, data: EducationInputSchema):
    try:
        employee = await sync_to_async(Employee.objects.get)(id=employee_id)
        education = await sync_to_async(Education.objects.create)(
            employee=employee,
            **data.dict()
        )
        return 201, EducationSchema.from_orm(education)
    except Exception as e:
        return 400, {"message": str(e)}

@employee_additional_api.get("/education", response={200: List[EducationSchema], 404: Message})
async def get_education(request, employee_id: int):
    try:
        education_list = await sync_to_async(list)(
            Education.objects.filter(employee_id=employee_id)
        )
        return 200, [EducationSchema.from_orm(edu) for edu in education_list]
    except Exception as e:
        return 404, {"message": str(e)}

@employee_additional_api.put("/education/{id}", response={200: EducationSchema, 404: Message})
async def update_education(request, id: int, data: EducationInputSchema):
    try:
        education = await sync_to_async(Education.objects.get)(id=id)
        for key, value in data.dict().items():
            setattr(education, key, value)
        await sync_to_async(education.save)()
        return 200, EducationSchema.from_orm(education)
    except Education.DoesNotExist:
        return 404, {"message": "Education record not found"}

@employee_additional_api.delete("/education/{id}", response={200: Message, 404: Message})
async def delete_education(request, id: int):
    try:
        education = await sync_to_async(Education.objects.get)(id=id)
        await sync_to_async(education.delete)()
        return 200, {"message": "Education record deleted successfully"}
    except Education.DoesNotExist:
        return 404, {"message": "Education record not found"}

# File upload endpoint for education documents
@employee_additional_api.post("/education/{id}/upload", response={200: Message, 404: Message})
async def upload_education_document(request, id: int):
    try:
        education = await sync_to_async(Education.objects.get)(id=id)
        data = await request.form()
        file = data.get('document')
        if file:
            education.document = file
            await sync_to_async(education.save)()
            return 200, {"message": "Document uploaded successfully"}
        return 400, {"message": "No document provided"}
    except Education.DoesNotExist:
        return 404, {"message": "Education record not found"}
    
# @employee_additional_api.get("/skills", response={200: List[], 404: Message})
# async def get_education(request, employee_id: int):
#     try:
#         education_list = await sync_to_async(list)(
#             Education.objects.filter(employee_id=employee_id)
#         )
#         return 200, [EducationSchema.from_orm(edu) for edu in education_list]
#     except Exception as e:
#         return 404, {"message": str(e)}