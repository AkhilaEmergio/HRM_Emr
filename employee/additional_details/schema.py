from ninja import Schema
from typing import Optional, Dict, List
from datetime import date, datetime



class Message(Schema):
    message: str

class EducationSchema(Schema):
    id: Optional[int] = None
    employee: Optional[int] = None
    degree: str
    specialization: Optional[str]
    college: str
    university: Optional[str]
    year_of_passing: str
    gpa: Optional[str]
    document: Optional[str]

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            employee=getattr(obj, "employee_id", None),  # 👈 convert to int
            degree=obj.degree,
            specialization=obj.specialization,
            college=obj.college,
            university=obj.university,
            year_of_passing=obj.year_of_passing,
            gpa=obj.gpa,
            document=str(obj.document) if obj.document else None,
        )


class EmergencySchema(Schema):
    id: Optional[int] = None
    employee: Optional[int] = None   # must stay int for API response
    name: str
    relationship: str
    dob: Optional[date] = None
    occupation: Optional[str] = None
    phone_number: str
    address: Optional[Dict] = None

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            employee=getattr(obj, "employee_id", None),  # ✅ FK as integer
            name=obj.name,
            relationship=obj.relationship,
            dob=obj.dob,
            occupation=obj.occupation,
            phone_number=obj.phone_number,
            address=obj.address,  # assuming JSONField/DictField in model
        )

class FamilySchema(Schema):
    id: Optional[int] = None
    employee: Optional[int] = None   # will show employee_id in response
    name: str
    relationship: str
    date_of_birth: Optional[date] = None
    occupation: Optional[str] = None
    phone: str
    address: Optional[Dict] = None   # assuming JSONField/DictField in model

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            employee=getattr(obj, "employee_id", None),  # ✅ convert FK to int
            name=obj.name,
            relationship=obj.relationship,
            date_of_birth=obj.date_of_birth,
            occupation=obj.occupation,
            phone=obj.phone,
            address=obj.address,
        )

class JobhistorySchema(Schema):
    id: Optional[int] = None
    employee: Optional[int] = None   # keep int, not str
    employer: str
    job_title: str
    employee_code: Optional[str] = None
    joining_date: date
    relieving_date: date
    last_CTC: str
    reason: Optional[str] = None
    document: Optional[str] = None

    # class Config:
    #     orm_mode = True   # ✅ required for from_orm


class ReferencesSchema(Schema):
    id: Optional[int]=None
    name: str
    job_title: Optional[str]
    company: Optional[str]
    email: str
    mobile_no: str
    
class BankSchema(Schema):
    id: Optional[int]=None
    name_of_bank: str
    account_no: str
    ifsc: str
    branch: Optional[str]
    account_type: str

