from ninja import Schema
from typing import Optional, Dict, List
from datetime import date, datetime



class Message(Schema):
    message: str

class EducationSchema(Schema):
    employee:Optional[int]=None
    degree:str
    specialization:Optional[str]
    college = str
    university =Optional[str]
    year_of_passing = str
    gpa = Optional[str]
    document = Optional[str]

class EmergencySchema(Schema):
    employee:Optional[int]=None
    name:str
    relationship:str
    dob:Optional[date]=None
    occupation:Optional[str]=None
    phone_number:str
    address:Optional[Dict]=None

class FamilySchema(Schema):
    employee:Optional[int]=None
    name:str
    relationship:str
    dob :Optional[date]=None
    occupation:Optional[str]=None
    phone_number:str
    address:Optional[Dict]=None

class JobhistorySchema(Schema):
    employee:Optional[str]=None
    employer:str
    job_title:str
    employee_code:Optional[str]=None
    joining_date:date
    relieving_date:date
    last_CTC:str
    reason:Optional[str]=None
    document:Optional[str]=None

