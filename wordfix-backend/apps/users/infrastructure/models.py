"""
Custom User model for WordFix.

Uses email as the primary identifier with UUID primary key.
"""

import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Custom user manager that uses email as the unique identifier."""

    def create_user(self, email: str, username: str, password: str | None = None, **extra_fields):
        """Create and return a regular user."""
        if not email:
            raise ValueError("Email is required.")
        if not username:
            raise ValueError("Username is required.")

        email = self.normalize_email(email).strip().lower()
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, username: str, password: str | None = None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email as the primary identifier."""

    PROFICIENCY_CHOICES = [
        ("A1", "Beginner"),
        ("A2", "Elementary"),
        ("B1", "Intermediate"),
        ("B2", "Upper Intermediate"),
        ("C1", "Advanced"),
        ("C2", "Proficient"),
    ]

    username_validator = RegexValidator(
        regex=r"^[a-zA-Z0-9_]+$",
        message="Username can only contain letters, numbers, and underscores.",
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[username_validator],
    )
    full_name = models.CharField(max_length=100, blank=True, default="")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    native_language = models.CharField(max_length=10, default="uz")
    learning_language = models.CharField(max_length=10, default="en")
    proficiency_level = models.CharField(
        max_length=2,
        choices=PROFICIENCY_CHOICES,
        default="A1",
    )
    daily_goal = models.PositiveIntegerField(default=10)
    timezone = models.CharField(max_length=50, default="Asia/Tashkent")
    is_premium = models.BooleanField(default=False)
    premium_until = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"
        ordering = ["-date_joined"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email

    @property
    def is_premium_active(self) -> bool:
        """Check if premium subscription is currently active."""
        if not self.is_premium:
            return False
        if self.premium_until is None:
            return True
        return self.premium_until > timezone.now()

    def clean(self) -> None:
        super().clean()
        if self.email:
            self.email = self.email.strip().lower()


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
