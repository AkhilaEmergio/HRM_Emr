from pydantic import BaseModel
from typing import Optional, Dict, Union, List
from datetime import datetime
from ninja import Schema
from settings.general_settings.schema import *

class Message(Schema):
    message: str

# Schemas for EmployeeProfileSettings
class EmployeeProfileSettingsSchema(Schema):
    id: int
    manage_employee_profile: str
    unique_fields: Dict
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
    updated_by: UserDetail


class EmployeeProfileSettingsInputSchema(Schema):
    manage_employee_profile: str
    unique_fields: Dict
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
    id: int
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