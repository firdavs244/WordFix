"""
Users infrastructure models package.

Re-exports all models for backward compatibility.
Import from here: ``from apps.users.infrastructure.models import CustomUser``
"""

from .user_models import CustomUser, CustomUserManager  # noqa: F401
from .progress_models import (  # noqa: F401
    Badge,
    Notification,
    OnboardingQuestion,
    OnboardingResult,
    UserBadge,
    UserProgress,
    XPTransaction,
)
from .learning_models import (  # noqa: F401
    DomainCoverage,
    LearningProfile,
    MistakePattern,
    SessionPerformance,
    WordRecommendation,
)

__all__ = [
    "CustomUser",
    "CustomUserManager",
    "UserProgress",
    "XPTransaction",
    "Badge",
    "UserBadge",
    "Notification",
    "OnboardingQuestion",
    "OnboardingResult",
    "LearningProfile",
    "MistakePattern",
    "DomainCoverage",
    "WordRecommendation",
    "SessionPerformance",
]
