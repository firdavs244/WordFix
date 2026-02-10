"""
Shared repository factories and utility providers.
"""

from django.conf import settings

from apps.users.infrastructure.repositories import DjangoUserRepository
from apps.words.domain.services import SpacedRepetitionService
from apps.words.infrastructure.repositories import (
    DjangoChatRepository,
    DjangoDailyActivityRepository,
    DjangoGameSessionRepository,
    DjangoReviewLogRepository,
    DjangoReviewSessionRepository,
    DjangoStreakRepository,
    DjangoTestQuestionRepository,
    DjangoTestSessionRepository,
    DjangoWordCategoryRepository,
    DjangoWordRepository,
)


def get_word_repository() -> DjangoWordRepository:
    return DjangoWordRepository()


def get_category_repository() -> DjangoWordCategoryRepository:
    return DjangoWordCategoryRepository()


def get_session_repository() -> DjangoReviewSessionRepository:
    return DjangoReviewSessionRepository()


def get_log_repository() -> DjangoReviewLogRepository:
    return DjangoReviewLogRepository()


def get_streak_repository() -> DjangoStreakRepository:
    return DjangoStreakRepository()


def get_activity_repository() -> DjangoDailyActivityRepository:
    return DjangoDailyActivityRepository()


def get_sr_service() -> SpacedRepetitionService:
    return SpacedRepetitionService()


def get_user_repository() -> DjangoUserRepository:
    return DjangoUserRepository()


def get_test_session_repository() -> DjangoTestSessionRepository:
    return DjangoTestSessionRepository()


def get_test_question_repository() -> DjangoTestQuestionRepository:
    return DjangoTestQuestionRepository()


def get_game_session_repository() -> DjangoGameSessionRepository:
    return DjangoGameSessionRepository()


def get_chat_repository() -> DjangoChatRepository:
    return DjangoChatRepository()


def _get_ai_provider():
    """Get AI provider (returns None if not configured)."""
    try:
        from core.services.ai.ai_factory import AIProviderFactory
        return AIProviderFactory.get_provider()
    except Exception:
        return None


def _get_tts_provider():
    """Get TTS provider (returns None if not configured)."""
    try:
        from core.services.tts.google_tts import GoogleTTSProvider
        return GoogleTTSProvider()
    except Exception:
        return None


def get_tts_provider():
    """Public accessor for TTS provider."""
    return _get_tts_provider()


def _get_enrich_task():
    """Get enrichment task callable."""
    try:
        from apps.words.infrastructure.tasks import enrich_word_task
        return lambda word_id, user_id: enrich_word_task.delay(word_id, user_id)
    except Exception:
        return None
