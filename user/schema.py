from datetime import date, datetime
from ninja import Schema
from typing import *


class UserData(Schema):
    id: int
    username: str
    password:str
    organization:str
    role:str

class Message(Schema):
    message: str

class TokenSchema(Schema):
    access: str
    refresh: str
    role:str
    organization:str

class TokenRefreshSchema(Schema):
    refresh: str

class userSchema(Schema):
    username: str
    email: str
    name: str
    phone: str
    password:str

class LoginSchema(Schema):
    username:str
    password:str



