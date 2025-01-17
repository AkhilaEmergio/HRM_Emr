from typing import Optional, List, Dict
from datetime import date
from datetime import datetime
from ninja import Schema

class Message(Schema):
    message: str

# Education Schema
class EducationSchema(Schema):
    id: int
    employee_id: int
    degree: str
    specialization: Optional[str]
    college: str
    university: Optional[str]
    year_of_passing: str
    gpa: Optional[str]
    document: Optional[str]

class EducationInputSchema(Schema):
    degree: str
    specialization: Optional[str]
    college: str
    university: Optional[str]
    year_of_passing: str
    gpa: Optional[str]

# Emergency Contact Schema
class EmergencySchema(Schema):
    id: int
    employee_id: int
    name: str
    relationship: str
    dob: Optional[str]
    occupation: Optional[str]
    phone_number: str
    address: Optional[Dict]


class EmergencyInputSchema(Schema):
    name: str
    relationship: str
    dob: Optional[str]
    occupation: Optional[str]
    phone_number: str
    address: Optional[Dict]

# Family Schema
class FamilySchema(Schema):
    id: int
    employee_id: int
    name: str
    phone: str
    relationship: str
    date_of_birth: Optional[date]
    gender: Optional[str]
    occupation: Optional[str]
    address: Optional[Dict]
    isdependent: bool

class FamilyInputSchema(Schema):
    name: str
    phone: str
    relationship: str
    date_of_birth: Optional[date]
    gender: Optional[str]
    occupation: Optional[str]
    address: Optional[Dict]
    isdependent: bool

# Job History Schema
class JobhistorySchema(Schema):
    id: int
    employee_id: int
    employer: str
    job_title: str
    employee_code: Optional[str]
    joining_date: date
    relieving_date: date
    last_CTC: str
    reason: Optional[str]
    document: Optional[str]


class JobhistoryInputSchema(Schema):
    employer: str
    job_title: str
    employee_code: Optional[str]
    joining_date: date
    relieving_date: date
    last_CTC: str
    reason: Optional[str]

# References Schema
class ReferencesSchema(Schema):
    id: int
    employee_id: int
    name: str
    job_title: Optional[str]
    company: Optional[str]
    email: str
    mobile_no: str


class ReferencesInputSchema(Schema):
    name: str
    job_title: Optional[str]
    company: Optional[str]
    email: str
    mobile_no: str

# Bank Schema
class BankSchema(Schema):
    id: int
    employee_id: int
    name_of_bank: str
    account_no: str
    ifsc: str
    branch: Optional[str]
    account_type: str
    payment_mode: Optional[str]
    document: Optional[str]


class BankInputSchema(Schema):
    name_of_bank: str
    account_no: str
    ifsc: str
    branch: Optional[str]
    account_type: str
    payment_mode: Optional[str]