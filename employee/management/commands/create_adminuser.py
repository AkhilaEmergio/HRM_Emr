from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        # Fetch superuser credentials from environment or config file
        username = config('DJANGO_SUPERUSER_USERNAME', default='admin@gmail.com')
        email = config('DJANGO_SUPERUSER_EMAIL', default='admin@gmail.com')
        password = config('DJANGO_SUPERUSER_PASSWORD', default='Adminpass111111@')

        # Get the user model (this is your UserProfile model, which extends AbstractUser)
        User = get_user_model()

        # Check if superuser already exists
        if not User.objects.filter(username=username).exists():
            self.stdout.write('Creating superuser...')
            
            # Create superuser using the custom UserProfile model (which extends AbstractUser)
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )

            # Assign additional fields for UserProfile
            user.name = 'Admin User'  # You can set default values for the profile here
            user.phone = '8606940413'
            user.employee_code = 'EMP001'
            user.reporting_manager = 'None'
            user.business_unit = 'HR'
            user.department = 'Admin'
            user.designation = 'Administrator'
            user.date_of_joining = '2024-12-25'
            user.employment_type = 'Full-time'
            user.service_status = 'Active'
            user.workmode = 'Office'
            user.probation = 'No'
            user.extension = 'No'
            user.notice_period = 'None'
            user.enrollment_no = '12345'
            user.trigger_onboarding = False
            user.send_mail = True
            user.weekly_offs = ["Saturday", "Sunday"]
            user.total_hr_spend = 0.0
            user.active_from = None
            user.inactive_from = None
            user.deactivate = False
            user.deactivated_on = None

            # Save the profile fields
            user.save()

            self.stdout.write(self.style.SUCCESS(f'Superuser created successfully with username {username}'))

        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser with username {username} already exists.'))
