"""
Management command: createsuperadmin

Creates a default superuser admin@wordfix.com / admin / admin123456
Idempotent — skips if email already exists.
"""

from django.core.management.base import BaseCommand

from apps.users.infrastructure.models import CustomUser


class Command(BaseCommand):
    help = "Create a default superuser (admin@wordfix.com / admin / admin123456)"

    def handle(self, *args, **options):
        email = "admin@wordfix.com"
        username = "admin"
        password = "admin123456"

        if CustomUser.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"Superuser '{email}' already exists. Skipping."))
            return

        CustomUser.objects.create_superuser(
            email=email,
            username=username,
            password=password,
            full_name="WordFix Admin",
        )
        self.stdout.write(self.style.SUCCESS(f"Superuser '{email}' created successfully."))
