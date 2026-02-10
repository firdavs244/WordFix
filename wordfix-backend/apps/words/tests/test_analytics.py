"""
Tests for Analytics feature.
"""

from datetime import date, timedelta

import pytest
from rest_framework import status

from apps.words.infrastructure.models import DailyActivity, Word


@pytest.mark.django_db
class TestAnalyticsOverview:

    def test_overview(self, authenticated_client, sample_words):
        """Overview → all fields present."""
        response = authenticated_client.get("/api/v1/analytics/overview/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data["data"]
        assert "total_words" in data
        assert "mastered_words" in data
        assert "mastered_percentage" in data
        assert "total_reviews" in data
        assert "total_correct" in data
        assert "overall_accuracy" in data
        assert "total_study_time_formatted" in data
        assert "total_xp" in data
        assert "current_level" in data
        assert "current_streak" in data
        assert "longest_streak" in data
        assert "tests_completed" in data
        assert "games_played" in data
        assert "avg_daily_words" in data
        assert "avg_daily_time" in data
        assert "member_since_days" in data

    def test_overview_correct_word_count(self, authenticated_client, sample_words):
        """Overview → correct word count."""
        response = authenticated_client.get("/api/v1/analytics/overview/")
        data = response.data["data"]
        assert data["total_words"] == 5  # from sample_words fixture


@pytest.mark.django_db
class TestWeeklyStats:

    def test_weekly_stats(self, authenticated_client, user):
        """Weekly stats → 7 days of data."""
        # Create some activity
        today = date.today()
        DailyActivity.objects.create(
            user=user, date=today,
            words_reviewed=10, words_added=3,
            correct_answers=8, incorrect_answers=2,
            xp_earned=50, total_time_seconds=600,
        )

        response = authenticated_client.get("/api/v1/analytics/weekly/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data["data"]
        assert len(data) == 7

        # Check today's data is present
        today_str = today.isoformat()
        today_data = next((d for d in data if d["date"] == today_str), None)
        assert today_data is not None
        assert today_data["words_reviewed"] == 10


@pytest.mark.django_db
class TestMonthlyStats:

    def test_monthly_stats(self, authenticated_client, user):
        """Monthly stats → 30 days."""
        response = authenticated_client.get("/api/v1/analytics/monthly/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data["data"]
        assert len(data) == 30


@pytest.mark.django_db
class TestDifficultWords:

    def test_difficult_words(self, authenticated_client, user, word_category):
        """Difficult words → sorted by accuracy."""
        # Create words with different accuracy
        Word.objects.create(
            user=user, original_word="hard1", translation="qiyin1",
            category=word_category, review_count=10,
            correct_count=3, incorrect_count=7,
        )
        Word.objects.create(
            user=user, original_word="hard2", translation="qiyin2",
            category=word_category, review_count=10,
            correct_count=5, incorrect_count=5,
        )

        response = authenticated_client.get("/api/v1/analytics/difficult-words/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data["data"]
        assert len(data) >= 2
        # Should be sorted by accuracy ascending
        if len(data) >= 2:
            assert data[0]["accuracy_rate"] <= data[1]["accuracy_rate"]


@pytest.mark.django_db
class TestWordProgress:

    def test_word_progress(self, authenticated_client, sample_words):
        """Word progress → distribution data."""
        response = authenticated_client.get("/api/v1/analytics/word-progress/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data["data"]
        assert "by_confidence" in data
        assert "by_difficulty" in data
        assert "by_category" in data
        assert "recently_mastered" in data
        assert "needs_attention" in data

    def test_word_progress_confidence_distribution(self, authenticated_client, sample_words):
        """Confidence distribution adds up to total words."""
        response = authenticated_client.get("/api/v1/analytics/word-progress/")
        data = response.data["data"]
        total_from_dist = sum(data["by_confidence"].values())
        assert total_from_dist == 5  # from sample_words


@pytest.mark.django_db
class TestStudyCalendar:

    def test_calendar(self, authenticated_client, user):
        """Calendar → heatmap data for current month."""
        today = date.today()
        response = authenticated_client.get(
            f"/api/v1/analytics/calendar/?year={today.year}&month={today.month}"
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.data["data"]
        assert len(data) > 0
        # Check that each day has required fields
        for day in data:
            assert "date" in day
            assert "active" in day
            assert "words_reviewed" in day
            assert "goal_completed" in day


@pytest.mark.django_db
class TestEmptyUser:

    def test_empty_user(self, authenticated_client):
        """New user → zeros everywhere."""
        response = authenticated_client.get("/api/v1/analytics/overview/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data["data"]
        assert data["total_words"] == 0
        assert data["mastered_words"] == 0
        assert data["total_reviews"] == 0


@pytest.mark.django_db
class TestAnalyticsAuth:

    def test_overview_unauth(self, api_client):
        resp = api_client.get("/api/v1/analytics/overview/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_weekly_unauth(self, api_client):
        resp = api_client.get("/api/v1/analytics/weekly/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_calendar_unauth(self, api_client):
        resp = api_client.get("/api/v1/analytics/calendar/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_progress_unauth(self, api_client):
        resp = api_client.get("/api/v1/analytics/word-progress/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_difficult_unauth(self, api_client):
        resp = api_client.get("/api/v1/analytics/difficult-words/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
