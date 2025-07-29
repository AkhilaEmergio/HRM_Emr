from ninja import Router
from datetime import date, timedelta
from typing import Dict, Any
from ninja_jwt.authentication import AsyncJWTAuth
from .schema import *
from .models import AttendanceDailyRecord, AttendanceTimePunch
from hrstop.utils.attendence_utils import get_employee_from_user, format_duration
from django.utils.timezone import localtime
from asgiref.sync import sync_to_async

attendance_api = Router(tags=["attendance"])

@attendance_api.post("attendance/punch", response=Dict[str, Any])
async def punch_attendance(request):
    employee = await get_employee_from_user(request.auth)
    today = date.today()
    now = localtime().time()

    daily_record, _ = await sync_to_async(AttendanceDailyRecord.objects.get_or_create)(employee=employee, date=today)

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

    total_time = sum(
        (p.out_time - p.in_time)
        for p in punches if p.in_time and p.out_time
    )

    return {
        "date": today,
        "day_name": today.strftime('%A'),
        "punches": [
            {
                "id": p.id,
                "in_time": p.in_time.strftime('%H:%M:%S') if p.in_time else None,
                "out_time": p.out_time.strftime('%H:%M:%S') if p.out_time else None,
                "duration": await format_duration(p.out_time - p.in_time) if p.in_time and p.out_time else None,
                "is_manual": p.is_manual,
                "device_info": p.device_info
            }
            for p in punches
        ],
        "total_time": await format_duration(total_time),
        "status": daily_record.status,
        "is_justified": daily_record.is_justified
    }

@attendance_api.get("/daily", response={200: DailyAttendanceResponse, 400: Message}, auth=AsyncJWTAuth())
async def get_daily_attendance(request, date: date = None):
    """Get daily attendance record"""
    user = request.auth
    if not user or not await sync_to_async(lambda: hasattr(user, 'employee'))():
        return 400, {"message": "Employee not found"}
    
    try:
        target_date = date or date.today()
        daily_record = await AttendanceDailyRecord.objects.aget(
            employee=user.employee,
            date=target_date
        )
        
        punches = await sync_to_async(list)(daily_record.timepunches.all().order_by('in_time'))
        
        return 200, {
            "date": target_date,
            "punches": punches,
            "status": daily_record.status,
            "total_hours": str(daily_record.total_time) if daily_record.total_time else "00:00"
        }
        
    except AttendanceDailyRecord.DoesNotExist:
        return 200, {
            "date": target_date,
            "punches": [],
            "status": "absent",
            "total_hours": "00:00"
        }
    except Exception as e:
        return 400, {"message": str(e)}

@attendance_api.get("/weekly", response={200: AttendanceRangeResponse, 400: Message}, auth=AsyncJWTAuth())
async def get_weekly_attendance(request, start_date: date = None, end_date: date = None):
    """Get weekly attendance records"""
    user = request.auth
    if not user or not await sync_to_async(lambda: hasattr(user, 'employee'))():
        return 400, {"message": "Employee not found"}
    
    try:
        if not start_date or not end_date:
            today = date.today()
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        
        records = await sync_to_async(list)(
            AttendanceDailyRecord.objects.filter(
                employee=user.employee,
                date__gte=start_date,
                date__lte=end_date
            ).order_by('date')
        )
        
        return 200, {
            "start_date": start_date,
            "end_date": end_date,
            "records": records
        }
        
    except Exception as e:
        return 400, {"message": str(e)}

@attendance_api.get("/summary", response={200: AttendanceSummary, 400: Message}, auth=AsyncJWTAuth())
async def get_attendance_summary(request, month: int = None, year: int = None):
    """Get monthly attendance summary"""
    user = request.auth
    if not user or not await sync_to_async(lambda: hasattr(user, 'employee'))():
        return 400, {"message": "Employee not found"}
    
    try:
        today = date.today()
        month = month or today.month
        year = year or today.year
        
        records = await sync_to_async(list)(
            AttendanceDailyRecord.objects.filter(
                employee=user.employee,
                date__year=year,
                date__month=month
            )
        )
        
        present_days = sum(1 for r in records if r.status == 'present')
        absent_days = sum(1 for r in records if r.status == 'absent')
        late_days = sum(1 for r in records if r.status == 'late')
        
        return 200, {
            "month": month,
            "year": year,
            "present_days": present_days,
            "absent_days": absent_days,
            "late_days": late_days,
            "total_hours": sum(
                (r.total_time.total_seconds() if r.total_time else 0) 
                for r in records
            ) / 3600
        }
        
    except Exception as e:
        return 400, {"message": str(e)}