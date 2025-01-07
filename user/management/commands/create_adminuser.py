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
            user.save()

            self.stdout.write(self.style.SUCCESS(f'Superuser created successfully with username {username}'))

        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser with username {username} already exists.'))
