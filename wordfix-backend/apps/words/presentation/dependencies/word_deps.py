"""
Word CRUD use-case factories.
"""

from django.conf import settings

from apps.words.application.use_cases import (
    AddWordUseCase,
    BulkAddWordsUseCase,
    DeleteWordUseCase,
    GetWordDetailUseCase,
    GetWordStatsUseCase,
    GetWordsUseCase,
    SearchWordsUseCase,
    UpdateWordUseCase,
)
from .common_deps import _get_enrich_task, get_word_repository


def get_add_word_use_case() -> AddWordUseCase:
    return AddWordUseCase(
        repository=get_word_repository(),
        enrich_task=_get_enrich_task(),
        enrichment_enabled=getattr(settings, 'WORD_ENRICHMENT_ENABLED', True),
    )


def get_words_use_case() -> GetWordsUseCase:
    return GetWordsUseCase(get_word_repository())


def get_word_detail_use_case() -> GetWordDetailUseCase:
    return GetWordDetailUseCase(get_word_repository())


def get_update_word_use_case() -> UpdateWordUseCase:
    return UpdateWordUseCase(get_word_repository())


def get_delete_word_use_case() -> DeleteWordUseCase:
    return DeleteWordUseCase(get_word_repository())


def get_bulk_add_words_use_case() -> BulkAddWordsUseCase:
    return BulkAddWordsUseCase(get_word_repository())


def get_word_stats_use_case() -> GetWordStatsUseCase:
    return GetWordStatsUseCase(get_word_repository())


def get_search_words_use_case() -> SearchWordsUseCase:
    return SearchWordsUseCase(get_word_repository())
