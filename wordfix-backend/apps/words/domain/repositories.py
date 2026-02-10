"""
Word domain repository interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from .entities import (
    ChatMessageEntity,
    ChatSessionEntity,
    ConfusingPairEntity,
    DailyActivityEntity,
    DailyChallengeEntity,
    DailyStreakEntity,
    GameSessionEntity,
    ReviewLogEntity,
    ReviewSessionEntity,
    TestQuestionEntity,
    TestSessionEntity,
    WordCategoryEntity,
    WordDistractorEntity,
    WordEntity,
)


class AbstractWordRepository(ABC):
    """Abstract repository interface for Word entity."""

    @abstractmethod
    def get_by_id(self, word_id: UUID, user_id: UUID) -> WordEntity:
        ...

    @abstractmethod
    def get_all_by_user(
        self, user_id: UUID, filters: dict | None = None,
        ordering: str = "-created_at", page: int = 1, page_size: int = 20,
    ) -> tuple[list[WordEntity], int]:
        ...

    @abstractmethod
    def create(self, user_id: UUID, **kwargs) -> WordEntity:
        ...

    @abstractmethod
    def update(self, word_id: UUID, user_id: UUID, **kwargs) -> WordEntity:
        ...

    @abstractmethod
    def delete(self, word_id: UUID, user_id: UUID) -> None:
        ...

    @abstractmethod
    def exists(self, original_word: str, user_id: UUID) -> bool:
        ...

    @abstractmethod
    def get_count_by_user(self, user_id: UUID) -> int:
        ...

    @abstractmethod
    def search(
        self, user_id: UUID, query: str, page: int = 1, page_size: int = 20,
    ) -> tuple[list[WordEntity], int]:
        ...

    @abstractmethod
    def get_by_category(self, user_id: UUID, category_id: UUID) -> list[WordEntity]:
        ...

    @abstractmethod
    def get_words_for_review(self, user_id: UUID) -> list[WordEntity]:
        ...

    @abstractmethod
    def get_review_words(
        self, user_id: UUID, limit: int = 20, session_type: str = "review",
    ) -> list[WordEntity]:
        """Get words due for review based on session type."""
        ...

    @abstractmethod
    def get_review_summary_stats(self, user_id: UUID) -> dict:
        """Get review summary statistics for a user."""
        ...

    @abstractmethod
    def bulk_create(self, user_id: UUID, words_data: list[dict]) -> dict:
        ...

    @abstractmethod
    def get_stats(self, user_id: UUID) -> dict:
        ...


class AbstractWordCategoryRepository(ABC):
    """Abstract repository for WordCategory."""

    @abstractmethod
    def get_all_by_user(self, user_id: UUID) -> list[WordCategoryEntity]:
        ...

    @abstractmethod
    def create(self, user_id: UUID, **kwargs) -> WordCategoryEntity:
        ...

    @abstractmethod
    def delete(self, category_id: UUID, user_id: UUID) -> None:
        ...

    @abstractmethod
    def exists(self, name: str, user_id: UUID) -> bool:
        ...

    @abstractmethod
    def update_words_count(self, category_id: UUID) -> None:
        ...


class AbstractReviewSessionRepository(ABC):
    """Abstract repository for ReviewSession."""

    @abstractmethod
    def create(self, user_id: UUID, **kwargs) -> ReviewSessionEntity:
        ...

    @abstractmethod
    def get_by_id(self, session_id: UUID, user_id: UUID) -> ReviewSessionEntity:
        ...

    @abstractmethod
    def update(self, session_id: UUID, **kwargs) -> ReviewSessionEntity:
        ...

    @abstractmethod
    def get_by_user(self, user_id: UUID, page: int = 1, page_size: int = 20) -> tuple[list[ReviewSessionEntity], int]:
        ...


class AbstractReviewLogRepository(ABC):
    """Abstract repository for ReviewLog."""

    @abstractmethod
    def create(self, **kwargs) -> ReviewLogEntity:
        ...

    @abstractmethod
    def get_by_session(self, session_id: UUID) -> list[ReviewLogEntity]:
        ...

    @abstractmethod
    def get_by_user(self, user_id: UUID, page: int = 1, page_size: int = 20) -> tuple[list[ReviewLogEntity], int]:
        ...


class AbstractDailyStreakRepository(ABC):
    """Abstract repository for DailyStreak."""

    @abstractmethod
    def get_or_create(self, user_id: UUID) -> DailyStreakEntity:
        ...

    @abstractmethod
    def update(self, streak_id: UUID, **kwargs) -> DailyStreakEntity:
        ...


class AbstractDailyActivityRepository(ABC):
    """Abstract repository for DailyActivity."""

    @abstractmethod
    def get_or_create_today(self, user_id: UUID) -> DailyActivityEntity:
        ...

    @abstractmethod
    def update(self, activity_id: UUID, **kwargs) -> DailyActivityEntity:
        ...

    @abstractmethod
    def get_by_date_range(self, user_id: UUID, start_date, end_date) -> list[DailyActivityEntity]:
        ...


class AbstractTestSessionRepository(ABC):
    """Abstract repository for TestSession."""

    @abstractmethod
    def create(self, user_id: UUID, **kwargs) -> TestSessionEntity:
        ...

    @abstractmethod
    def get_by_id(self, session_id: UUID, user_id: UUID) -> TestSessionEntity:
        ...

    @abstractmethod
    def update(self, session_id: UUID, **kwargs) -> TestSessionEntity:
        ...

    @abstractmethod
    def get_by_user(self, user_id: UUID, page: int = 1, page_size: int = 20) -> tuple[list[TestSessionEntity], int]:
        ...


class AbstractTestQuestionRepository(ABC):
    """Abstract repository for TestQuestion."""

    @abstractmethod
    def create(self, **kwargs) -> TestQuestionEntity:
        ...

    @abstractmethod
    def bulk_create(self, questions_data: list[dict]) -> list[TestQuestionEntity]:
        ...

    @abstractmethod
    def get_by_id(self, question_id: UUID) -> TestQuestionEntity:
        ...

    @abstractmethod
    def get_by_session(self, session_id: UUID) -> list[TestQuestionEntity]:
        ...

    @abstractmethod
    def update(self, question_id: UUID, **kwargs) -> TestQuestionEntity:
        ...


class AbstractGameSessionRepository(ABC):
    """Abstract repository for GameSession."""

    @abstractmethod
    def create(self, user_id: UUID, **kwargs) -> GameSessionEntity:
        ...

    @abstractmethod
    def get_by_id(self, session_id: UUID, user_id: UUID) -> GameSessionEntity:
        ...

    @abstractmethod
    def update(self, session_id: UUID, **kwargs) -> GameSessionEntity:
        ...

    @abstractmethod
    def get_by_user(self, user_id: UUID, page: int = 1, page_size: int = 20) -> tuple[list[GameSessionEntity], int]:
        ...

    @abstractmethod
    def get_stats(self, user_id: UUID) -> dict:
        ...


class AbstractChatRepository(ABC):
    """Abstract repository for Chat sessions and messages."""

    @abstractmethod
    def create_session(self, user_id: UUID, topic: str = "", target_words: list | None = None) -> ChatSessionEntity:
        ...

    @abstractmethod
    def get_session(self, session_id: UUID, user_id: UUID) -> ChatSessionEntity:
        ...

    @abstractmethod
    def update_session(self, session_id: UUID, **kwargs) -> ChatSessionEntity:
        ...

    @abstractmethod
    def end_session(self, session_id: UUID) -> ChatSessionEntity:
        ...

    @abstractmethod
    def get_sessions_by_user(self, user_id: UUID, page: int = 1, page_size: int = 20) -> tuple[list[ChatSessionEntity], int]:
        ...

    @abstractmethod
    def add_message(self, session_id: UUID, role: str, content: str, corrections: list | None = None,
                    words_used: list | None = None, order: int = 0) -> ChatMessageEntity:
        ...

    @abstractmethod
    def get_messages(self, session_id: UUID, limit: int | None = None) -> list[ChatMessageEntity]:
        ...

    @abstractmethod
    def add_words_practiced(self, session_id: UUID, words: list[str]) -> None:
        ...


class AbstractConfusingPairRepository(ABC):
    """Abstract repository for ConfusingPair."""

    @abstractmethod
    def get_or_create(self, user_id: UUID, word_1_id: UUID, word_2_id: UUID) -> tuple[ConfusingPairEntity, bool]:
        ...

    @abstractmethod
    def increment_confusion(self, pair_id: UUID) -> ConfusingPairEntity:
        ...

    @abstractmethod
    def get_by_user(self, user_id: UUID, include_resolved: bool = False) -> list[ConfusingPairEntity]:
        ...

    @abstractmethod
    def get_by_id(self, pair_id: UUID, user_id: UUID) -> ConfusingPairEntity:
        ...

    @abstractmethod
    def update(self, pair_id: UUID, **kwargs) -> ConfusingPairEntity:
        ...

    @abstractmethod
    def resolve(self, pair_id: UUID) -> ConfusingPairEntity:
        ...

    @abstractmethod
    def get_unresolved_count(self, user_id: UUID) -> int:
        ...


class AbstractDailyChallengeRepository(ABC):
    """Abstract repository for DailyChallenge."""

    @abstractmethod
    def get_or_create_today(self, user_id: UUID, challenges: list | None = None) -> tuple[DailyChallengeEntity, bool]:
        ...

    @abstractmethod
    def update(self, challenge_id: UUID, **kwargs) -> DailyChallengeEntity:
        ...

    @abstractmethod
    def get_by_date(self, user_id: UUID, date) -> DailyChallengeEntity | None:
        ...

    @abstractmethod
    def get_consecutive_completed_days(self, user_id: UUID) -> int:
        ...


class AbstractWordDistractorRepository(ABC):
    """Abstract repository for WordDistractor."""

    @abstractmethod
    def get_by_word(self, word_id: UUID, language: str = "uz") -> WordDistractorEntity | None:
        ...

    @abstractmethod
    def create(self, word_id: UUID, distractors: list, language: str = "uz",
               generated_by: str = "ai") -> WordDistractorEntity:
        ...

    @abstractmethod
    def update_or_create(self, word_id: UUID, distractors: list, language: str = "uz",
                         generated_by: str = "ai") -> WordDistractorEntity:
        ...
