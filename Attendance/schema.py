from ninja import Schema
from datetime import date, time
from typing import List, Optional, Dict, Any
from pydantic import Field, validator
from enum import Enum

class Message(Schema):
    message: str

class PunchRecord(Schema):
    id: Optional[int] = None
    in_time: Optional[str] = None
    out_time: Optional[str] = None
    duration: Optional[str] = None
    is_manual: Optional[bool] = None
    device_info: Optional[str] = None
    location: Optional[str] = None

class AttendanceStatus(str, Enum):
    present = "present"
    absent = "absent"
    half_day = "half_day"
    late = "late"
    early_left = "early_left"
    weekend = "weekend"
    holiday = "holiday"

class JustificationType(str, Enum):
    late_arrival = "late_arrival"
    early_departure = "early_departure"
    short_time = "short_time"
    missed_punch = "missed_punch"
    absent = "absent"

class JustificationStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class DailyAttendanceResponse(Schema):
    date: date
    day_name: str
    punches: List[PunchRecord]
    total_time: str
    status: AttendanceStatus
    is_justified: bool
    is_holiday: bool = False
    holiday_name: Optional[str] = None

class AttendanceRangeResponse(Schema):
    start_date: date
    end_date: date
    attendances: List[DailyAttendanceResponse]

class JustificationRequest(Schema):
    date: date
    request_type: JustificationType
    reason: str
    supporting_document: Optional[str] = None

class JustificationResponse(Schema):
    id: int
    date: date
    request_type: JustificationType
    reason: str
    status: JustificationStatus
    supporting_document: Optional[str] = None
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[str] = None
    created_at: str

class AttendanceSummary(Schema):
    month: str
    year: int
    present_days: int
    absent_days: int
    late_days: int
    early_left_days: int
    half_days: int
    holiday_days: int
    weekend_days: int
    total_working_hours: str
    expected_working_hours: str
    discrepancy_hours: str

class ManualPunchRequest(Schema):
    date: date
    in_time: Optional[str] = None
    out_time: Optional[str] = None
    reason: str

    @validator('in_time', 'out_time')
    def validate_time_format(cls, v):
        if v is None:
            return v
        try:
            time.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError("Time must be in HH:MM:SS format")