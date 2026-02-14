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
    has_completed_onboarding = models.BooleanField(default=False)
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
