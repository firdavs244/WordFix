"""
Tests for Story Builder API views.
"""

import pytest
from rest_framework import status


@pytest.mark.django_db
class TestStoryBuilderViews:

    def test_start_201(self, authenticated_client, sample_words):
        """Start story builder → 201."""
        response = authenticated_client.post(
            "/api/v1/games/story-builder/start/", format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data["data"]
        assert "session_id" in data
        assert "ai_text" in data
        assert "genre" in data

    def test_start_unauthenticated(self, api_client):
        """Unauthenticated → 401."""
        response = api_client.post("/api/v1/games/story-builder/start/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_submit_round(self, authenticated_client, sample_words):
        """Submit a story round → 200."""
        start_resp = authenticated_client.post(
            "/api/v1/games/story-builder/start/", format="json",
        )
        assert start_resp.status_code == status.HTTP_201_CREATED
        data = start_resp.data["data"]

        response = authenticated_client.post(
            "/api/v1/games/story-builder/submit/",
            {
                "session_id": str(data["session_id"]),
                "user_text": "The apple fell from the tree while I had to run quickly.",
            },
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True

    def test_complete(self, authenticated_client, sample_words):
        """Complete story builder → 200 with full story."""
        start_resp = authenticated_client.post(
            "/api/v1/games/story-builder/start/", format="json",
        )
        data = start_resp.data["data"]
        session_id = str(data["session_id"])

        # Submit round
        authenticated_client.post(
            "/api/v1/games/story-builder/submit/",
            {
                "session_id": session_id,
                "user_text": "I found a beautiful apple and started to run quickly.",
            },
            format="json",
        )

        # Complete
        response = authenticated_client.post(
            "/api/v1/games/story-builder/complete/",
            {"session_id": session_id},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert "total_score" in response.data["data"]

    def test_start_not_enough_words(self, authenticated_client, user):
        """Start with < 5 words → 400."""
        from apps.words.infrastructure.models import Word
        # Create only 2 words
        for i in range(2):
            Word.objects.create(
                user=user, original_word=f"word{i}",
                translation=f"trans{i}",
            )
        response = authenticated_client.post(
            "/api/v1/games/story-builder/start/", format="json",
        )
        assert response.status_code in (
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
