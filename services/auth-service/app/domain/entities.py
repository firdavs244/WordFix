"""
User domain entity — pure Python, no framework dependencies.

Mirrors the monolith's UserEntity from apps/users/domain/entities.py.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass
class UserEntity:
    """Core User entity — pure domain object."""

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
        return self.premium_until > datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        """Convert to serializable dict (for API responses)."""
        data = {
            "id": str(self.id),
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "avatar": self.avatar or "",
            "native_language": self.native_language,
            "learning_language": self.learning_language,
            "proficiency_level": self.proficiency_level,
            "daily_goal": self.daily_goal,
            "timezone": self.timezone,
            "is_premium": self.is_premium,
            "is_premium_active": self.is_premium_active,
            "has_completed_onboarding": self.has_completed_onboarding,
            "date_joined": self.date_joined.isoformat() if self.date_joined else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "premium_until": self.premium_until.isoformat() if self.premium_until else None,
        }
        return data
