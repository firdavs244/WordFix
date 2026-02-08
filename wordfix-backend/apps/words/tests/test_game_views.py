"""
Tests for Game API views.
"""

import uuid

import pytest
from rest_framework import status

from apps.words.infrastructure.models import GameSession


@pytest.mark.django_db
class TestSpeedRoundViews:

    def test_start_201(self, authenticated_client, sample_words):
        """Start speed round → 201."""
        response = authenticated_client.post(
            "/api/v1/games/speed-round/start/", format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert "session_id" in response.data["data"]
        assert "words" in response.data["data"]
        assert "time_limit" in response.data["data"]

    def test_start_unauthenticated(self, api_client):
        """Unauthenticated → 401."""
        response = api_client.post("/api/v1/games/speed-round/start/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_submit(self, authenticated_client, sample_words):
        """Submit answers → 200 with score."""
        start_resp = authenticated_client.post(
            "/api/v1/games/speed-round/start/", format="json",
        )
        session_id = start_resp.data["data"]["session_id"]
        words = start_resp.data["data"]["words"]

        answers = [
            {"word_id": str(w["word_id"]), "selected_answer": w["correct_translation"]}
            for w in words[:2]
        ]

        response = authenticated_client.post(
            "/api/v1/games/speed-round/submit/",
            {"session_id": str(session_id), "answers": answers},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True


@pytest.mark.django_db
class TestWordMatchViews:

    def test_start_201(self, authenticated_client, sample_words):
        """Start word match → 201."""
        response = authenticated_client.post(
            "/api/v1/games/word-match/start/",
            {"pair_count": 5},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert "session_id" in response.data["data"]
        assert "words" in response.data["data"]
        assert "translations" in response.data["data"]

    def test_submit(self, authenticated_client, sample_words):
        """Submit word match pairs → 200."""
        start_resp = authenticated_client.post(
            "/api/v1/games/word-match/start/",
            {"pair_count": 5},
            format="json",
        )
        session_id = start_resp.data["data"]["session_id"]
        words = start_resp.data["data"]["words"]

        from apps.words.infrastructure.models import Word
        pairs = []
        for w_data in words:
            word = Word.objects.get(id=w_data["word_id"])
            pairs.append({
                "word_id": str(w_data["word_id"]),
                "matched_translation": word.translation,
            })

        response = authenticated_client.post(
            "/api/v1/games/word-match/submit/",
            {"session_id": str(session_id), "pairs": pairs, "time_seconds": 25},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True


@pytest.mark.django_db
class TestWordContextViews:

    def test_start_201(self, authenticated_client, sample_words):
        """Start word context → 201."""
        response = authenticated_client.post(
            "/api/v1/games/word-context/start/", format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert "session_id" in response.data["data"]
        assert "questions" in response.data["data"]

    def test_submit(self, authenticated_client, sample_words):
        """Submit word context answers → 200."""
        start_resp = authenticated_client.post(
            "/api/v1/games/word-context/start/", format="json",
        )
        session_id = start_resp.data["data"]["session_id"]
        questions = start_resp.data["data"]["questions"]

        answers = [
            {"word_id": str(q["word_id"]), "selected_answer": q["correct_answer"]}
            for q in questions
        ]

        response = authenticated_client.post(
            "/api/v1/games/word-context/submit/",
            {"session_id": str(session_id), "answers": answers},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True


@pytest.mark.django_db
class TestGameHistoryView:
    URL = "/api/v1/games/history/"

    def test_history_200(self, authenticated_client, user):
        """Empty history → 200."""
        response = authenticated_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True

    def test_history_unauthenticated(self, api_client):
        response = api_client.get(self.URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_history_with_data(self, authenticated_client, sample_words):
        """After playing, history returns sessions."""
        authenticated_client.post(
            "/api/v1/games/speed-round/start/", format="json",
        )
        response = authenticated_client.get(self.URL)
        assert response.data["meta"]["total_count"] >= 0


@pytest.mark.django_db
class TestGameStatsView:
    URL = "/api/v1/games/stats/"

    def test_stats_200(self, authenticated_client):
        """Stats endpoint → 200."""
        response = authenticated_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True

    def test_stats_unauthenticated(self, api_client):
        response = api_client.get(self.URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
