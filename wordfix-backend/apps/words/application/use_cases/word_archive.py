"""
Word archive use cases: archive, unarchive, list archived, bulk archive.
"""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class ArchiveWordUseCase:
    """Archive a single word."""

    def __init__(self, word_repo):
        self.word_repo = word_repo

    def execute(self, user_id, word_id) -> dict:
        user_id = UUID(str(user_id))
        word_id = UUID(str(word_id))
        word = self.word_repo.archive_word(user_id, word_id)
        return {
            "id": str(word.id),
            "original_word": word.original_word,
            "is_archived": word.is_archived,
            "archived_at": word.archived_at.isoformat() if word.archived_at else None,
        }


class UnarchiveWordUseCase:
    """Unarchive a single word."""

    def __init__(self, word_repo):
        self.word_repo = word_repo

    def execute(self, user_id, word_id) -> dict:
        user_id = UUID(str(user_id))
        word_id = UUID(str(word_id))
        word = self.word_repo.unarchive_word(user_id, word_id)
        return {
            "id": str(word.id),
            "original_word": word.original_word,
            "is_archived": word.is_archived,
        }


class GetArchivedWordsUseCase:
    """Get list of archived words for a user."""

    def __init__(self, word_repo):
        self.word_repo = word_repo

    def execute(self, user_id, page: int = 1, page_size: int = 20) -> dict:
        user_id = UUID(str(user_id))
        words, total = self.word_repo.get_archived_words(user_id, page, page_size)
        return {
            "words": words,
            "total": total,
            "page": page,
            "page_size": page_size,
        }


class BulkArchiveUseCase:
    """Archive multiple words at once."""

    def __init__(self, word_repo):
        self.word_repo = word_repo

    def execute(self, user_id, word_ids: list) -> dict:
        user_id = UUID(str(user_id))
        uuid_ids = [UUID(str(wid)) for wid in word_ids]
        count = self.word_repo.bulk_archive(user_id, uuid_ids)
        return {
            "archived_count": count,
        }
