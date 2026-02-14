"""
User progress, XP, badges, and notification models.
"""

import uuid

from django.db import models

from .user_models import CustomUser


class UserProgress(models.Model):
    """Tracks XP, level, and aggregate stats for a user."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="progress",
    )
    total_xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    words_learned_total = models.PositiveIntegerField(default=0)
    words_mastered_total = models.PositiveIntegerField(default=0)
    tests_completed = models.PositiveIntegerField(default=0)
    games_played = models.PositiveIntegerField(default=0)
    reviews_completed = models.PositiveIntegerField(default=0)
    perfect_scores = models.PositiveIntegerField(default=0)
    total_study_time_seconds = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_progress"
        verbose_name = "User Progress"
        verbose_name_plural = "User Progress"

    def __str__(self) -> str:
        return f"Progress for {self.user.email}: Level {self.level}, {self.total_xp} XP"


class XPTransaction(models.Model):
    """Records each XP award or deduction."""

    REASON_CHOICES = [
        ("word_added", "Word Added"),
        ("review_correct", "Review Correct"),
        ("review_incorrect", "Review Incorrect"),
        ("review_complete", "Review Session Complete"),
        ("review_perfect", "Perfect Review"),
        ("test_complete", "Test Complete"),
        ("test_good", "Test Good Score"),
        ("test_perfect", "Perfect Test"),
        ("game_complete", "Game Complete"),
        ("game_good", "Game Good Score"),
        ("word_mastered", "Word Mastered"),
        ("streak_7", "7-Day Streak"),
        ("streak_30", "30-Day Streak"),
        ("daily_goal", "Daily Goal Complete"),
        ("badge_reward", "Badge Reward"),
        ("level_up", "Level Up"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="xp_transactions",
    )
    amount = models.IntegerField()
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.CharField(max_length=200, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "xp_transactions"
        ordering = ["-created_at"]
        verbose_name = "XP Transaction"
        verbose_name_plural = "XP Transactions"

    def __str__(self) -> str:
        return f"{self.user.email}: {self.amount:+d} XP ({self.reason})"


class Badge(models.Model):
    """Badge definitions."""

    CATEGORY_CHOICES = [
        ("words", "Words"),
        ("streak", "Streak"),
        ("review", "Review"),
        ("test", "Test"),
        ("game", "Game"),
        ("mastery", "Mastery"),
        ("level", "Level"),
    ]

    RARITY_CHOICES = [
        ("common", "Common"),
        ("rare", "Rare"),
        ("epic", "Epic"),
        ("legendary", "Legendary"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=50, default="award")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    xp_reward = models.PositiveIntegerField(default=0)
    rarity = models.CharField(max_length=10, choices=RARITY_CHOICES, default="common")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "badges"
        ordering = ["category", "code"]
        verbose_name = "Badge"
        verbose_name_plural = "Badges"

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class UserBadge(models.Model):
    """Tracks badges earned by users."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="badges",
    )
    badge = models.ForeignKey(
        Badge,
        on_delete=models.CASCADE,
        related_name="user_badges",
    )
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_badges"
        unique_together = ["user", "badge"]
        ordering = ["-earned_at"]
        verbose_name = "User Badge"
        verbose_name_plural = "User Badges"

    def __str__(self) -> str:
        return f"{self.user.email} earned {self.badge.name}"


class Notification(models.Model):
    """User notifications."""

    TYPE_CHOICES = [
        ("review_reminder", "Review Reminder"),
        ("streak_warning", "Streak Warning"),
        ("badge_earned", "Badge Earned"),
        ("level_up", "Level Up"),
        ("daily_goal_complete", "Daily Goal Complete"),
        ("word_mastered", "Word Mastered"),
        ("weekly_report", "Weekly Report"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    type = models.CharField(max_length=25, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self) -> str:
        return f"{self.type}: {self.title} (user={self.user.email})"


class OnboardingQuestion(models.Model):
    """Pre-built level assessment questions."""

    LEVEL_CHOICES = [
        ("A1", "A1"), ("A2", "A2"), ("B1", "B1"),
        ("B2", "B2"), ("C1", "C1"), ("C2", "C2"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=200)
    options = models.JSONField(default=list)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "onboarding_questions"
        ordering = ["level", "order"]
        verbose_name = "Onboarding Question"
        verbose_name_plural = "Onboarding Questions"

    def __str__(self) -> str:
        return f"[{self.level}] {self.question_text[:50]}"


class OnboardingResult(models.Model):
    """User's onboarding test result."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="onboarding_result",
    )
    answers = models.JSONField(default=list)
    determined_level = models.CharField(max_length=2, default="A1")
    completed_at = models.DateTimeField(auto_now_add=True)
    total_correct = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "onboarding_results"
        verbose_name = "Onboarding Result"
        verbose_name_plural = "Onboarding Results"

    def __str__(self) -> str:
        return f"Onboarding: {self.user.email} → {self.determined_level}"
