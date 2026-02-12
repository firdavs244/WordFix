"""
Tests for review and enrichment API views.
"""

from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.infrastructure.models import CustomUser
from apps.words.infrastructure.models import (
    DailyActivity,
    DailyStreak,
    ReviewLog,
    ReviewSession,
    Word,
    WordCategory,
)


@pytest.fixture
def review_user(db):
    return CustomUser.objects.create_user(
        email="reviewer@test.com",
        username="reviewer",
        password="testpass123",
        full_name="Review User",
        daily_goal=10,
    )


@pytest.fixture
def review_client(review_user):
    client = APIClient()
    refresh = RefreshToken.for_user(review_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return client


@pytest.fixture
def review_word(review_user):
    return Word.objects.create(
        user=review_user,
        original_word="apple",
        translation="olma",
        difficulty_level="easy",
        confidence_score=50.0,
        next_review_at=timezone.now(),
    )


@pytest.fixture
def review_words(review_user):
    words = []
    for i, name in enumerate(["hello", "world", "test", "code", "python"]):
        w = Word.objects.create(
            user=review_user,
            original_word=name,
            translation=f"translation_{name}",
            difficulty_level="medium",
            next_review_at=timezone.now(),
        )
        words.append(w)
    return words


@pytest.fixture
def review_session(review_user):
    return ReviewSession.objects.create(
        user=review_user,
        session_type="review",
        total_words=0,
    )


# =============================================================================
# REVIEW WORDS
# =============================================================================


@pytest.mark.django_db
class TestReviewWordsView:
    def test_get_review_words(self, review_client, review_words):
        response = review_client.get("/api/v1/review/words/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["success"] is True
        assert len(response.json()["data"]) > 0

    def test_get_review_words_with_type(self, review_client, review_words):
        response = review_client.get("/api/v1/review/words/?type=quick")
        assert response.status_code == status.HTTP_200_OK

    def test_get_review_words_with_limit(self, review_client, review_words):
        response = review_client.get("/api/v1/review/words/?limit=2")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["data"]) <= 2

    def test_unauthenticated_rejected(self):
        client = APIClient()
        response = client.get("/api/v1/review/words/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# =============================================================================
# SESSION CRUD
# =============================================================================


@pytest.mark.django_db
class TestReviewSessionViews:
    def test_create_session(self, review_client, review_words):
        response = review_client.post(
            "/api/v1/review/sessions/",
            {"session_type": "review"},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()["data"]
        assert data["session_type"] == "review"
        assert data["is_completed"] is False

    def test_create_quick_session(self, review_client, review_words):
        response = review_client.post(
            "/api/v1/review/sessions/",
            {"session_type": "quick"},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_session_default_type(self, review_client, review_words):
        response = review_client.post(
            "/api/v1/review/sessions/", {}, format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["data"]["session_type"] == "review"

    def test_get_session_detail(self, review_client, review_session):
        url = f"/api/v1/review/sessions/{review_session.id}/"
        response = review_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_complete_session(self, review_client, review_session):
        url = f"/api/v1/review/sessions/{review_session.id}/complete/"
        response = review_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["is_completed"] is True


# =============================================================================
# SUBMIT ANSWER
# =============================================================================


@pytest.mark.django_db
class TestSubmitAnswerView:
    def test_submit_correct_answer(self, review_client, review_session, review_word):
        url = f"/api/v1/review/sessions/{review_session.id}/answer/"
        response = review_client.post(url, {
            "word_id": str(review_word.id),
            "quality": 4,
            "response_time_ms": 2000,
        }, format="json")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["is_correct"] is True

    def test_submit_incorrect_answer(self, review_client, review_session, review_word):
        url = f"/api/v1/review/sessions/{review_session.id}/answer/"
        response = review_client.post(url, {
            "word_id": str(review_word.id),
            "quality": 1,
        }, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["is_correct"] is False

    def test_submit_invalid_quality(self, review_client, review_session, review_word):
        url = f"/api/v1/review/sessions/{review_session.id}/answer/"
        response = review_client.post(url, {
            "word_id": str(review_word.id),
            "quality": 10,
        }, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_submit_missing_word_id(self, review_client, review_session):
        url = f"/api/v1/review/sessions/{review_session.id}/answer/"
        response = review_client.post(url, {
            "quality": 4,
        }, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_submit_answer_updates_word(self, review_client, review_session, review_word):
        url = f"/api/v1/review/sessions/{review_session.id}/answer/"
        review_client.post(url, {
            "word_id": str(review_word.id),
            "quality": 5,
        }, format="json")

        review_word.refresh_from_db()
        assert review_word.review_count == 1
        assert review_word.correct_count == 1
        assert review_word.next_review_at is not None


# =============================================================================
# REVIEW SUMMARY
# =============================================================================


@pytest.mark.django_db
class TestReviewSummaryView:
    def test_get_summary(self, review_client, review_words):
        response = review_client.get("/api/v1/review/summary/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "total_words" in data
        assert "due_today" in data
        assert "streak" in data
        assert "daily_goal" in data
        assert "daily_progress_pct" in data


# =============================================================================
# REVIEW HISTORY
# =============================================================================


@pytest.mark.django_db
class TestReviewHistoryView:
    def test_get_empty_history(self, review_client):
        response = review_client.get("/api/v1/review/history/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"] == []

    def test_get_history_with_sessions(self, review_client, review_user):
        for i in range(3):
            ReviewSession.objects.create(
                user=review_user,
                session_type="review",
                total_words=i + 1,
                is_completed=True,
            )

        response = review_client.get("/api/v1/review/history/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["data"]) == 3


# =============================================================================
# STREAK
# =============================================================================


@pytest.mark.django_db
class TestStreakView:
    def test_get_streak_creates_if_not_exists(self, review_client):
        response = review_client.get("/api/v1/review/streak/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["current_streak"] == 0

    def test_get_streak_existing(self, review_client, review_user):
        DailyStreak.objects.create(
            user=review_user, current_streak=5, longest_streak=10,
        )
        response = review_client.get("/api/v1/review/streak/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["current_streak"] == 5
        assert data["longest_streak"] == 10


# =============================================================================
# DAILY PROGRESS
# =============================================================================


@pytest.mark.django_db
class TestDailyProgressView:
    def test_get_daily_progress(self, review_client):
        response = review_client.get("/api/v1/review/daily-progress/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["words_reviewed"] == 0
        assert data["xp_earned"] == 0


# =============================================================================
# ENRICHMENT VIEWS
# =============================================================================


@pytest.mark.django_db
class TestEnrichmentViews:
    def test_enrichment_status(self, review_client, review_word):
        url = f"/api/v1/words/{review_word.id}/enrichment-status/"
        response = review_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["enrichment_status"] == "pending"
        assert data["is_enriched"] is False

    @patch("apps.words.infrastructure.tasks.enrich_word_task")
    def test_enrich_word(self, mock_task, review_client, review_word):
        url = f"/api/v1/words/{review_word.id}/enrich/"
        response = review_client.post(url)
        assert response.status_code == status.HTTP_202_ACCEPTED
        mock_task.delay.assert_called_once()

    def test_enrich_all_no_pending(self, review_client, review_user):
        # Create a word that's already enriched
        Word.objects.create(
            user=review_user,
            original_word="enriched_word",
            enrichment_status="enriched",
            is_enriched=True,
        )
        response = review_client.post("/api/v1/words/enrich-all/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["count"] == 0

    @patch("apps.words.infrastructure.tasks.batch_enrich_task")
    def test_enrich_all_with_pending(self, mock_task, review_client, review_user):
        Word.objects.create(
            user=review_user,
            original_word="pending_word",
            enrichment_status="pending",
        )
        response = review_client.post("/api/v1/words/enrich-all/")
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json()["data"]["count"] >= 1


# =============================================================================
# PREDICTED INTERVALS
# =============================================================================


@pytest.mark.django_db
class TestPredictedIntervalsView:
    def test_predict_intervals(self, review_client, review_word):
        url = f"/api/v1/review/words/{review_word.id}/predict/"
        response = review_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert len(data) == 6  # Predictions for quality 0-5
