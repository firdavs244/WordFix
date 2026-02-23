"""
Dependency injection for archive use cases.
"""

from apps.words.application.use_cases.word_archive import (
    ArchiveWordUseCase,
    BulkArchiveUseCase,
    GetArchivedWordsUseCase,
    UnarchiveWordUseCase,
)
from apps.words.infrastructure.repositories.word_repo import DjangoWordRepository


def get_word_repo():
    return DjangoWordRepository()


def get_archive_use_case():
    return ArchiveWordUseCase(word_repo=get_word_repo())


def get_unarchive_use_case():
    return UnarchiveWordUseCase(word_repo=get_word_repo())


def get_archived_words_use_case():
    return GetArchivedWordsUseCase(word_repo=get_word_repo())


def get_bulk_archive_use_case():
    return BulkArchiveUseCase(word_repo=get_word_repo())
