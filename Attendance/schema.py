from ninja import Schema
from typing import Optional, Dict, List
from datetime import date, datetime

class Message(Schema):
    message: str

class Attendance(Schema):
    time: str
    total_hours: float
    date:date

