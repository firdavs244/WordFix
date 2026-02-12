"""
Tests for edge cases and error handling.
"""

import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest
from django.core.cache import cache
from rest_framework import status


@pytest.mark.django_db
class TestReviewSessionEdgeCases:

    def test_start_review_not_enough_words(self, authenticated_client, user):
        """Start review with < 5 words → validation error."""
        from apps.words.infrastructure.models import Word

        # Create only 3 words (need at least 5)
        for i in range(3):
            Word.objects.create(
                user=user, original_word=f"edge{i}",
                translation=f"trans{i}",
            )

        response = authenticated_client.post(
            "/api/v1/review/sessions/",
            {"session_type": "review"},
            format="json",
        )
        # Should return error about not enough words
        assert response.status_code in (
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    def test_start_review_with_enough_words(self, authenticated_client, sample_words):
        """Start review with >= 5 words → success."""
        response = authenticated_client.post(
            "/api/v1/review/sessions/",
            {"session_type": "review"},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestEnrichmentRetry:

    def test_retry_failed_enrichment(self, authenticated_client, user):
        """Retry enrichment on failed word → 202."""
        from apps.words.infrastructure.models import Word

        word = Word.objects.create(
            user=user, original_word="failedword",
            translation="test", enrichment_status="failed",
            enrichment_error="AI provider unavailable",
        )

        response = authenticated_client.post(
            f"/api/v1/words/{word.id}/enrichment-retry/",
            format="json",
        )
        assert response.status_code == status.HTTP_202_ACCEPTED

        word.refresh_from_db()
        assert word.enrichment_status == "pending"
        assert word.enrichment_error == ""

    def test_retry_non_failed_enrichment(self, authenticated_client, sample_word):
        """Retry on non-failed word → 400."""
        response = authenticated_client.post(
            f"/api/v1/words/{sample_word.id}/enrichment-retry/",
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestStaleSessionCleanup:

    def test_stale_review_sessions_cleaned(self, user):
        """Review sessions > 2h old are auto-completed."""
        from apps.words.infrastructure.models import ReviewSession
        from apps.words.infrastructure.tasks import cleanup_stale_sessions_task

        # Create a stale session (3 hours old)
        session = ReviewSession.objects.create(
            user=user, session_type="review", total_words=5,
        )
        ReviewSession.objects.filter(id=session.id).update(
            started_at=datetime.now(timezone.utc) - timedelta(hours=3),
        )

        cleanup_stale_sessions_task()

        session.refresh_from_db()
        assert session.is_completed is True

    def test_stale_game_sessions_cleaned(self, user):
        """Game sessions > 1h old are auto-completed with score 0."""
        from apps.words.infrastructure.models import GameSession
        from apps.words.infrastructure.tasks import cleanup_stale_sessions_task

        session = GameSession.objects.create(
            user=user, game_type="story_builder", max_score=100,
        )
        GameSession.objects.filter(id=session.id).update(
            started_at=datetime.now(timezone.utc) - timedelta(hours=2),
        )

        cleanup_stale_sessions_task()

        session.refresh_from_db()
        assert session.is_completed is True
        assert session.score == 0

    def test_fresh_sessions_not_cleaned(self, user):
        """Recent sessions are not touched."""
        from apps.words.infrastructure.models import GameSession
        from apps.words.infrastructure.tasks import cleanup_stale_sessions_task

        session = GameSession.objects.create(
            user=user, game_type="speed_round", max_score=10,
        )
        # Session is fresh (just created)
        cleanup_stale_sessions_task()

        session.refresh_from_db()
        assert session.is_completed is False


class TestDailyChallengeTypes:

    def test_easy_pool_includes_story_and_listening(self):
        """Easy challenge pool includes write_story and listening."""
        from apps.words.domain.services import DailyChallengeService

        types = {c["type"] for c in DailyChallengeService.CHALLENGE_TYPES_EASY}
        assert "write_story" in types
        assert "listening" in types

    def test_medium_pool_includes_story_and_listening(self):
        """Medium challenge pool includes write_story and listening."""
        from apps.words.domain.services import DailyChallengeService

        types = {c["type"] for c in DailyChallengeService.CHALLENGE_TYPES_MEDIUM}
        assert "write_story" in types
        assert "listening" in types

    def test_hard_pool_includes_story_and_listening(self):
        """Hard challenge pool includes write_story and listening."""
        from apps.words.domain.services import DailyChallengeService

        types = {c["type"] for c in DailyChallengeService.CHALLENGE_TYPES_HARD}
        assert "write_story" in types
        assert "listening" in types
