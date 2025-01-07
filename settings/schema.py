from datetime import date, datetime
from ninja import Schema
from typing import *
from employee.schema import *


class GeneralSchema(Schema):
    company_name: str
    company_logo: Optional[str]  # File URL or path
    website_url: str
    email_id: str
    employee_code: Optional[str]
    address: str
    state: str
    pincode: str
    fax: Optional[str] = None
    phone: str
    timezone: str

class Message(Schema):
    message: str

class EmployeeSchema(Schema):
    pan:Optional[bool]
    aadhar:Optional[bool]
    job_history:Optional[bool]
    education:Optional[bool]
    family:Optional[bool]
    access:Optional[bool]

class DepartmentInputSchema(Schema):
    title: str
    description: Optional[str] = None
    department_head: Optional[str] = None

class DepartmentSchema(Schema):
    title: str
    description: Optional[str] = None
    department_head:Optional[EmployeeCreation] 
    updated_by: Optional[EmployeeCreation]

class DesignationInputSchema(Schema):
    title: str
    description: Optional[str] = None
    rank: Optional[str] = None


class DesignationSchema(Schema):
    title: str
    description: Optional[str] = None
    rank: Optional[str] = None
    updated:Optional[EmployeeCreation]=None

class Bandschema(Schema):
    title: str
    rank: Optional[str] = None
    updated_by: EmployeeCreation

class BusinessUnitSchema(Schema):
    title: str
    description: Optional[str] = None
    unit_head: Optional[EmployeeCreation] = None
    updated_by: Optional[EmployeeCreation]



