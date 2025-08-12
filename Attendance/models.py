from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from datetime import timedelta,datetime,date

from user.models import Organization
from employee.basic_details.models import Employee

User = get_user_model()

class AttendanceDailyRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half Day'),
        ('late', 'Late'),
        ('early_left', 'Early Left'),
        ('weekend', 'Weekend'),
        ('holiday', 'Holiday')
    ], default='present')
    is_justified = models.BooleanField(default=False)
    justification_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']
        verbose_name = 'Daily Attendance'
        verbose_name_plural = 'Daily Attendance Records'

    def __str__(self):
        return f"{self.employee.user.name} - {self.date} ({self.status})"

    def calculate_status(self):
        punches = self.time_punches.all().order_by('in_time')

        if not punches.exists():
            # Weekend check
            if self.date.weekday() >= 5:
                self.status = 'weekend'
            else:
                self.status = 'absent'
            self.save()
            return

        total_seconds = 0
        for punch in punches:
            if punch.in_time and punch.out_time:
                # Combine with the attendance date to make full datetime
                in_dt = datetime.combine(self.date, punch.in_time)
                out_dt = datetime.combine(self.date, punch.out_time)

                # Handle cases where out_time might be past midnight
                if out_dt < in_dt:
                    out_dt += timedelta(days=1)

                total_seconds += (out_dt - in_dt).total_seconds()

        first_punch_time = punches.first().in_time
        last_punch_time = punches.last().out_time

        # Status logic
        if total_seconds < 18000:  # Less than 5 hours
            self.status = 'half_day'
        elif first_punch_time > datetime.strptime('09:30:00', '%H:%M:%S').time():
            self.status = 'late'
        elif last_punch_time and last_punch_time < datetime.strptime('18:00:00', '%H:%M:%S').time():
            self.status = 'early_left'
        else:
            self.status = 'present'

        self.save()

class AttendanceTimePunch(models.Model):
    daily_record = models.ForeignKey(AttendanceDailyRecord, on_delete=models.CASCADE, related_name='time_punches')
    in_time = models.TimeField(null=True, blank=True)
    out_time = models.TimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    is_manual = models.BooleanField(default=False)
    device_info = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Time Punch'
        verbose_name_plural = 'Time Punches'
        ordering = ['in_time']

    def save(self, *args, **kwargs):
        if self.in_time and self.out_time:
            # Calculate duration for this punch pair
            in_dt = timezone.datetime.combine(self.daily_record.date, self.in_time)
            out_dt = timezone.datetime.combine(self.daily_record.date, self.out_time)
            self.duration = out_dt - in_dt
        super().save(*args, **kwargs)
        self.daily_record.calculate_status()

    def __str__(self):
        return f"{self.daily_record.employee.user.name} - {self.in_time} to {self.out_time}"

class AttendanceJustification(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_justifications')
    daily_record = models.ForeignKey(AttendanceDailyRecord, on_delete=models.CASCADE, related_name='justifications')
    request_type = models.CharField(max_length=20, choices=[
        ('late_arrival', 'Late Arrival'),
        ('early_departure', 'Early Departure'),
        ('short_time', 'Short Total Time'),
        ('missed_punch', 'Missed Punch'),
        ('absent', 'Absent')
    ])
    reason = models.TextField()
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ])
    supporting_document = models.FileField(upload_to='justifications/', null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Attendance Justification'
        verbose_name_plural = 'Attendance Justifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee.user.name} - {self.request_type} ({self.status})"

class Holiday(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='holidays')
    name = models.CharField(max_length=255)
    date = models.DateField()
    recurring = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('organization', 'date', 'name')
        ordering = ['date']

    def __str__(self):
        return f"{self.name} ({self.date})"