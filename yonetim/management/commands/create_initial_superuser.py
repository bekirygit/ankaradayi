from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser with predefined credentials if one does not exist.'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'renderadmin'
        password = 'renderpassword' # Lütfen bunu daha sonra değiştirin!
        email = 'admin@example.com'

        if not User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f'Creating superuser {username}...'))
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created successfully with password {password}'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {username} already exists.'))
