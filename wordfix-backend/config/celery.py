"""
Celery configuration for WordFix project.
"""

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("config")

# Load config from Django settings, using CELERY_ namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# Also discover tasks in infrastructure sub-packages (Clean Architecture layout)
app.autodiscover_tasks([
    "apps.words.infrastructure",
    "apps.users.infrastructure",
])


# Celery Beat schedule
app.conf.beat_schedule = {
    "update-streaks-daily": {
        "task": "apps.words.infrastructure.tasks.update_streaks_task",
        "schedule": 86400.0,  # Once per day
    },
    "cleanup-stale-sessions": {
        "task": "apps.words.infrastructure.tasks.cleanup_stale_sessions_task",
        "schedule": 3600.0,  # Every hour
    },
    "review-reminder-morning": {
        "task": "apps.users.infrastructure.tasks.review_reminder_task",
        "schedule": 43200.0,  # Twice per day (12h)
    },
    "streak-warning-evening": {
        "task": "apps.users.infrastructure.tasks.streak_warning_task",
        "schedule": 86400.0,  # Once per day
    },
    "weekly-report": {
        "task": "apps.users.infrastructure.tasks.weekly_report_task",
        "schedule": 604800.0,  # Once per week
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task to verify Celery is working."""
    print(f"Request: {self.request!r}")
