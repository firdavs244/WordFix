"""
Tests for Test API views.
"""

import uuid

import pytest
from rest_framework import status


@pytest.mark.django_db
class TestTestGenerateView:
    URL = "/api/v1/tests/generate/"

    def test_generate_test_201(self, authenticated_client, sample_words):
        """Generate a test successfully."""
        data = {
            "test_type": "multiple_choice",
            "question_count": 5,
            "difficulty": "adaptive",
        }
        response = authenticated_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED, response.data
        assert response.data["success"] is True
        assert "session" in response.data["data"]
        assert "questions" in response.data["data"]

    def test_generate_unauthenticated(self, api_client):
        """Unauthenticated → 401."""
        data = {"test_type": "multiple_choice"}
        response = api_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_generate_invalid_type(self, authenticated_client, sample_words):
        """Invalid test_type → 400."""
        data = {"test_type": "invalid_type"}
        response = authenticated_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestTestSubmitAnswerView:

    def test_submit_answer(self, authenticated_client, sample_words, user):
        """Submit a test answer."""
        # Generate a test first
        gen_resp = authenticated_client.post(
            "/api/v1/tests/generate/",
            {"test_type": "multiple_choice", "question_count": 5},
            format="json",
        )
        assert gen_resp.status_code == status.HTTP_201_CREATED

        session_id = gen_resp.data["data"]["session"]["id"]
        question = gen_resp.data["data"]["questions"][0]

        url = f"/api/v1/tests/{session_id}/answer/"
        data = {
            "question_id": question["id"],
            "answer": "test-answer",
        }
        response = authenticated_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True

    def test_submit_answer_wrong_session(self, authenticated_client, sample_words):
        """Wrong session_id → 404."""
        fake_id = uuid.uuid4()
        url = f"/api/v1/tests/{fake_id}/answer/"
        data = {"question_id": str(uuid.uuid4()), "answer": "x"}
        response = authenticated_client.post(url, data, format="json")
        assert response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST]


@pytest.mark.django_db
class TestTestCompleteView:

    def test_complete_test(self, authenticated_client, sample_words, user):
        """Complete a test session."""
        gen_resp = authenticated_client.post(
            "/api/v1/tests/generate/",
            {"test_type": "multiple_choice", "question_count": 5},
            format="json",
        )
        session_id = gen_resp.data["data"]["session"]["id"]

        url = f"/api/v1/tests/{session_id}/complete/"
        response = authenticated_client.post(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True


@pytest.mark.django_db
class TestTestHistoryView:
    URL = "/api/v1/tests/history/"

    def test_history_200(self, authenticated_client, user):
        """Empty history → 200 ok."""
        response = authenticated_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True

    def test_history_unauthenticated(self, api_client):
        """Unauthenticated → 401."""
        response = api_client.get(self.URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_history_with_data(self, authenticated_client, sample_words):
        """History returns sessions after generating tests."""
        authenticated_client.post(
            "/api/v1/tests/generate/",
            {"test_type": "multiple_choice", "question_count": 5},
            format="json",
        )
        response = authenticated_client.get(self.URL)
        assert response.data["meta"]["total_count"] >= 1


@pytest.mark.django_db
class TestTestDetailView:

    def test_detail(self, authenticated_client, sample_words):
        """Get test session detail."""
        gen_resp = authenticated_client.post(
            "/api/v1/tests/generate/",
            {"test_type": "multiple_choice", "question_count": 5},
            format="json",
        )
        session_id = gen_resp.data["data"]["session"]["id"]

        url = f"/api/v1/tests/{session_id}/"
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "session" in response.data["data"]
        assert "questions" in response.data["data"]
