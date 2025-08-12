from datetime import date, datetime, time, timedelta
from typing import Dict, Any
from django.db.models import Q, Sum, Count
from django.utils.timezone import localtime
from employee.basic_details.models import Employee
from Attendance.models import AttendanceDailyRecord, AttendanceTimePunch, Holiday

from datetime import timedelta

async def format_duration(duration) -> str:
    if not duration:
        return "00:00"

    # Handle both timedelta and numeric seconds
    if isinstance(duration, (float, int)):
        total_seconds = int(duration)
    elif isinstance(duration, timedelta):
        total_seconds = int(duration.total_seconds())
    else:
        raise TypeError(f"Unsupported duration type: {type(duration)}")

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"


async def calculate_week_range(target_date: date) -> tuple[date, date]:
    start = target_date - timedelta(days=target_date.weekday())
    end = start + timedelta(days=6)
    return start, end

async def get_employee_from_user(user):
    try:
        return await Employee.objects.aget(user=user)
    except Employee.DoesNotExist:
        return None

async def get_daily_attendance_response(daily_record: AttendanceDailyRecord) -> Dict[str, Any]:
    punches = [punch async for punch in daily_record.time_punches.all().order_by('in_time')]
    
    # Calculate total time for the day
    total_time = sum(
        (punch.out_time - punch.in_time) 
        for punch in punches 
        if punch.in_time and punch.out_time
    )
    
    # Check for holiday
    holiday = await Holiday.objects.filter(
        organization=daily_record.employee.user.organization,
        date=daily_record.date
    ).afirst()
    
    return {
        "date": daily_record.date,
        "day_name": daily_record.date.strftime('%A'),
        "punches": [
            {
                "id": punch.id,
                "in_time": punch.in_time.strftime('%H:%M:%S') if punch.in_time else None,
                "out_time": punch.out_time.strftime('%H:%M:%S') if punch.out_time else None,
                "duration": await format_duration(punch.duration) if punch.duration else None,
                "is_manual": punch.is_manual,
                "device_info": punch.device_info
            }
            for punch in punches
        ],
        "total_time": await format_duration(total_time),
        "status": daily_record.status,
        "is_justified": daily_record.is_justified,
        "is_holiday": bool(holiday),
        "holiday_name": holiday.name if holiday else None
    }