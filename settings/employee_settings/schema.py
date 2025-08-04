from pydantic import BaseModel
from typing import Optional, Dict, Union, List
from datetime import datetime
from ninja import Schema
from settings.general_settings.schema import *

class Message(Schema):
    message: str

class UserDetail(Schema):
    id: int
    name: str
    
class organizationDetail(Schema):
     id:int
     name:str

# Schemas for EmployeeProfileSettings
class EmployeeProfileSettingsSchema(Schema):
    organization: Optional[organizationDetail] = None
    manage_employee_profile: Optional[str] = None
    unique_fields: Optional[Dict] = None
    employee_skills: Optional[str] = None
    custom_skills: Optional[Dict] = None
    approve_required: Optional[bool] = None
    employees_addable: Optional[bool] = None
    filter_search: Optional[bool] = None
    generally_showable_fields: Optional[Dict] = None
    officially_showable_fields: Optional[Dict] = None
    contacts_showable_fields: Optional[Dict] = None
    other_showable_fields: Optional[Dict] = None
    mandatory_inputable_fields: Optional[Dict] = None
    updated_by: Optional[UserDetail] = None

class EmployeeProfileSettingsInputSchema(Schema):

    manage_employee_profile: Optional[str] = None
    unique_fields:Optional[Dict]
    employee_skills: str
    custom_skills: Optional[Dict]
    approve_required: bool
    employees_addable: bool
    filter_search: bool
    generally_showable_fields: Dict
    officially_showable_fields: Dict
    contacts_showable_fields: Dict
    other_showable_fields: Dict
    mandatory_inputable_fields: Dict

# Schemas for DocumentSetting
class DocumentSettingSchema(Schema):
    organization: Optional[organizationDetail] = None
    title: str
    module: str
    description: str
    applicable_to: str
    no_of_document: int
    expiry_date: bool
    mandatory: bool
    identification: bool
    issue_date: bool
    updated_by_id: int

class DocumentSettingInputSchema(Schema):
    title: str
    module: str
    description: str
    applicable_to: str
    no_of_document: int
    expiry_date: bool
    mandatory: bool
    identification: bool
    issue_date: bool