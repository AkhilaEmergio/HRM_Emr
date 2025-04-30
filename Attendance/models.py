from django.db import models
from  employee.basic_details.models import Employee

# Create your models here.

class Attendance(models.Model):
    date = models.DateField()
    time = models.TimeField()
    user=models.ForeignKey(Employee,on_delete=models.CASCADE,null=True)
    total_hours=models.FloatField()
    status=models.CharField(max_length=50)
    remarks=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

