"""
Word domain repository interfaces package.

Re-exports all abstract repository classes for backward compatibility.
Import from here: ``from apps.words.domain.repositories import AbstractWordRepository``
"""

from .word_repositories import (  # noqa: F401
    AbstractWordCategoryRepository,
    AbstractWordRepository,
)
from .session_repositories import (  # noqa: F401
    AbstractChatRepository,
    AbstractConfusingPairRepository,
    AbstractDailyActivityRepository,
    AbstractDailyChallengeRepository,
    AbstractDailyStreakRepository,
    AbstractGameSessionRepository,
    AbstractReviewLogRepository,
    AbstractReviewSessionRepository,
    AbstractTestQuestionRepository,
    AbstractTestSessionRepository,
    AbstractWordDistractorRepository,
)

__all__ = [
    "AbstractWordRepository",
    "AbstractWordCategoryRepository",
    "AbstractReviewSessionRepository",
    "AbstractReviewLogRepository",
    "AbstractDailyStreakRepository",
    "AbstractDailyActivityRepository",
    "AbstractTestSessionRepository",
    "AbstractTestQuestionRepository",
    "AbstractGameSessionRepository",
    "AbstractChatRepository",
    "AbstractConfusingPairRepository",
    "AbstractDailyChallengeRepository",
    "AbstractWordDistractorRepository",
]
