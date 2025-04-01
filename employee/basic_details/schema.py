from ninja import Schema
from typing import Optional, Dict, List
from datetime import date, datetime

class Message(Schema):
    message: str

class UserDetail(Schema):
    name:str
    email:str
    phone:str
    role:str

class Business_unit(Schema):
    title: str
    description: Optional[str] = None
    unit_head: Optional[UserDetail] = None
    updated_by: Optional[UserDetail]

class Designation(Schema):
    title: str
    description: Optional[str] = None
    rank: Optional[str] = None
    updated_by:Optional[UserDetail]

class Department(Schema):
    title: str
    description: Optional[str] = None
    department_head:Optional[UserDetail]
    updated_by: Optional[UserDetail]

class EmployeeSchema(Schema):
    id: int
    user: UserDetail
    created_by: UserDetail
    employee_code: Optional[str]
    profile: Optional[str]
    reporting_manager: Optional[UserDetail]
    business_unit: Optional[Business_unit]
    department: Optional[Department]
    designation: Optional[Designation]
    date_of_joining: Optional[str]
    employment_type: Optional[str]
    service_status: Optional[str]
    workmode: Optional[str]
    probation: Optional[str]
    extension: Optional[str]
    notice_period: Optional[str]
    enrollment_no: Optional[str]
    trigger_onboarding: Optional[bool]
    send_mail: Optional[bool] = True
    weekly_offs: Optional[Dict]
    permissions: Optional[Dict]

class EmployeeInputSchema(Schema):
    username: str
    email: str
    password: str
    name: str
    phone: str
    role: str = "employee"
    employee_code: Optional[str]=None
    reporting_manager_id: Optional[int]=None
    business_unit_id: Optional[int]=None
    department_id: Optional[int]=None
    designation_id: Optional[int]=None
    date_of_joining: Optional[str]=None
    employment_type: Optional[str]=None
    service_status: Optional[str]=None
    workmode: Optional[str]=None
    probation: Optional[str]=None
    extension: Optional[str]=None
    notice_period: Optional[str]=None
    enrollment_no: Optional[str]=None
    trigger_onboarding: Optional[bool]=None
    send_mail: Optional[bool] = True
    weekly_offs: Optional[Dict]=None
    permissions: Optional[Dict]=None

class EmployeeUpdateSchema(Schema):
    employee_code: Optional[str]
    profile: Optional[str]
    reporting_manager_id: Optional[int]=None
    business_unit_id: Optional[int]=None
    department_id: Optional[int]=None
    designation_id: Optional[int]=None
    date_of_joining: Optional[str]=None
    employment_type: Optional[str]=None
    service_status: Optional[str]=None
    workmode: Optional[str]=None
    probation: Optional[str]=None
    extension: Optional[str]=None
    notice_period: Optional[str]=None
    enrollment_no: Optional[str]=None
    trigger_onboarding: Optional[bool]=None
    send_mail: Optional[bool] = True
    weekly_offs: Optional[Dict]=None
    permissions: Optional[Dict]=None


class PersonalDetailSchema(Schema):
    id: Optional[int]=None
    fullname: Dict[str,str]
    date_of_birth: date
    place_of_birth: str
    gender: str
    bloodgroup: str
    domicile: str
    citizenship: str
    religion: str
    marital_status: str
    marriage_date: Optional[date]=None
    workphone: Optional[str]
    personal_email: Optional[str]
    linkedin: Optional[str]
    slackuser: Optional[str]
    permanent_address: str
    present_address: str
    drivinglicense: Optional[str]
    passport: Optional[str]
    aadhar_number: str
    pan: Optional[str]
    uan: Optional[str]
    skills: Optional[Dict]
    total_experiance: Optional[int]