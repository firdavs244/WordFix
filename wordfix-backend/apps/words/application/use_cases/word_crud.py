"""
Word CRUD use cases.
"""

import logging
from uuid import UUID

from apps.common.exceptions import ValidationError
from apps.words.domain.repositories import AbstractWordRepository

logger = logging.getLogger(__name__)

from typing import Callable


class AddWordUseCase:
    """Add a new word to user's word bank."""

    def __init__(
        self,
        repository: AbstractWordRepository,
        enrich_task: Callable | None = None,
        enrichment_enabled: bool = True,
    ):
        self.repository = repository
        self.enrich_task = enrich_task
        self.enrichment_enabled = enrichment_enabled

    def execute(self, user_id: UUID, data: dict):
        """Validate and create a word. Triggers auto-enrichment if enabled."""
        original_word = data.get("original_word", "").strip().lower()
        if not original_word:
            raise ValidationError("Word is required.")

        word = self.repository.create(user_id=user_id, **data)

        # Trigger auto-enrichment
        if self.enrichment_enabled and self.enrich_task:
            try:
                self.enrich_task(str(word.id), str(user_id))
            except Exception as e:
                logger.warning(f"Failed to queue enrichment task: {e}")

        return word


class GetWordsUseCase:
    """Get paginated words list with filters."""

    def __init__(self, repository: AbstractWordRepository):
        self.repository = repository

    def execute(self, user_id: UUID, filters=None, ordering="-created_at", page=1, page_size=20):
        return self.repository.get_all_by_user(
            user_id=user_id, filters=filters, ordering=ordering,
            page=page, page_size=page_size,
        )


class GetWordDetailUseCase:
    """Get a single word detail."""

    def __init__(self, repository: AbstractWordRepository):
        self.repository = repository

    def execute(self, word_id: UUID, user_id: UUID):
        return self.repository.get_by_id(word_id=word_id, user_id=user_id)


class UpdateWordUseCase:
    """Update a word (partial)."""

    def __init__(self, repository: AbstractWordRepository):
        self.repository = repository

    def execute(self, word_id: UUID, user_id: UUID, data: dict):
        data.pop("original_word", None)
        return self.repository.update(word_id=word_id, user_id=user_id, **data)


class DeleteWordUseCase:
    """Delete a word permanently."""

    def __init__(self, repository: AbstractWordRepository):
        self.repository = repository

    def execute(self, word_id: UUID, user_id: UUID) -> None:
        self.repository.delete(word_id=word_id, user_id=user_id)


class BulkAddWordsUseCase:
    """Bulk add words."""

    def __init__(self, repository: AbstractWordRepository):
        self.repository = repository

    def execute(self, user_id: UUID, words_data: list[dict]) -> dict:
        return self.repository.bulk_create(user_id=user_id, words_data=words_data)


class GetWordStatsUseCase:
    """Get word stats for a user."""

    def __init__(self, repository: AbstractWordRepository):
        self.repository = repository

    def execute(self, user_id: UUID) -> dict:
        return self.repository.get_stats(user_id=user_id)


class SearchWordsUseCase:
    """Search words."""

    def __init__(self, repository: AbstractWordRepository):
        self.repository = repository

    def execute(self, user_id: UUID, query: str, page: int = 1, page_size: int = 20):
        return self.repository.search(
            user_id=user_id, query=query, page=page, page_size=page_size,
        )
