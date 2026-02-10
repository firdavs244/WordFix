"""
Enrichment use-case factories and task helpers.
"""

from django.conf import settings

from apps.words.application.use_cases import (
    BatchEnrichUseCase,
    EnrichWordUseCase,
)
from .common_deps import (
    _get_ai_provider,
    _get_tts_provider,
    get_user_repository,
    get_word_repository,
)


def _get_distractor_task():
    """Get distractor generation task callable."""
    try:
        from apps.words.infrastructure.tasks import generate_distractors_task
        return lambda word_id, user_id: generate_distractors_task.delay(word_id, user_id)
    except Exception:
        return None


def get_enrich_use_case() -> EnrichWordUseCase:
    from core.services.ai.prompts import NATIVE_LANGUAGE_MAP, WORD_ENRICHMENT_PROMPT

    return EnrichWordUseCase(
        word_repo=get_word_repository(),
        ai_provider=_get_ai_provider(),
        tts_provider=_get_tts_provider(),
        user_repo=get_user_repository(),
        media_root=str(settings.MEDIA_ROOT),
        media_url=str(settings.MEDIA_URL),
        prompt_template=WORD_ENRICHMENT_PROMPT,
        language_map=NATIVE_LANGUAGE_MAP,
        distractor_task=_get_distractor_task(),
    )


def get_batch_enrich_use_case() -> BatchEnrichUseCase:
    return BatchEnrichUseCase(
        word_repo=get_word_repository(),
        ai_provider=_get_ai_provider(),
        tts_provider=_get_tts_provider(),
    )


def get_enrich_word_task():
    """Get single-word enrichment task callable (returns None if unavailable)."""
    try:
        from apps.words.infrastructure.tasks import enrich_word_task
        return lambda word_id, user_id: enrich_word_task.delay(word_id, user_id)
    except Exception:
        return None


def get_batch_enrich_task():
    """Get batch enrichment task callable (returns None if unavailable)."""
    try:
        from apps.words.infrastructure.tasks import batch_enrich_task
        return lambda user_id, word_ids: batch_enrich_task.delay(user_id, word_ids)
    except Exception:
        return None


def get_pending_enrichment_word_ids(user_id) -> list:
    """Query word IDs pending enrichment for a user."""
    from apps.words.infrastructure.models import Word
    return list(
        Word.objects.filter(
            user_id=user_id,
            enrichment_status__in=["pending", "failed"],
        ).values_list("id", flat=True)
    )
