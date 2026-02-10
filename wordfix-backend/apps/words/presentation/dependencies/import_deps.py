"""
Smart import use-case factories.
"""

from django.conf import settings

from apps.words.application.use_cases import (
    AnalyzeTextUseCase,
    ImportWordsUseCase,
)
from .common_deps import (
    _get_ai_provider,
    _get_enrich_task,
    get_user_repository,
    get_word_repository,
)


def get_analyze_text_use_case() -> AnalyzeTextUseCase:
    from core.services.ai.prompts import NATIVE_LANGUAGE_MAP, SMART_IMPORT_PROMPT

    return AnalyzeTextUseCase(
        word_repo=get_word_repository(),
        ai_provider=_get_ai_provider(),
        user_repo=get_user_repository(),
        prompt_template=SMART_IMPORT_PROMPT,
        language_map=NATIVE_LANGUAGE_MAP,
    )


def get_import_words_use_case() -> ImportWordsUseCase:
    return ImportWordsUseCase(
        word_repo=get_word_repository(),
        enrich_task=_get_enrich_task(),
        enrichment_enabled=getattr(settings, 'WORD_ENRICHMENT_ENABLED', True),
    )
