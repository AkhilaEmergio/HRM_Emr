from datetime import date, datetime
from ninja import Schema
from typing import *

class OrganizationSchema(Schema):
    name: str
    domain: str
    logo: Optional[str] = None  # Optional
    address:Dict[str,str]
    date:datetime

class Message(Schema):
    message: str
    
class UserProfileSchema(Schema):
    username: str
    email: str
    password: str
    name: str
    phone: str
    role: str = "admin" 