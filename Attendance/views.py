from ninja import Router
from datetime import date, timedelta
from typing import Dict, Any
from ninja_jwt.authentication import AsyncJWTAuth
from .schema import *
from .models import AttendanceDailyRecord, AttendanceTimePunch,Holiday
from hrstop.utils.attendence_utils import get_employee_from_user, format_duration
from django.utils.timezone import localtime
from asgiref.sync import sync_to_async
from datetime import date, datetime

attendance_api = Router(tags=["attendance"])

@attendance_api.post("attendance/punch", response=Dict[str, Any])
async def punch_attendance(request):
    employee = await get_employee_from_user(request.auth)
    today = date.today()
    now = localtime().time()

    daily_record, _ = await sync_to_async(AttendanceDailyRecord.objects.get_or_create)(
        employee=employee,
        date=today
    )

    open_punch = await sync_to_async(lambda: daily_record.time_punches.filter(out_time__isnull=True).first())()
    if open_punch:
        open_punch.out_time = now
        await sync_to_async(open_punch.save)()
    else:
        await sync_to_async(AttendanceTimePunch.objects.create)(
            daily_record=daily_record,
            in_time=now,
            device_info=request.META.get('HTTP_USER_AGENT', 'Unknown')
        )

    await sync_to_async(daily_record.refresh_from_db)()
    punches = await sync_to_async(lambda: list(daily_record.time_punches.all().order_by('in_time')))()

    # Calculate total time safely
    total_seconds = 0
    for p in punches:
        if p.in_time and p.out_time:
            start_dt = datetime.combine(today, p.in_time)
            end_dt = datetime.combine(today, p.out_time)
            total_seconds += (end_dt - start_dt).total_seconds()

    return {
        "date": today,
        "day_name": today.strftime('%A'),
        "punches": [
            {
                "id": p.id,
                "in_time": p.in_time.strftime('%H:%M:%S') if p.in_time else None,
                "out_time": p.out_time.strftime('%H:%M:%S') if p.out_time else None,
                "duration": await format_duration(
                    (datetime.combine(today, p.out_time) - datetime.combine(today, p.in_time)).total_seconds()
                ) if p.in_time and p.out_time else None,
                "is_manual": p.is_manual,
                "device_info": p.device_info
            }
            for p in punches
        ],
        "total_time": await format_duration(total_seconds),
        "status": daily_record.status,
        "is_justified": daily_record.is_justified
    }


async def get_daily_attendance_response(daily_record: AttendanceDailyRecord) -> Dict[str, Any]:
    punches = [punch async for punch in daily_record.time_punches.all().order_by('in_time')]
    
    # Calculate total time
    total_time = sum(
        (punch.out_time - punch.in_time).total_seconds()
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
                "duration": await format_duration(punch.duration.total_seconds()) if punch.duration else None,
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


@attendance_api.get("/daily", response={200: DailyAttendanceResponse, 400: Message}, auth=AsyncJWTAuth())
async def get_daily_attendance(request, date: date = None):
    """Get daily attendance record"""
    user = request.auth
    if not user:
        return 400, {"message": "Employee not found"}

    try:
        target_date = date or datetime.today().date()

        daily_record = await AttendanceDailyRecord.objects.prefetch_related("time_punches").aget(
            employee=user.id,
            date=target_date
        )

        return 200, await get_daily_attendance_response(daily_record)

    except AttendanceDailyRecord.DoesNotExist:
        return 200, {
            "date": target_date,
            "day_name": target_date.strftime("%A"),
            "punches": [],
            "status": "absent",
            "total_time": "00:00",
            "is_justified": False,
            "is_holiday": False,
            "holiday_name": None,
        }

    except Exception as e:
        return 400, {"message": str(e)}

@attendance_api.get("/weekly", response={200: AttendanceRangeResponse, 400: Message}, auth=AsyncJWTAuth())
async def get_weekly_attendance(request, start_date: date = None, end_date: date = None):
    """Get weekly attendance records"""
    user = request.auth
    if not user:
        return 400, {"message": "Employee not found"}
    
    try:
        if not start_date or not end_date:
            today = date.today()
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        
        records = await sync_to_async(list)(
            AttendanceDailyRecord.objects.filter(
                employee=user.id,
                date__gte=start_date,
                date__lte=end_date
            ).order_by('date')
        )
        
        return 200, {
            "start_date": start_date,
            "end_date": end_date,
            "attendances": [
                await get_daily_attendance_response(record) for record in records
            ]
        }

    except Exception as e:
        return 400, {"message": str(e)}


@attendance_api.get("/summary", response={200: AttendanceSummary, 400: Message}, auth=AsyncJWTAuth())
async def get_attendance_summary(request, month: int = None, year: int = None):
    """Get monthly attendance summary"""
    user = request.auth
    if not user:
        return 400, {"message": "Employee not found"}
    
    try:
        today = date.today()
        month = month or today.month
        year = year or today.year
        
        records = await sync_to_async(list)(
            AttendanceDailyRecord.objects.filter(
                employee=user.id,
                date__year=year,
                date__month=month
            )
        )
        
        present_days = sum(1 for r in records if r.status == 'present')
        absent_days = sum(1 for r in records if r.status == 'absent')
        late_days = sum(1 for r in records if r.status == 'late')

        # total hours worked
        total_hours = sum(
            (r.total_time.total_seconds() if r.total_time else 0) 
            for r in records
        ) / 3600  

        # expected hours (assuming 8 per present day)
        expected_hours = present_days * 8  

        discrepancy = total_hours - expected_hours  

        return 200, {
            "month": str(month),   # make month string if schema wants it
            "year": year,
            "present_days": present_days,
            "absent_days": absent_days,
            "late_days": late_days,
            "early_left_days": 0,
            "half_days": 0,
            "holiday_days": 0,
            "weekend_days": 0,
            "total_working_hours": f"{total_hours:.2f}",     # convert float → string
            "expected_working_hours": str(expected_hours),   # int → string
            "discrepancy_hours": f"{discrepancy:.2f}",       # float → string
        }
        
    except Exception as e:
        return 400, {"message": str(e)}
