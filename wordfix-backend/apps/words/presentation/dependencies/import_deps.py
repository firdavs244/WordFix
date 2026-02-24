"""
Smart import use-case factories.
"""

from django.conf import settings

from apps.words.application.use_cases import (
    AnalyzeTextUseCase,
    CSVImportUseCase,
    ImportWordsUseCase,
    ValidateCSVUseCase,
)
from .common_deps import (
    _get_ai_provider,
    _get_enrich_task,
    get_word_repository,
)


def get_analyze_text_use_case() -> AnalyzeTextUseCase:
    return AnalyzeTextUseCase(
        word_repo=get_word_repository(),
        ai_provider=_get_ai_provider(),
    )


def get_import_words_use_case() -> ImportWordsUseCase:
    return ImportWordsUseCase(
        word_repo=get_word_repository(),
        enrich_task=_get_enrich_task(),
        enrichment_enabled=getattr(settings, 'WORD_ENRICHMENT_ENABLED', True),
    )


def get_csv_validate_use_case() -> ValidateCSVUseCase:
    return ValidateCSVUseCase()


def get_csv_import_use_case() -> CSVImportUseCase:
    return CSVImportUseCase(
        word_repo=get_word_repository(),
        enrich_task=_get_enrich_task(),
        enrichment_enabled=getattr(settings, 'WORD_ENRICHMENT_ENABLED', True),
    )
