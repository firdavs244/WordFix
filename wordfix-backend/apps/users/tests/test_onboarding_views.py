"""
Integration tests for onboarding views.
"""

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.infrastructure.models import (
    CustomUser,
    OnboardingQuestion,
    UserProgress,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    u = CustomUser.objects.create_user(
        email="viewtest@example.com",
        username="viewtestuser",
        password="testpass123",
    )
    UserProgress.objects.create(user=u)
    return u


@pytest.fixture
def auth_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return api_client


@pytest.fixture
def seed_questions(db):
    from apps.users.management.commands.seed_onboarding_questions import QUESTIONS

    for q in QUESTIONS:
        OnboardingQuestion.objects.create(**q)


class TestOnboardingViews:
    """Integration tests for onboarding API endpoints."""

    def test_get_questions_200(self, api_client, seed_questions):
        """GET questions returns 200."""
        response = api_client.get("/api/v1/auth/onboarding/questions/")
        assert response.status_code == 200
        assert response.json()["success"] is True

    def test_submit_200_with_level(self, auth_client, user, seed_questions):
        """POST submit returns 200 with level."""
        questions = OnboardingQuestion.objects.all()
        answers = [
            {"question_id": str(q.id), "answer": q.correct_answer}
            for q in questions
            if q.level in ("A1", "A2")
        ] + [
            {"question_id": str(q.id), "answer": "wrong"}
            for q in questions
            if q.level not in ("A1", "A2")
        ]
        response = auth_client.post(
            "/api/v1/auth/onboarding/submit/",
            {"answers": answers},
            format="json",
        )
        assert response.status_code == 200
        assert "determined_level" in response.json()["data"]

    def test_submit_unauth_401(self, api_client, seed_questions):
        """POST submit without auth returns 401."""
        response = api_client.post(
            "/api/v1/auth/onboarding/submit/",
            {"answers": []},
            format="json",
        )
        assert response.status_code == 401

    def test_skip_200(self, auth_client, user):
        """POST skip returns 200."""
        response = auth_client.post("/api/v1/auth/onboarding/skip/")
        assert response.status_code == 200

    def test_status_200(self, auth_client, user):
        """GET status returns 200."""
        response = auth_client.get("/api/v1/auth/onboarding/status/")
        assert response.status_code == 200
        assert "completed" in response.json()["data"]
