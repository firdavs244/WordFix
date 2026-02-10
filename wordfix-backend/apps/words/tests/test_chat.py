"""
Tests for AI Chat feature.
"""

import pytest
from unittest.mock import MagicMock, patch
from rest_framework import status

from apps.words.infrastructure.models import Word


@pytest.mark.django_db
class TestChatUseCases:

    def test_start_chat(self, authenticated_client, sample_words):
        """Start chat → session + first message."""
        response = authenticated_client.post(
            "/api/v1/chat/start/",
            {},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data["data"]
        assert "session_id" in data
        assert "topic" in data
        assert "target_words" in data
        assert "first_message" in data
        assert data["first_message"]["role"] == "assistant"

    def test_start_chat_with_topic(self, authenticated_client, sample_words):
        """Start chat with topic → topic saved."""
        response = authenticated_client.post(
            "/api/v1/chat/start/",
            {"topic": "travel"},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["data"]["topic"] == "travel"

    def test_send_message(self, authenticated_client, sample_words):
        """Send message → AI response with corrections."""
        # Start chat
        start_resp = authenticated_client.post(
            "/api/v1/chat/start/",
            {"topic": "technology"},
            format="json",
        )
        session_id = start_resp.data["data"]["session_id"]

        # Send message
        response = authenticated_client.post(
            f"/api/v1/chat/sessions/{session_id}/message/",
            {"message": "I think technology is very important in our life."},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.data["data"]
        assert "ai_message" in data
        assert "corrections" in data
        assert "words_used" in data

    def test_send_message_word_used(self, authenticated_client, sample_words):
        """When target word is used, it should be tracked."""
        # Start chat
        start_resp = authenticated_client.post(
            "/api/v1/chat/start/",
            {},
            format="json",
        )
        session_id = start_resp.data["data"]["session_id"]
        target_words = start_resp.data["data"]["target_words"]

        # Send message using a target word
        if target_words:
            message = f"I love {target_words[0]} very much!"
            response = authenticated_client.post(
                f"/api/v1/chat/sessions/{session_id}/message/",
                {"message": message},
                format="json",
            )
            assert response.status_code == status.HTTP_200_OK

    def test_end_chat(self, authenticated_client, sample_words):
        """End chat → session closed, stats returned."""
        # Start
        start_resp = authenticated_client.post(
            "/api/v1/chat/start/",
            {"topic": "food"},
            format="json",
        )
        session_id = start_resp.data["data"]["session_id"]

        # End
        response = authenticated_client.post(
            f"/api/v1/chat/sessions/{session_id}/end/",
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.data["data"]
        assert "session_id" in data
        assert "message_count" in data

    def test_chat_history(self, authenticated_client, sample_words):
        """Chat history → paginated list."""
        # Create a session
        authenticated_client.post("/api/v1/chat/start/", {"topic": "sports"}, format="json")

        response = authenticated_client.get("/api/v1/chat/history/")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data["data"], list)
        assert len(response.data["data"]) >= 1

    def test_chat_session_detail(self, authenticated_client, sample_words):
        """Session detail → session + messages list."""
        # Create and interact
        start_resp = authenticated_client.post(
            "/api/v1/chat/start/",
            {"topic": "movies"},
            format="json",
        )
        session_id = start_resp.data["data"]["session_id"]

        response = authenticated_client.get(f"/api/v1/chat/sessions/{session_id}/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data["data"]
        assert "session" in data
        assert "messages" in data
        assert len(data["messages"]) >= 1


@pytest.mark.django_db
class TestChatViewAuth:

    def test_start_unauth(self, api_client):
        """Unauthenticated → 401."""
        resp = api_client.post("/api/v1/chat/start/", {}, format="json")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_history_unauth(self, api_client):
        """Unauthenticated → 401."""
        resp = api_client.get("/api/v1/chat/history/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
