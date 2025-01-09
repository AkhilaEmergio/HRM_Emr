from datetime import date, datetime
from ninja import Schema
from typing import *

class UserData(Schema):
    id: int
    username: str
    password:str

class Message(Schema):
    message: str

class EmployeeLogin(Schema):
    username: str  
    password: str
    
class EmployeeCreation(Schema):
    employee_code: str
    profile: Optional[str] = None  
    reporting_manager: Optional[str] = None
    business_unit: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    date_of_joining: Optional[str] = None
    employment_type: Optional[str] = None
    service_status: Optional[str] = None
    workmode: Optional[str] = None
    probation: Optional[str] = None
    extension: Optional[str] = None
    notice_period: Optional[str] = None
    enrollment_no: Optional[str] = None
    trigger_onboarding: Optional[bool] = False
    send_mail: Optional[bool] = True
    weekly_offs: Optional[List[str]] = None 
    total_hr_spend: Optional[float] = 0.0
    active_from: Optional[str] = None
    inactive_from: Optional[str] = None
    deactivate: Optional[bool] = False
    deactivated_on: Optional[str] = None



class TokenSchema(Schema):
    access: str
    refresh: str

class TokenRefreshSchema(Schema):
    refresh: str

class PersonalDetailSchema(Schema):
    fullname: dict
    date_of_birth: date
    place_of_birth: str
    gender: str
    bloodgroup: str
    domicile: str
    citizenship: str
    religion: str
    marital_status: str
    marriage_date: Optional[date]
    mobile: str
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
    skills: Optional[str]
    previous_exp: Optional[str]

class GeneralSchema(Schema):
    company_name: str
    company_logo: str
    website_url: str
    email_id: str
    employee_code: str
    address: str
    state: str
    pincode: str
    fax: str
    phone: str
    timezone: str

class EducationSchema(Schema):
    degree: str
    specialization: str
    college: str
    university: str
    year_of_passing: str
    gpa: str
    document: str

class EmergencySchema(Schema):
    name: str
    relationship: str
    dob: Optional[str]
    phone_number: str
    occupation: Optional[str]
    address: str
