"""
ReviewSession, ReviewLog, DailyStreak, DailyActivity Django ORM models.
"""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.common.models import AbstractBaseModel


class ReviewSession(AbstractBaseModel):
    """A review session tracking user's study activity."""

    SESSION_TYPE_CHOICES = [
        ("review", "Review"),
        ("quick", "Quick"),
        ("focus", "Focus"),
        ("learn", "Learn"),
        ("mixed", "Mixed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="review_sessions",
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    total_words = models.PositiveIntegerField(default=0)
    correct_count = models.PositiveIntegerField(default=0)
    incorrect_count = models.PositiveIntegerField(default=0)
    average_quality = models.FloatField(default=0.0)
    duration_seconds = models.PositiveIntegerField(default=0)
    session_type = models.CharField(
        max_length=10,
        choices=SESSION_TYPE_CHOICES,
        default="review",
    )
    is_completed = models.BooleanField(default=False)
    current_combo = models.PositiveIntegerField(default=0)
    max_combo = models.PositiveIntegerField(default=0)
    combo_xp_bonus = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "review_sessions"
        ordering = ["-started_at"]
        verbose_name = "Review Session"
        verbose_name_plural = "Review Sessions"

    def __str__(self) -> str:
        return f"Review {self.session_type} by user {self.user_id} at {self.started_at}"


class ReviewLog(AbstractBaseModel):
    """Individual word review log within a session."""

    session = models.ForeignKey(
        ReviewSession,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logs",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="review_logs",
    )
    word = models.ForeignKey(
        "Word",
        on_delete=models.CASCADE,
        related_name="review_logs",
    )
    quality = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    response_time_ms = models.PositiveIntegerField(null=True, blank=True)
    is_correct = models.BooleanField()
    reviewed_at = models.DateTimeField(auto_now_add=True)
    previous_confidence = models.FloatField(default=0.0)
    new_confidence = models.FloatField(default=0.0)
    previous_interval = models.PositiveIntegerField(default=0)
    new_interval = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "review_logs"
        ordering = ["-reviewed_at"]
        verbose_name = "Review Log"
        verbose_name_plural = "Review Logs"

    def __str__(self) -> str:
        return f"Review of '{self.word}' quality={self.quality}"


class DailyStreak(AbstractBaseModel):
    """Tracks consecutive daily study streaks for a user."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="streak",
    )
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    streak_frozen_until = models.DateField(null=True, blank=True)
    total_review_days = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "daily_streaks"
        verbose_name = "Daily Streak"
        verbose_name_plural = "Daily Streaks"

    def __str__(self) -> str:
        return f"Streak {self.current_streak} days for user {self.user_id}"


class DailyActivity(AbstractBaseModel):
    """Tracks daily learning activity for a user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="daily_activities",
    )
    date = models.DateField()
    words_reviewed = models.PositiveIntegerField(default=0)
    words_added = models.PositiveIntegerField(default=0)
    words_mastered = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    incorrect_answers = models.PositiveIntegerField(default=0)
    total_time_seconds = models.PositiveIntegerField(default=0)
    goal_completed = models.BooleanField(default=False)
    xp_earned = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "daily_activities"
        unique_together = ["user", "date"]
        ordering = ["-date"]
        verbose_name = "Daily Activity"
        verbose_name_plural = "Daily Activities"

    def __str__(self) -> str:
        return f"Activity for user {self.user_id} on {self.date}"
