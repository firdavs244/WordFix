"""
Tests for Celery tasks (EAGER mode).
"""

from datetime import date, timedelta
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from django.utils import timezone

from apps.users.infrastructure.models import CustomUser
from apps.words.infrastructure.models import DailyStreak, ReviewSession, Word


@pytest.fixture
def task_user(db):
    return CustomUser.objects.create_user(
        email="task@test.com",
        username="taskuser",
        password="testpass123",
    )


@pytest.fixture
def task_word(task_user):
    return Word.objects.create(
        user=task_user,
        original_word="taskword",
        translation="task tarjima",
        enrichment_status="pending",
    )


# =============================================================================
# ENRICH WORD TASK
# =============================================================================


@pytest.mark.django_db
class TestEnrichWordTask:
    @patch("apps.words.presentation.dependencies.get_enrich_use_case")
    def test_enrich_word_success(self, mock_get_uc, task_word, task_user):
        from apps.words.infrastructure.tasks import enrich_word_task

        mock_uc = MagicMock()
        mock_get_uc.return_value = mock_uc

        enrich_word_task(str(task_word.id), str(task_user.id))
        mock_uc.execute.assert_called_once_with(str(task_word.id), str(task_user.id))

    @patch("apps.words.presentation.dependencies.get_enrich_use_case")
    def test_enrich_word_general_error_marks_failed(self, mock_get_uc, task_word, task_user):
        from apps.words.infrastructure.tasks import enrich_word_task

        mock_uc = MagicMock()
        mock_uc.execute.side_effect = Exception("General error")
        mock_get_uc.return_value = mock_uc

        enrich_word_task(str(task_word.id), str(task_user.id))

        task_word.refresh_from_db()
        assert task_word.enrichment_status == "failed"


# =============================================================================
# BATCH ENRICH TASK
# =============================================================================


@pytest.mark.django_db
class TestBatchEnrichTask:
    @patch("apps.words.presentation.dependencies.get_batch_enrich_use_case")
    def test_batch_enrich(self, mock_get_uc, task_user):
        from apps.words.infrastructure.tasks import batch_enrich_task

        mock_uc = MagicMock()
        mock_uc.execute.return_value = {"enriched": 2, "failed": 0, "errors": []}
        mock_get_uc.return_value = mock_uc

        result = batch_enrich_task(str(task_user.id), [str(uuid4()), str(uuid4())])
        assert result["enriched"] == 2

    @patch("apps.words.presentation.dependencies.get_batch_enrich_use_case")
    def test_batch_enrich_error(self, mock_get_uc, task_user):
        from apps.words.infrastructure.tasks import batch_enrich_task

        mock_uc = MagicMock()
        mock_uc.execute.side_effect = Exception("batch error")
        mock_get_uc.return_value = mock_uc

        result = batch_enrich_task(str(task_user.id), [str(uuid4())])
        assert result["failed"] == 1


# =============================================================================
# UPDATE STREAKS TASK
# =============================================================================


@pytest.mark.django_db
class TestUpdateStreaksTask:
    def test_resets_stale_streaks(self, task_user):
        from apps.words.infrastructure.tasks import update_streaks_task

        # Create a streak that's stale (last activity 3 days ago)
        DailyStreak.objects.create(
            user=task_user,
            current_streak=5,
            longest_streak=5,
            last_activity_date=date.today() - timedelta(days=3),
        )

        update_streaks_task()

        streak = DailyStreak.objects.get(user=task_user)
        assert streak.current_streak == 0

    def test_does_not_reset_active_streaks(self, task_user):
        from apps.words.infrastructure.tasks import update_streaks_task

        DailyStreak.objects.create(
            user=task_user,
            current_streak=5,
            longest_streak=5,
            last_activity_date=date.today(),
        )

        update_streaks_task()

        streak = DailyStreak.objects.get(user=task_user)
        assert streak.current_streak == 5

    def test_does_not_reset_frozen_streaks(self, task_user):
        from apps.words.infrastructure.tasks import update_streaks_task

        DailyStreak.objects.create(
            user=task_user,
            current_streak=5,
            longest_streak=5,
            last_activity_date=date.today() - timedelta(days=3),
            streak_frozen_until=date.today(),
        )

        update_streaks_task()

        streak = DailyStreak.objects.get(user=task_user)
        assert streak.current_streak == 5


# =============================================================================
# CLEANUP SESSIONS TASK
# =============================================================================


@pytest.mark.django_db
class TestCleanupSessionsTask:
    def test_cleans_stale_sessions(self, task_user):
        from apps.words.infrastructure.tasks import cleanup_stale_sessions_task

        # Create old open session
        session = ReviewSession.objects.create(
            user=task_user,
            session_type="review",
            is_completed=False,
        )
        # Use .update() to bypass auto_now_add for started_at
        ReviewSession.objects.filter(pk=session.pk).update(
            started_at=timezone.now() - timedelta(hours=3)
        )

        cleanup_stale_sessions_task()

        session.refresh_from_db()
        assert session.is_completed is True
        assert session.duration_seconds > 0

    def test_does_not_touch_recent_sessions(self, task_user):
        from apps.words.infrastructure.tasks import cleanup_stale_sessions_task

        session = ReviewSession.objects.create(
            user=task_user,
            session_type="review",
            is_completed=False,
        )

        cleanup_stale_sessions_task()

        session.refresh_from_db()
        assert session.is_completed is False
