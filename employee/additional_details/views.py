from ninja import File, Router
from ninja.files import UploadedFile
from typing import List
from employee.additional_details.models import *
from employee.additional_details.schema import *
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async

employee_additional_api = Router()

# EDUCATION
@employee_additional_api.post("/education", response={201: EducationSchema, 400: dict})
async def create_education(request, data: EducationSchema, document: Optional[UploadedFile] =File(None) ):
    user = request.auth
    try:
        employee = await sync_to_async(Employee.objects.get)(user=user)

        # ensure employee is not duplicated in data
        data_dict = data.dict()
        data_dict.pop("employee", None)

        education = await sync_to_async(Education.objects.create)(
            employee=employee,   # ✅ use object
            **data_dict
        )
        if document:
            education.document = document
            await sync_to_async(education.save)()

        return 201, EducationSchema.from_orm(education)

    except Employee.DoesNotExist:
        return 400, {"message": "Employee profile not found"}
    except Exception as e:
        return 400, {"message": str(e)}



@employee_additional_api.get("/education", response={200: List[EducationSchema], 404: dict})
async def get_education(request):
    user = request.auth
    try:
        employee = await sync_to_async(Employee.objects.get)(user=user)
        # ✅ safe: select_related if you want employee details
        education = await sync_to_async(list)(
            Education.objects.filter(employee=employee)
        )
        return 200, [EducationSchema.from_orm(e) for e in education]
    except Employee.DoesNotExist:
        return 404, {"message": "Employee profile not found"}

# EMERGENCY
@employee_additional_api.post("/emergency", response={201: EmergencySchema, 400: dict})
async def create_emergency(request, data: EmergencySchema):
    user = request.auth
    try:
        employee = await sync_to_async(Employee.objects.get)(user=user)
        emergency = await sync_to_async(Emergency.objects.create)(
            employee=employee,  # Django expects instance
            **data.dict(exclude={"employee"})  # prevent duplicate key
        )
        return 201, EmergencySchema.from_orm(emergency)
    except Employee.DoesNotExist:
        return 400, {"message": "Employee profile not found"}


@employee_additional_api.get("/emergency", response={200: List[EmergencySchema], 404: dict})
async def get_emergency(request):
    user = request.auth
    try:
        employee = await sync_to_async(Employee.objects.get)(user=user)
        emergency = await sync_to_async(list)(Emergency.objects.filter(employee=employee))
        return 200, [EmergencySchema.from_orm(e) for e in emergency]
    except Employee.DoesNotExist:
        return 404, {"message": "Employee profile not found"}

# FAMILY
@employee_additional_api.post("/family", response={201: FamilySchema, 400: dict})
async def create_family(request, data: FamilySchema):
    user = request.auth
    try:
        employee = await sync_to_async(Employee.objects.get)(user=user)
        family = await sync_to_async(Family.objects.create)(
            employee=employee,
            **data.dict(exclude={"employee"})  # prevent duplicate employee field
        )
        return 201, FamilySchema.from_orm(family)
    except Employee.DoesNotExist:
        return 400, {"message": "Employee profile not found"}


@employee_additional_api.get("/family", response={200: List[FamilySchema], 404: dict})
async def get_family(request):
    user = request.auth
    try:
        employee = await sync_to_async(Employee.objects.get)(user=user)
        family = await sync_to_async(list)(Family.objects.filter(employee=employee))
        return 200, [FamilySchema.from_orm(f) for f in family]
    except Employee.DoesNotExist:
        return 404, {"message": "Employee profile not found"}

# JOB HISTORY
@employee_additional_api.post("/jobhistory", response={201: JobhistorySchema, 400: dict})
async def create_job_history(request, data: JobhistorySchema, document: Optional[UploadedFile] = File(None)):
    user = request.auth
    try:
        employee = await sync_to_async(Employee.objects.get)(user=user)

        job = await sync_to_async(Jobhistory.objects.create)(
            employee=employee,
            **data.dict(exclude={"employee"})
        )

        if document:
            job.document = document.name  # store filename or handle path
            await sync_to_async(job.save)()

        # 🚀 Construct schema manually (avoid .from_orm)
        job_data = JobhistorySchema(
            id=job.id,
            employee=employee.id,
            employer=job.employer,
            job_title=job.job_title,
            employee_code=job.employee_code,
            joining_date=job.joining_date,
            relieving_date=job.relieving_date,
            last_CTC=job.last_CTC,
            reason=job.reason,
            document=job.document if job.document else None,
        )
        return 201, job_data
    except Employee.DoesNotExist:
        return 400, {"message": "Employee profile not found"}


@employee_additional_api.get("/jobhistory", response={200: List[JobhistorySchema], 404: dict})
async def get_job_history(request):
    user = request.auth
    try:
        employee = await sync_to_async(Employee.objects.get)(user=user)
        jobs = await sync_to_async(list)(Jobhistory.objects.filter(employee=employee))

        job_list = [
            JobhistorySchema(
                id=j.id,
                employee=employee.id,
                employer=j.employer,
                job_title=j.job_title,
                employee_code=j.employee_code,
                joining_date=j.joining_date,
                relieving_date=j.relieving_date,
                last_CTC=j.last_CTC,
                reason=j.reason,
                document=j.document if j.document else None,
            )
            for j in jobs
        ]

        return 200, job_list
    except Employee.DoesNotExist:
        return 404, {"message": "Employee profile not found"}


# REFERENCES
@employee_additional_api.post("/references", response={201: ReferencesSchema, 400: dict})
async def create_references(request, data: ReferencesSchema):
    user = request.auth
    try:
        employee = await sync_to_async(Employee.objects.get)(user=user)
        reference = await sync_to_async(References.objects.create)(
            employee=employee,
            **data.dict()
        )
        return 201, ReferencesSchema.from_orm(reference)
    except Employee.DoesNotExist:
        return 400, {"message": "Employee profile not found"}

@employee_additional_api.get("/references", response={200: List[ReferencesSchema], 404: dict})
async def get_references(request):
    user = request.auth
    try:
        employee = await sync_to_async(Employee.objects.get)(user=user)
        references = await sync_to_async(list)(References.objects.filter(employee=employee))
        return 200, [ReferencesSchema.from_orm(r) for r in references]
    except Employee.DoesNotExist:
        return 404, {"message": "Employee profile not found"}

# BANK
@employee_additional_api.post("/bank", response={201: BankSchema, 400: dict})
async def create_bank(request, data: BankSchema):
    user = request.auth
    try:
        employee = await sync_to_async(Employee.objects.get)(user=user)
        bank = await sync_to_async(Bank.objects.create)(
            employee=employee,
            **data.dict()
        )
        return 201, BankSchema.from_orm(bank)
    except Employee.DoesNotExist:
        return 400, {"message": "Employee profile not found"}

@employee_additional_api.get("/bank", response={200: List[BankSchema], 404: dict})
async def get_bank(request):
    user = request.auth
    try:
        employee = await sync_to_async(Employee.objects.get)(user=user)
        banks = await sync_to_async(list)(Bank.objects.filter(employee=employee))
        return 200, [BankSchema.from_orm(b) for b in banks]
    except Employee.DoesNotExist:
        return 404, {"message": "Employee profile not found"}
