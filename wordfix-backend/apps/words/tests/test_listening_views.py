"""
Tests for Listening Challenge API views.
"""

import pytest
from rest_framework import status


@pytest.mark.django_db
class TestListeningChallengeViews:

    def test_start_201(self, authenticated_client, sample_words):
        """Start listening challenge → 201."""
        response = authenticated_client.post(
            "/api/v1/games/listening/start/", format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data["data"]
        assert "session_id" in data
        assert "first_word" in data
        assert "total_rounds" in data

    def test_start_unauthenticated(self, api_client):
        """Unauthenticated → 401."""
        response = api_client.post("/api/v1/games/listening/start/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_submit_answer(self, authenticated_client, sample_words):
        """Submit listening answer → 200."""
        start_resp = authenticated_client.post(
            "/api/v1/games/listening/start/", format="json",
        )
        assert start_resp.status_code == status.HTTP_201_CREATED
        data = start_resp.data["data"]
        session_id = str(data["session_id"])

        # Try submitting answer for round 1
        response = authenticated_client.post(
            "/api/v1/games/listening/answer/",
            {
                "session_id": session_id,
                "round_number": 1,
                "answer": "test",
            },
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True

    def test_complete(self, authenticated_client, sample_words):
        """Complete listening challenge → 200."""
        start_resp = authenticated_client.post(
            "/api/v1/games/listening/start/", format="json",
        )
        data = start_resp.data["data"]
        session_id = str(data["session_id"])

        response = authenticated_client.post(
            "/api/v1/games/listening/complete/",
            {"session_id": session_id},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert "total_score" in response.data["data"]

    def test_start_not_enough_words(self, authenticated_client, user):
        """Start with < 5 words → 400."""
        from apps.words.infrastructure.models import Word
        for i in range(2):
            Word.objects.create(
                user=user, original_word=f"listen{i}",
                translation=f"trans{i}",
            )
        response = authenticated_client.post(
            "/api/v1/games/listening/start/", format="json",
        )
        assert response.status_code in (
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
