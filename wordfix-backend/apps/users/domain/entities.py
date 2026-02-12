"""
User domain entities.

Pure Python classes with no Django dependencies.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone as tz
from uuid import UUID, uuid4


@dataclass
class UserEntity:
    """
    Core User entity - pure domain object.
    """

    id: UUID = field(default_factory=uuid4)
    email: str = ""
    username: str = ""
    full_name: str = ""
    avatar: str = ""
    native_language: str = "uz"
    learning_language: str = "en"
    proficiency_level: str = "A1"
    daily_goal: int = 10
    timezone: str = "Asia/Tashkent"
    is_premium: bool = False
    premium_until: datetime | None = None
    is_active: bool = True
    is_staff: bool = False
    has_completed_onboarding: bool = False
    date_joined: datetime | None = None
    last_login: datetime | None = None

    @property
    def is_premium_active(self) -> bool:
        """Check if premium subscription is currently active."""
        if not self.is_premium:
            return False
        if self.premium_until is None:
            return True
        return self.premium_until > datetime.now(tz.utc)

    def validate_email(self) -> None:
        """Validate email format."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not self.email or not re.match(pattern, self.email):
            raise ValueError(f"Invalid email format: {self.email}")

    def validate_username(self) -> None:
        """Validate username format."""
        if not self.username:
            raise ValueError("Username is required.")
        if len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        if len(self.username) > 30:
            raise ValueError("Username must be at most 30 characters long.")
        if not re.match(r"^[a-zA-Z0-9_]+$", self.username):
            raise ValueError(
                "Username can only contain letters, numbers, and underscores."
            )
