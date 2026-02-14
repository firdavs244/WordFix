"""
Word domain entities package.

Re-exports all entity classes for backward compatibility.
Import from here: ``from apps.words.domain.entities import WordEntity``
"""

from .word_entities import WordCategoryEntity, WordEntity  # noqa: F401
from .session_entities import (  # noqa: F401
    ChatMessageEntity,
    ChatSessionEntity,
    ConfusingPairEntity,
    DailyActivityEntity,
    DailyChallengeEntity,
    DailyStreakEntity,
    GameSessionEntity,
    ListeningRoundEntity,
    ReviewLogEntity,
    ReviewSessionEntity,
    StoryRoundEntity,
    TestQuestionEntity,
    TestSessionEntity,
    WordDistractorEntity,
)

__all__ = [
    "WordCategoryEntity",
    "WordEntity",
    "ReviewSessionEntity",
    "ReviewLogEntity",
    "DailyStreakEntity",
    "DailyActivityEntity",
    "TestSessionEntity",
    "TestQuestionEntity",
    "GameSessionEntity",
    "ChatSessionEntity",
    "ChatMessageEntity",
    "ConfusingPairEntity",
    "DailyChallengeEntity",
    "WordDistractorEntity",
    "StoryRoundEntity",
    "ListeningRoundEntity",
]
