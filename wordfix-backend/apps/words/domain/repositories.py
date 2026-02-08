"""
Word domain repository interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from .entities import (
    DailyActivityEntity,
    DailyStreakEntity,
    GameSessionEntity,
    ReviewLogEntity,
    ReviewSessionEntity,
    TestQuestionEntity,
    TestSessionEntity,
    WordCategoryEntity,
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
