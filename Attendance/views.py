from ninja import Router
from datetime import date, timedelta
from typing import Dict, Any
from ninja_jwt.authentication import AsyncJWTAuth
from .schema import *
from .models import AttendanceDailyRecord, AttendanceTimePunch,Holiday,AttendanceJustification
from hrstop.utils.attendence_utils import get_employee_from_user, format_duration
from django.utils.timezone import localtime
from asgiref.sync import sync_to_async
from datetime import date, datetime
from django.contrib.auth import get_user_model
from employee.basic_details.models import Employee
from user.models import UserProfile

attendance_api = Router(tags=["attendance"])
User= get_user_model()

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
    # Fetch punches asynchronously using sync_to_async
    punches = await sync_to_async(lambda: list(daily_record.time_punches.all().order_by("in_time")))()

    # Calculate total time
    total_time_seconds = sum(
        ((p.out_time.hour*3600 + p.out_time.minute*60 + p.out_time.second) -
         (p.in_time.hour*3600 + p.in_time.minute*60 + p.in_time.second))
        for p in punches if p.in_time and p.out_time
    )

    # Fetch holiday asynchronously
    holiday = await sync_to_async(lambda: Holiday.objects.filter(
        organization=daily_record.employee.user.organization,
        date=daily_record.date
    ).first())()

    return {
        "date": daily_record.date,
        "day_name": daily_record.date.strftime('%A'),
        "punches": [
            {
                "id": p.id,
                "in_time": p.in_time.strftime('%H:%M:%S') if p.in_time else None,
                "out_time": p.out_time.strftime('%H:%M:%S') if p.out_time else None,
                "duration": await format_duration(
                    ((p.out_time.hour*3600 + p.out_time.minute*60 + p.out_time.second) -
                     (p.in_time.hour*3600 + p.in_time.minute*60 + p.in_time.second))
                ) if p.in_time and p.out_time else None,
                "is_manual": p.is_manual,
                "device_info": p.device_info,
            }
            for p in punches
        ],
        "total_time": await format_duration(total_time_seconds),
        "status": daily_record.status,
        "is_justified": daily_record.is_justified,
        "is_holiday": bool(holiday),
        "holiday_name": holiday.name if holiday else None,
    }

@attendance_api.get("/daily", response={200: DailyAttendanceResponse, 400: Message}, auth=AsyncJWTAuth())
async def get_daily_attendance(request, target_date: date = None):
    """Get daily attendance record for the logged-in employee"""
    user = request.auth
    if not user:
        return 400, {"message": "Employee not found"}

    target_date = target_date or datetime.today().date()

    try:
        # Fetch employee safely in sync thread
        employee = await sync_to_async(lambda: Employee.objects.filter(user_id=user.id).first())()
        if not employee:
            return 400, {"message": "Employee not found"}

        # Fetch daily record safely in sync thread
        daily_record = await sync_to_async(
            lambda: AttendanceDailyRecord.objects.filter(
                employee=employee,
                date=target_date
            ).prefetch_related("time_punches").first()
        )()

        if daily_record:
            # Call your async helper
            return 200, await get_daily_attendance_response(daily_record)
        else:
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
    """Get weekly attendance records for the logged-in employee"""
    user = request.auth
    if not user:
        return 400, {"message": "Employee not found"}

    try:
        today = date.today()
        start_date = start_date or (today - timedelta(days=today.weekday()))
        end_date = end_date or (start_date + timedelta(days=6))

        employee = await Employee.objects.filter(user_id=user.id).afirst()
        if not employee:
            return 400, {"message": "Employee not found"}

        records = await sync_to_async(list)(
            AttendanceDailyRecord.objects.filter(
                employee=employee,
                date__gte=start_date,
                date__lte=end_date
            ).prefetch_related("time_punches").order_by('date')
        )

        attendances = []
        for record in records:
            attendances.append(await get_daily_attendance_response(record))

        return 200, {
            "start_date": start_date,
            "end_date": end_date,
            "attendances": attendances
        }

    except Exception as e:
        return 400, {"message": str(e)}


@attendance_api.get("/summary", response={200: AttendanceSummary, 400: Message}, auth=AsyncJWTAuth())
async def get_attendance_summary(request, month: int = None, year: int = None):
    """Get monthly attendance summary for the logged-in employee"""
    user = request.auth
    if not user:
        return 400, {"message": "Employee not found"}

    try:
        today = date.today()
        month = month or today.month
        year = year or today.year

        # Fetch user and employee asynchronously
        user_obj = await User.objects.filter(id=user.id).afirst()
        if not user_obj:
            return 400, {"message": "User not found"}

        employee = await Employee.objects.filter(user=user_obj).afirst()
        if not employee:
            return 400, {"message": "Employee not found"}

        # Get all daily attendance records for the month
        records = await sync_to_async(list)(
            AttendanceDailyRecord.objects.filter(
                employee=employee,
                date__year=year,
                date__month=month
            ).prefetch_related('time_punches')
        )

        # Initialize counters
        present_days = absent_days = late_days = early_left_days = half_days = holiday_days = weekend_days = 0
        total_seconds = 0

        for record in records:
            # Count statuses
            if record.status == 'present':
                present_days += 1
            elif record.status == 'absent':
                absent_days += 1
            elif record.status == 'late':
                late_days += 1
            elif record.status == 'early_left':
                early_left_days += 1
            elif record.status == 'half_day':
                half_days += 1
            elif record.status == 'holiday':
                holiday_days += 1
            elif record.status == 'weekend':
                weekend_days += 1

            # Sum total worked seconds for all punches
            total_seconds += sum(
                (tp.duration.total_seconds() for tp in record.time_punches.all() if tp.duration)
            )

        total_hours = total_seconds / 3600
        expected_hours = present_days * 8  # Assuming 8 hours per present day
        discrepancy = total_hours - expected_hours

        return 200, {
            "month": str(month),
            "year": year,
            "present_days": present_days,
            "absent_days": absent_days,
            "late_days": late_days,
            "early_left_days": early_left_days,
            "half_days": half_days,
            "holiday_days": holiday_days,
            "weekend_days": weekend_days,
            "total_working_hours": f"{total_hours:.2f}",
            "expected_working_hours": str(expected_hours),
            "discrepancy_hours": f"{discrepancy:.2f}",
        }

    except Exception as e:
        return 400, {"message": str(e)}

@attendance_api.get("/monthly", response={200: list, 400: Message}, auth=AsyncJWTAuth())
async def get_monthly_attendance(request, month: int = None, year: int = None):
    """
    Get detailed daily attendance for the logged-in employee for a specific month.
    Returns daily status, punches, and total worked hours per day.
    """
    user = request.auth
    if not user:
        return 400, {"message": "Employee not found"}

    try:
        today = date.today()
        month = month or today.month
        year = year or today.year

        # Fetch user and employee asynchronously
        user_obj = await User.objects.filter(id=user.id).afirst()
        if not user_obj:
            return 400, {"message": "User not found"}

        employee = await Employee.objects.filter(user=user_obj).afirst()
        if not employee:
            return 400, {"message": "Employee not found"}

        # Fetch all daily attendance records for the month
        records = await sync_to_async(list)(
            AttendanceDailyRecord.objects.filter(
                employee=employee,
                date__year=year,
                date__month=month
            ).prefetch_related('time_punches')
        )

        monthly_data = []
        for record in records:
            punches_data = [
                {
                    "in_time": str(tp.in_time) if tp.in_time else None,
                    "out_time": str(tp.out_time) if tp.out_time else None,
                    "duration_hours": round(tp.duration.total_seconds()/3600, 2) if tp.duration else 0,
                    "is_manual": tp.is_manual,
                    "device_info": tp.device_info,
                    "location": tp.location,
                }
                for tp in record.time_punches.all()
            ]

            total_seconds = sum(tp.duration.total_seconds() for tp in record.time_punches.all() if tp.duration)
            total_hours = round(total_seconds / 3600, 2)

            monthly_data.append({
                "date": str(record.date),
                "status": record.status,
                "is_justified": record.is_justified,
                "justification_reason": record.justification_reason,
                "total_worked_hours": total_hours,
                "punches": punches_data
            })

        return 200, monthly_data

    except Exception as e:
        return 400, {"message": str(e)}
    
@attendance_api.get("/last-punch", auth=AsyncJWTAuth())
async def get_last_punch(request):
    """Get the last punch time (out_time if exists else in_time)"""
    user = request.auth
    if not user:
        return 400, {"message": "User not authenticated"}

    # 🔹 Step 1: Get Employee linked to this user
    user = await User.objects.filter(id=user.id).afirst()
    employee = await Employee.objects.filter(user=user).afirst()
    if not employee:
        return 400, {"message": "Employee not found"}
    

    # 🔹 Step 2: Get today's attendance record
    record = await AttendanceDailyRecord.objects.filter(
        employee=employee.id,
        date=date.today()
    ).afirst()

    if not record:
        return 200, {"last_punch_time": None, "message": "No punches today"}

    # 🔹 Step 3: Get last punch from related punches
    last_punch = await AttendanceTimePunch.objects.filter(
    daily_record=record
).order_by("-id").afirst()


    if not last_punch:
        return 200, {"last_punch_time": None, "message": "No punches today"}

    # 🔹 Step 4: Decide in/out
    punch_time = (
        last_punch.out_time.strftime("%H:%M:%S")
        if last_punch.out_time
        else last_punch.in_time.strftime("%H:%M:%S") if last_punch.in_time else None
    )

    return 200, {
        "last_punch_time": punch_time,
        "type": "OUT" if last_punch.out_time else "IN"
    }


# @attendance_api.get("/all", auth=AsyncJWTAuth())
# async def get_all_attendance(request):
    """Get all attendance records for the logged-in user"""
    user = request.auth
    if not user:
        return 400, {"message": "Employee not found"}

    # Fetch all attendance records
    records = await AttendanceDailyRecord.objects.filter(
        employee_id=user.id
    ).aprefetch_related("time_punches").aall()

    attendances = []
    for record in records:
        punches = []
        async for punch in record.time_punches.all():
            punches.append({
                "id": punch.id,
                "in_time": punch.in_time.strftime("%H:%M:%S") if punch.in_time else None,
                "out_time": punch.out_time.strftime("%H:%M:%S") if punch.out_time else None,
                "duration": str(punch.duration) if punch.duration else None,
                "is_manual": punch.is_manual,
                "device_info": punch.device_info,
            })

        attendances.append({
            "date": str(record.date),
            "day_name": record.date.strftime("%A"),
            "punches": punches,
            "total_time": str(record.total_working_hours or "00:00"),
            "status": record.status,
            "is_justified": record.is_justified,
            "is_holiday": record.is_holiday,
            "holiday_name": record.holiday_name,
        })

    return 200, {
        "employee_id": user.id,
        "employee_name": user.get_full_name() if hasattr(user, "get_full_name") else str(user),
        "attendances": attendances
    }


@attendance_api.get("/all_attendance", response=Dict[str, Any])
async def get_all_attendance(request, start_date: str = None, end_date: str = None):
    employee = await get_employee_from_user(request.auth)

    # Parse dates if provided, otherwise fetch all
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # ✅ all ORM queries inside sync function
    def fetch_records():
        qs = AttendanceDailyRecord.objects.filter(employee=employee)
        if start_date and end_date:
            qs = qs.filter(date__range=(start_date, end_date))
        qs = qs.order_by("-date").prefetch_related("time_punches")

        records = []
        for record in qs:
            punches = list(record.time_punches.all().order_by("in_time"))
            records.append((record, punches))
        return records

    records = await sync_to_async(fetch_records)()

    # ✅ Now only pure Python logic in async land
    result = []
    for record, punches in records:
        total_seconds = 0
        for p in punches:
            if p.in_time and p.out_time:
                start_dt = datetime.combine(record.date, p.in_time)
                end_dt = datetime.combine(record.date, p.out_time)
                total_seconds += (end_dt - start_dt).total_seconds()

        result.append({
            "date": record.date,
            "day_name": record.date.strftime('%A'),
            "punches": [
                {
                    "id": p.id,
                    "in_time": p.in_time.strftime('%H:%M:%S') if p.in_time else None,
                    "out_time": p.out_time.strftime('%H:%M:%S') if p.out_time else None,
                    "duration": await format_duration(
                        (datetime.combine(record.date, p.out_time) - datetime.combine(record.date, p.in_time)).total_seconds()
                    ) if p.in_time and p.out_time else None,
                    "is_manual": p.is_manual,
                    "device_info": p.device_info
                }
                for p in punches
            ],
            "total_time": await format_duration(total_seconds),
            "status": record.status,
            "is_justified": record.is_justified
        })

    return {
        "employee": employee.id,
        "start_date": start_date,
        "end_date": end_date,
        "attendances": result
    }
from django.utils import timezone

@attendance_api.get("/all", response=Dict[str, Any])
async def get_logged_user_attendance(request, start_date: str = None, end_date: str = None):
    employee = await get_employee_from_user(request.auth)

    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    else:
        start_date = timezone.now().date() - timedelta(days=6)  # default last 7 days

    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    else:
        end_date = timezone.now().date()

    STANDARD_SECONDS = 8 * 60 * 60  # 8 hours

    def fetch_records():
        # preload all attendance & holidays in one go
        daily_qs = AttendanceDailyRecord.objects.filter(
            employee=employee, date__range=(start_date, end_date)
        ).prefetch_related("time_punches")

        records_map = {rec.date: rec for rec in daily_qs}

        holidays = {h.date: h for h in Holiday.objects.filter(
            organization=employee.user.organization, date__range=(start_date, end_date)
        )}

        results = []
        current_date = start_date
        today = timezone.now().date()

        while current_date <= end_date:
            record = records_map.get(current_date)
            punches_data = []
            total_seconds = 0
            percentage = 0
            status = None
            is_justified = False

            # check weekend
            weekday = current_date.weekday()  # 0=Mon,6=Sun
            if weekday in [5, 6]:  # Saturday/Sunday
                status = "Weekend/Off Day"

            # check holiday
            elif current_date in holidays:
                status = f"Holiday - {holidays[current_date].name}"

            # if punch record exists
            elif record:
                punches = list(record.time_punches.all().order_by("in_time"))
                for p in punches:
                    duration = None
                    if p.in_time and p.out_time:
                        duration = (datetime.combine(current_date, p.out_time) -
                                    datetime.combine(current_date, p.in_time)).total_seconds()
                        total_seconds += duration

                    punches_data.append({
                        "id": p.id,
                        "in_time": p.in_time.strftime('%H:%M:%S') if p.in_time else None,
                        "out_time": p.out_time.strftime('%H:%M:%S') if p.out_time else None,
                        "duration": str(timedelta(seconds=duration)) if duration else None,
                        "is_manual": p.is_manual,
                        "device_info": p.device_info
                    })

                percentage = round((total_seconds / STANDARD_SECONDS) * 100, 2) if total_seconds else 0
                status = record.status
                is_justified = record.is_justified

            # if no record
            else:
                if current_date > today:
                    status = "Coming Day"
                else:
                    status = "Absent"

            results.append({
                "date": current_date,
                "day_name": current_date.strftime("%A"),
                "punches": punches_data,
                "total_time": str(timedelta(seconds=total_seconds)) if total_seconds else None,
                "percentage": percentage,
                "status": status,
                "is_justified": is_justified
            })

            current_date += timedelta(days=1)

        return results

    attendances = await sync_to_async(fetch_records)()

    return {
        "employee_id": employee.id,
        "start_date": start_date,
        "end_date": end_date,
        "attendances": attendances
    }



# @attendance_api.post("/request", response={200: AttendanceRequestResponse, 400: Message}, auth=AsyncJWTAuth())
# async def submit_attendance_request(request, payload: AttendanceRequestSchema):
#     user = request.auth
#     if not user:
#         return 400, {"message": "Employee not found"}

#     try:
#         # Auto-assign employee from logged-in user
#         employee = await sync_to_async(lambda: Employee.objects.filter(user_id=user.id).first())()
#         if not employee:
#             return 400, {"message": "Employee not found"}

#         # Get daily record for the date provided (or today if using "requested for")
#         daily_record = await sync_to_async(lambda: AttendanceDailyRecord.objects.filter(
#             employee=employee,
#             date=payload.daily_record_id  # or map "requested_for" to date
#         ).first())()
#         if not daily_record:
#             return 400, {"message": "Daily attendance record not found"}

#         # Create justification request
#         justification = await sync_to_async(lambda: AttendanceJustification.objects.create(
#             employee=employee,
#             daily_record=daily_record,
#             request_type=payload.request_type,
#             reason=payload.reason,
#             supporting_document=payload.supporting_document
#         ))()

#         return 200, {
#             "id": justification.id,
#             "employee_id": employee.id,
#             "daily_record_id": daily_record.id,
#             "request_type": justification.request_type,
#             "reason": justification.reason,
#             "status": justification.status,
#             "supporting_document": justification.supporting_document.url if justification.supporting_document else None,
#             "created_at": str(justification.created_at),
#             "updated_at": str(justification.updated_at),
#         }

#     except Exception as e:
#         return 400, {"message": str(e)}
@attendance_api.get(
    "/monthly-all",
    response={200: MonthlyAttendanceResponse, 400: Message},
    auth=AsyncJWTAuth(),
)
async def get_monthly_attendance_admin(request, month: int = None, year: int = None):
    """
    Admin-only: Get detailed daily attendance for ALL employees in their organization.
    """
    user = request.auth
    if not user:
        return 400, {"message": "User not authenticated"}

    try:
        today = date.today()
        month = month or today.month
        year = year or today.year

        # ✅ Fetch logged-in user
        user_obj = await UserProfile.objects.filter(id=user.id).afirst()
        if not user_obj:
            return 400, {"message": "User not found"}

        # ✅ Only admins allowed
        if user_obj.role != "admin":
            return 400, {"message": "Only admins can view all employees' attendance"}

        # ✅ Get organization
        org = await sync_to_async(lambda: user_obj.organization)()
        if not org:
            return 400, {"message": "Organization not found"}

        # ✅ Fetch employees in org
        employees = await sync_to_async(list)(
            Employee.objects.filter(user__organization=org)
        )

        employees_data = []

        for emp in employees:
            # Attendance records for this employee
            records = await sync_to_async(list)(
                AttendanceDailyRecord.objects.filter(
                    employee=emp,
                    date__year=year,
                    date__month=month
                ).prefetch_related("time_punches")
            )

            daily_attendance = []
            for record in records:
                punches = record.time_punches.all()

                punches_data = [
                    {
                        "in_time": str(tp.in_time) if tp.in_time else None,
                        "out_time": str(tp.out_time) if tp.out_time else None,
                        "duration": str(tp.duration) if tp.duration else None,
                    }
                    for tp in punches
                ]

                # total time (HH:MM:SS style)
                total_seconds = sum(tp.duration.total_seconds() for tp in punches if tp.duration)
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                seconds = int(total_seconds % 60)
                total_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

                daily_attendance.append({
                    "date": str(record.date),
                    "day_name": record.date.strftime("%A"),
                    "punches": punches_data,
                    "total_time": total_time,
                    "status": record.status,
                    "is_justified": record.is_justified,
                })

            employee_name = await sync_to_async(lambda: emp.user.get_full_name())()

            employees_data.append({
                "employee_id": emp.id,
                "employee_name": employee_name,
                "attendance": daily_attendance,
            })

        # ✅ Final response (matches MonthlyAttendanceResponse)
        return 200, {
            "organization": {
                "id": org.id,
                "name": org.organization_name,
                "domain": org.domain,
                "code": org.organisation_code,
                "logo": org.logo.url if org.logo else None,
                "timezone": org.timezone,
                "address": org.address,
            },
            "month": month,
            "year": year,
            "employees": employees_data,
        }

    except Exception as e:
        return 400, {"message": str(e)}
