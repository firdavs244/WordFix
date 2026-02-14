"""
Word and category repository interfaces.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from ..entities import (
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
