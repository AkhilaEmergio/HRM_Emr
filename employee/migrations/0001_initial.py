# Generated by Django 5.1.4 on 2025-01-09 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_code', models.CharField(max_length=100)),
                ('profile', models.FileField(null=True, upload_to='profiles/')),
                ('date_of_joining', models.CharField(max_length=100, null=True)),
                ('employment_type', models.CharField(max_length=100, null=True)),
                ('service_status', models.CharField(max_length=100, null=True)),
                ('workmode', models.CharField(max_length=100, null=True)),
                ('probation', models.CharField(max_length=100, null=True)),
                ('extension', models.CharField(max_length=100, null=True)),
                ('notice_period', models.CharField(max_length=100, null=True)),
                ('enrollment_no', models.CharField(max_length=50, null=True)),
                ('trigger_onboarding', models.BooleanField(default=False, null=True)),
                ('send_mail', models.BooleanField(default=True, null=True)),
                ('weekly_offs', models.JSONField(null=True)),
                ('permissions', models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.JSONField()),
                ('date_of_birth', models.DateField()),
                ('place_of_birth', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('bloodgroup', models.CharField(max_length=100)),
                ('domicile', models.CharField(max_length=100)),
                ('citizenship', models.CharField(max_length=100)),
                ('religion', models.CharField(max_length=100)),
                ('marital_status', models.CharField(max_length=100)),
                ('marriage_date', models.DateField(null=True)),
                ('workphone', models.CharField(max_length=20, null=True)),
                ('personal_email', models.CharField(max_length=100, null=True)),
                ('linkedin', models.CharField(max_length=100, null=True)),
                ('slackuser', models.CharField(max_length=100, null=True)),
                ('permanent_address', models.TextField()),
                ('present_address', models.TextField()),
                ('drivinglicense', models.CharField(max_length=100, null=True)),
                ('passport', models.CharField(max_length=100, null=True)),
                ('aadhar_number', models.CharField(max_length=100)),
                ('pan', models.CharField(max_length=100, null=True)),
                ('uan', models.CharField(max_length=100, null=True)),
                ('skills', models.JSONField(blank=True, null=True)),
                ('total_experiance', models.IntegerField(null=True)),
            ],
        ),
    ]
