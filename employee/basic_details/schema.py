from ninja import Schema
from typing import Optional, Dict, List
from datetime import datetime

class Message(Schema):
    message: str

class EmployeeSchema(Schema):
    id: int
    user_id: Optional[int]
    created_by_id: Optional[int]
    employee_code: Optional[str]
    profile: Optional[str]
    reporting_manager_id: Optional[int]
    business_unit_id: Optional[int]
    department_id: Optional[int]
    designation_id: Optional[int]
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