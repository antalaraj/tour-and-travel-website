from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates an admin user'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin@123'
            )
            self.stdout.write(self.style.SUCCESS('Admin user created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists')) 