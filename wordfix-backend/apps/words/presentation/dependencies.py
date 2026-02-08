"""
Word dependency injection.

Infrastructure concern: wires concrete implementations into use cases.
"""

from django.conf import settings

from apps.users.infrastructure.repositories import DjangoUserRepository
from apps.words.application.use_cases import (
    AddWordUseCase,
    BatchEnrichUseCase,
    BulkAddWordsUseCase,
    CompleteReviewSessionUseCase,
    CompleteTestSessionUseCase,
    DeleteWordUseCase,
    EnrichWordUseCase,
    GenerateTestUseCase,
    GetGameHistoryUseCase,
    GetGameStatsUseCase,
    GetReviewSummaryUseCase,
    GetReviewWordsUseCase,
    GetTestDetailUseCase,
    GetTestHistoryUseCase,
    GetWordDetailUseCase,
    GetWordStatsUseCase,
    GetWordsUseCase,
    SearchWordsUseCase,
    StartReviewSessionUseCase,
    StartSpeedRoundUseCase,
    StartWordContextUseCase,
    StartWordMatchUseCase,
    SubmitReviewAnswerUseCase,
    SubmitSpeedRoundUseCase,
    SubmitTestAnswerUseCase,
    SubmitWordContextUseCase,
    SubmitWordMatchUseCase,
    UpdateStreakUseCase,
    UpdateWordUseCase,
)
from apps.words.domain.services import SpacedRepetitionService
from apps.words.infrastructure.repositories import (
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


def get_user_repository() -> DjangoUserRepository:
    return DjangoUserRepository()


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
    )


def get_batch_enrich_use_case() -> BatchEnrichUseCase:
    return BatchEnrichUseCase(
        word_repo=get_word_repository(),
        ai_provider=_get_ai_provider(),
        tts_provider=_get_tts_provider(),
    )


def get_review_words_use_case() -> GetReviewWordsUseCase:
    return GetReviewWordsUseCase(word_repo=get_word_repository())


def get_start_session_use_case() -> StartReviewSessionUseCase:
    return StartReviewSessionUseCase(session_repo=get_session_repository())


def get_submit_answer_use_case() -> SubmitReviewAnswerUseCase:
    return SubmitReviewAnswerUseCase(
        word_repo=get_word_repository(),
        session_repo=get_session_repository(),
        log_repo=get_log_repository(),
        sr_service=get_sr_service(),
        streak_repo=get_streak_repository(),
        activity_repo=get_activity_repository(),
    )


def get_complete_session_use_case() -> CompleteReviewSessionUseCase:
    return CompleteReviewSessionUseCase(
        session_repo=get_session_repository(),
        log_repo=get_log_repository(),
    )


def get_review_summary_use_case() -> GetReviewSummaryUseCase:
    return GetReviewSummaryUseCase(
        word_repo=get_word_repository(),
        streak_repo=get_streak_repository(),
        activity_repo=get_activity_repository(),
        user_repo=get_user_repository(),
    )


def get_update_streak_use_case() -> UpdateStreakUseCase:
    return UpdateStreakUseCase(streak_repo=get_streak_repository())


# =============================================================================
# TASK HELPERS (keep infrastructure imports out of views)
# =============================================================================


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


# =============================================================================
# TEST USE-CASE FACTORIES
# =============================================================================


def get_test_session_repository() -> DjangoTestSessionRepository:
    return DjangoTestSessionRepository()


def get_test_question_repository() -> DjangoTestQuestionRepository:
    return DjangoTestQuestionRepository()


def get_game_session_repository() -> DjangoGameSessionRepository:
    return DjangoGameSessionRepository()


def get_generate_test_use_case() -> GenerateTestUseCase:
    from core.services.ai.prompts import (
        CONTEXT_GUESS_PROMPT,
        FILL_BLANK_PROMPT,
        MULTIPLE_CHOICE_PROMPT,
        NATIVE_LANGUAGE_MAP,
    )

    return GenerateTestUseCase(
        word_repo=get_word_repository(),
        test_session_repo=get_test_session_repository(),
        test_question_repo=get_test_question_repository(),
        ai_provider=_get_ai_provider(),
        user_repo=get_user_repository(),
        prompt_templates={
            "multiple_choice": MULTIPLE_CHOICE_PROMPT,
            "fill_blank": FILL_BLANK_PROMPT,
            "context_guess": CONTEXT_GUESS_PROMPT,
        },
        language_map=NATIVE_LANGUAGE_MAP,
    )


def get_submit_test_answer_use_case() -> SubmitTestAnswerUseCase:
    return SubmitTestAnswerUseCase(
        question_repo=get_test_question_repository(),
        word_repo=get_word_repository(),
        sr_service=get_sr_service(),
        activity_repo=get_activity_repository(),
    )


def get_complete_test_session_use_case() -> CompleteTestSessionUseCase:
    return CompleteTestSessionUseCase(
        test_session_repo=get_test_session_repository(),
        test_question_repo=get_test_question_repository(),
        activity_repo=get_activity_repository(),
    )


def get_test_history_use_case() -> GetTestHistoryUseCase:
    return GetTestHistoryUseCase(
        test_session_repo=get_test_session_repository(),
    )


def get_test_detail_use_case() -> GetTestDetailUseCase:
    return GetTestDetailUseCase(
        test_session_repo=get_test_session_repository(),
        test_question_repo=get_test_question_repository(),
    )


# =============================================================================
# GAME USE-CASE FACTORIES
# =============================================================================


def get_start_speed_round_use_case() -> StartSpeedRoundUseCase:
    return StartSpeedRoundUseCase(
        word_repo=get_word_repository(),
        game_session_repo=get_game_session_repository(),
    )


def get_submit_speed_round_use_case() -> SubmitSpeedRoundUseCase:
    return SubmitSpeedRoundUseCase(
        word_repo=get_word_repository(),
        game_session_repo=get_game_session_repository(),
        sr_service=get_sr_service(),
        activity_repo=get_activity_repository(),
    )


def get_start_word_match_use_case() -> StartWordMatchUseCase:
    return StartWordMatchUseCase(
        word_repo=get_word_repository(),
        game_session_repo=get_game_session_repository(),
    )


def get_submit_word_match_use_case() -> SubmitWordMatchUseCase:
    return SubmitWordMatchUseCase(
        word_repo=get_word_repository(),
        game_session_repo=get_game_session_repository(),
        sr_service=get_sr_service(),
        activity_repo=get_activity_repository(),
    )


def get_start_word_context_use_case() -> StartWordContextUseCase:
    from core.services.ai.prompts import NATIVE_LANGUAGE_MAP, WORD_CONTEXT_GAME_PROMPT

    return StartWordContextUseCase(
        word_repo=get_word_repository(),
        game_session_repo=get_game_session_repository(),
        ai_provider=_get_ai_provider(),
        user_repo=get_user_repository(),
        prompt_template=WORD_CONTEXT_GAME_PROMPT,
        language_map=NATIVE_LANGUAGE_MAP,
    )


def get_submit_word_context_use_case() -> SubmitWordContextUseCase:
    return SubmitWordContextUseCase(
        word_repo=get_word_repository(),
        game_session_repo=get_game_session_repository(),
        sr_service=get_sr_service(),
        activity_repo=get_activity_repository(),
    )


def get_game_history_use_case() -> GetGameHistoryUseCase:
    return GetGameHistoryUseCase(
        game_session_repo=get_game_session_repository(),
    )


def get_game_stats_use_case() -> GetGameStatsUseCase:
    return GetGameStatsUseCase(
        game_session_repo=get_game_session_repository(),
    )
