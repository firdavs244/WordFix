"""
Celery tasks for user notifications and reminders.
"""

import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def review_reminder_task():
    """Send review reminders to users with due words.

    Scheduled: daily at 9:00 and 19:00.
    """
    from datetime import timezone as tz
    from django.utils import timezone
    from apps.users.infrastructure.models import CustomUser
    from apps.words.infrastructure.models import Word
    from apps.users.presentation.progress_dependencies import get_notification_service

    notification_service = get_notification_service()
    now = timezone.now()

    users = CustomUser.objects.filter(is_active=True)
    sent = 0

    for user in users:
        due_count = Word.objects.filter(
            user=user,
            next_review_at__lte=now,
            is_mastered=False,
            is_active=True,
        ).count()

        if due_count > 0:
            notification_service.create_notification(
                user_id=user.id,
                notification_type="review_reminder",
                title="Time to Review! 📚",
                message=f"You have {due_count} words waiting for review!",
                data={"due_count": due_count},
            )
            sent += 1

    logger.info(f"Sent {sent} review reminders")


@shared_task
def streak_warning_task():
    """Warn users about losing their streak.

    Scheduled: daily at 20:00.
    """
    from datetime import date
    from apps.words.infrastructure.models import DailyStreak, DailyActivity
    from apps.users.presentation.progress_dependencies import get_notification_service

    notification_service = get_notification_service()
    today = date.today()
    sent = 0

    streaks = DailyStreak.objects.filter(
        current_streak__gt=0,
    ).select_related("user")

    for streak in streaks:
        # Check if user has reviewed today
        has_activity = DailyActivity.objects.filter(
            user=streak.user,
            date=today,
            words_reviewed__gt=0,
        ).exists()

        if not has_activity:
            notification_service.create_notification(
                user_id=streak.user.id,
                notification_type="streak_warning",
                title="Don't Lose Your Streak! 🔥",
                message=f"Don't lose your {streak.current_streak}-day streak! Review now!",
                data={"current_streak": streak.current_streak},
            )
            sent += 1

    logger.info(f"Sent {sent} streak warnings")


@shared_task
def weekly_report_task():
    """Send weekly report notifications.

    Scheduled: every Monday at 10:00.
    """
    from datetime import date, timedelta
    from django.db.models import Sum
    from apps.users.infrastructure.models import CustomUser, XPTransaction
    from apps.words.infrastructure.models import DailyActivity
    from apps.users.presentation.progress_dependencies import get_notification_service

    notification_service = get_notification_service()
    today = date.today()
    week_ago = today - timedelta(days=7)
    sent = 0

    users = CustomUser.objects.filter(is_active=True)

    for user in users:
        # Weekly stats
        activities = DailyActivity.objects.filter(
            user=user, date__gte=week_ago, date__lt=today,
        )
        words_reviewed = sum(a.words_reviewed for a in activities)
        words_added = sum(a.words_added for a in activities)

        xp_earned = XPTransaction.objects.filter(
            user=user, created_at__date__gte=week_ago, created_at__date__lt=today,
        ).aggregate(total=Sum("amount"))["total"] or 0

        if words_reviewed > 0 or words_added > 0 or xp_earned > 0:
            notification_service.create_notification(
                user_id=user.id,
                notification_type="weekly_report",
                title="Weekly Report 📊",
                message=(
                    f"This week: {words_reviewed} words reviewed, "
                    f"{words_added} words added, {xp_earned} XP earned!"
                ),
                data={
                    "words_reviewed": words_reviewed,
                    "words_added": words_added,
                    "xp_earned": xp_earned,
                },
            )
            sent += 1

    logger.info(f"Sent {sent} weekly reports")
