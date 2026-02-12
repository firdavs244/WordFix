"""
Celery tasks for word enrichment and scheduled operations.
"""

import logging

from celery import shared_task

from core.interfaces.ai_provider import AIProviderError

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    rate_limit="10/m",
)
def enrich_word_task(self, word_id: str, user_id: str):
    """Enrich a single word with AI data."""
    from apps.words.presentation.dependencies import get_enrich_use_case

    try:
        use_case = get_enrich_use_case()
        use_case.execute(word_id, user_id)
        logger.info(f"Successfully enriched word {word_id}")
    except AIProviderError as e:
        logger.warning(f"AI provider error enriching word {word_id}: {e}")
        try:
            self.retry(exc=e)
        except self.MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for word {word_id}")
            _mark_word_failed(word_id, user_id, str(e))
    except Exception as e:
        logger.error(f"Unexpected error enriching word {word_id}: {e}")
        _mark_word_failed(word_id, user_id, str(e))


@shared_task(rate_limit="20/m")
def generate_audio_task(word_id: str, user_id: str):
    """Generate TTS audio for a word."""
    from apps.words.presentation.dependencies import get_tts_provider, get_word_repository

    try:
        import os
        from django.conf import settings

        repo = get_word_repository()
        from uuid import UUID
        word = repo.get_by_id(word_id=UUID(word_id), user_id=UUID(user_id))

        tts = get_tts_provider()
        audio_bytes = tts.generate_audio(word.original_word)

        audio_dir = os.path.join(
            str(settings.MEDIA_ROOT), "audio", "words", user_id, word_id
        )
        os.makedirs(audio_dir, exist_ok=True)
        audio_path = os.path.join(audio_dir, "pronunciation.mp3")
        with open(audio_path, "wb") as f:
            f.write(audio_bytes)

        audio_url = f"{settings.MEDIA_URL}audio/words/{user_id}/{word_id}/pronunciation.mp3"
        repo.update(
            word_id=UUID(word_id), user_id=UUID(user_id), audio_url=audio_url
        )
        logger.info(f"Generated audio for word {word_id}")
    except Exception as e:
        logger.error(f"Audio generation failed for word {word_id}: {e}")


@shared_task
def batch_enrich_task(user_id: str, word_ids: list):
    """Enrich multiple words in batch."""
    from apps.words.presentation.dependencies import get_batch_enrich_use_case

    try:
        use_case = get_batch_enrich_use_case()
        result = use_case.execute(user_id, word_ids)
        logger.info(
            f"Batch enrichment: {result['enriched']} enriched, {result['failed']} failed"
        )
        return result
    except Exception as e:
        logger.error(f"Batch enrichment failed: {e}")
        return {"enriched": 0, "failed": len(word_ids), "errors": [str(e)]}


def _mark_word_failed(word_id: str, user_id: str, error: str):
    """Mark word enrichment as failed."""
    try:
        from apps.words.presentation.dependencies import get_word_repository
        from uuid import UUID
        repo = get_word_repository()
        repo.update(
            word_id=UUID(word_id), user_id=UUID(user_id),
            enrichment_status="failed", enrichment_error=error,
        )
    except Exception as e:
        logger.error(f"Failed to mark word {word_id} as failed: {e}")


@shared_task
def update_streaks_task():
    """Check and reset streaks for users who missed a day.
    
    Scheduled via Celery Beat (daily).
    """
    from datetime import date, timedelta
    from apps.words.infrastructure.models import DailyStreak

    yesterday = date.today() - timedelta(days=1)
    stale = DailyStreak.objects.filter(
        last_activity_date__lt=yesterday,
        current_streak__gt=0,
    ).exclude(
        streak_frozen_until__gte=date.today(),
    )

    count = stale.update(current_streak=0)
    logger.info(f"Reset {count} stale streaks")


@shared_task
def cleanup_stale_sessions_task():
    """Complete sessions that have been open for more than 2 hours.

    Scheduled via Celery Beat (hourly).
    """
    from django.utils import timezone
    from datetime import timedelta
    from apps.words.infrastructure.models import ReviewSession, GameSession

    cutoff = timezone.now() - timedelta(hours=2)

    # Clean up stale review sessions
    stale_reviews = ReviewSession.objects.filter(
        is_completed=False,
        started_at__lt=cutoff,
    )

    review_count = 0
    for session in stale_reviews:
        duration = int((timezone.now() - session.started_at).total_seconds())
        session.is_completed = True
        session.completed_at = timezone.now()
        session.duration_seconds = duration
        session.save()
        review_count += 1

    # Clean up stale game sessions (1 hour for games)
    game_cutoff = timezone.now() - timedelta(hours=1)
    stale_games = GameSession.objects.filter(
        is_completed=False,
        started_at__lt=game_cutoff,
    )

    game_count = 0
    for session in stale_games:
        session.is_completed = True
        session.completed_at = timezone.now()
        session.score = 0
        session.save()
        game_count += 1

    logger.info(
        f"Cleaned up {review_count} stale review sessions, "
        f"{game_count} stale game sessions"
    )


@shared_task(
    bind=True,
    max_retries=2,
    default_retry_delay=30,
)
def generate_distractors_task(self, word_id: str, user_id: str):
    """Generate smart distractors for a word. Called after enrichment."""
    try:
        from apps.words.presentation.dependencies import get_distractor_service
        from uuid import UUID

        service = get_distractor_service()
        from apps.words.presentation.dependencies import get_word_repository, get_user_repository
        word_repo = get_word_repository()
        word = word_repo.get_by_id(word_id=UUID(word_id), user_id=UUID(user_id))

        # Get user language info
        native_lang = "Uzbek"
        user_level = "B1"
        try:
            user_repo = get_user_repository()
            from core.services.ai.prompts import NATIVE_LANGUAGE_MAP
            user_info = user_repo.get_user_language_info(UUID(user_id))
            native_lang = NATIVE_LANGUAGE_MAP.get(
                user_info.get("native_language", "uz"), "Uzbek"
            )
            user_level = user_info.get("proficiency_level", "B1")
        except Exception:
            pass

        service.generate_distractors(
            word_id=UUID(word_id),
            word=word.original_word,
            translation=word.translation,
            part_of_speech=word.part_of_speech,
            synonyms=word.synonyms or [],
            difficulty=word.difficulty_level,
            user_id=UUID(user_id),
            user_level=user_level,
            native_language=native_lang,
        )
        logger.info(f"Generated distractors for word {word_id}")
    except Exception as e:
        logger.error(f"Distractor generation failed for word {word_id}: {e}")
        try:
            self.retry(exc=e)
        except self.MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for distractor generation: {word_id}")


@shared_task
def generate_daily_challenges_task():
    """Generate daily challenges for all active users. Run daily at 00:01."""
    from apps.users.infrastructure.models import CustomUser, UserProgress
    from apps.words.infrastructure.models import Word
    from apps.words.domain.services import DailyChallengeService
    from apps.words.infrastructure.repositories import DjangoDailyChallengeRepository

    repo = DjangoDailyChallengeRepository()
    users = CustomUser.objects.filter(is_active=True)
    created_count = 0

    for user in users:
        try:
            # Get user level
            try:
                progress = UserProgress.objects.get(user=user)
                level = progress.level
            except UserProgress.DoesNotExist:
                level = 1

            word_count = Word.objects.filter(user_id=user.id).count()
            challenges = DailyChallengeService.generate_daily_challenges(level, word_count)

            _, created = repo.get_or_create_today(
                user_id=user.id,
                challenges=challenges,
            )
            if created:
                created_count += 1
        except Exception as e:
            logger.error(f"Failed to generate challenges for user {user.id}: {e}")

    logger.info(f"Generated daily challenges for {created_count} users")
