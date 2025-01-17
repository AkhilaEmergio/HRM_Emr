from datetime import date, datetime
from ninja import Schema
from typing import *
from employee.basic_details.schema import *


class GeneralSchema(Schema):
    organization_name: str
    domain: str
    address: dict[str,str]
    fax: Optional[str] = None
    timezone: str

class organizationDetail(Schema):
     id:int
     name:str

class UserDetail(Schema):
    name:str
    email:str
    phone:str
    role:str
    # organization:Optional[organizationDetail]=None

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
    department_head:Optional[UserDetail] 
    updated_by: Optional[UserDetail]

class DesignationInputSchema(Schema):
    title: str
    description: Optional[str] = None
    rank: Optional[str] = None

class DesignationSchema(Schema):
    title: str
    description: Optional[str] = None
    rank: Optional[str] = None
    updated_by:Optional[UserDetail]

class BandInputschema(Schema):
    title: str
    rank: Optional[str] = None

class Bandschema(Schema):
    title: str
    rank: Optional[str] = None
    updated_by:UserDetail

class BusinessUnitInputSchema(Schema):
    title: str
    description: Optional[str] = None
    unit_head: Optional[str]=None

class BusinessUnitSchema(Schema):
    title: str
    description: Optional[str] = None
    unit_head: Optional[UserDetail] = None
    updated_by: Optional[UserDetail]

class BillingInfoInputSchema(Schema):
    name:str
    address:Dict[str,str]
    gstin:Optional[str]
    pan:Optional[str]
    country:Optional[str]

class BillingInfoSchema(Schema):
    name:str
    address:Dict[str,str]
    gstin:Optional[str]
    pan:Optional[str]
    country:Optional[str]
    updated_by:UserDetail


