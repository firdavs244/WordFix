"""
Management command to create all badge definitions.

Idempotent: safe to run multiple times.
Usage: python manage.py create_badges
"""

from django.core.management.base import BaseCommand

from apps.users.domain.services import BADGE_DEFINITIONS
from apps.users.infrastructure.models import Badge


class Command(BaseCommand):
    help = "Create all badge definitions (idempotent)."

    def handle(self, *args, **options):
        created = 0
        updated = 0

        for badge_def in BADGE_DEFINITIONS:
            badge, was_created = Badge.objects.update_or_create(
                code=badge_def["code"],
                defaults={
                    "name": badge_def["name"],
                    "description": badge_def["description"],
                    "icon": badge_def["icon"],
                    "category": badge_def["category"],
                    "xp_reward": badge_def["xp_reward"],
                    "rarity": badge_def["rarity"],
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Badges: {created} created, {updated} updated. "
                f"Total: {Badge.objects.count()}"
            )
        )
