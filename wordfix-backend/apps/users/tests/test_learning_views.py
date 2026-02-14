"""
Tests for learning views (API endpoints).
"""

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.infrastructure.models import CustomUser, LearningProfile, WordRecommendation


@pytest.fixture
def learning_user(db):
    return CustomUser.objects.create_user(
        email="learn@example.com",
        username="learnuser",
        password="testpass123",
    )


@pytest.fixture
def learning_client(learning_user):
    client = APIClient()
    refresh = RefreshToken.for_user(learning_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return client


@pytest.mark.django_db
class TestLearningViews:

    def test_get_profile_200(self, learning_client):
        response = learning_client.get("/api/v1/learning-profile/")
        assert response.status_code == 200
        assert response.data["success"] is True
        assert "preferred_style" in response.data["data"]

    def test_analyze_profile_200(self, learning_client):
        response = learning_client.post("/api/v1/learning-profile/analyze/")
        assert response.status_code == 200
        assert response.data["success"] is True
        assert "learning_style" in response.data["data"]

    def test_get_patterns_200(self, learning_client):
        response = learning_client.get("/api/v1/learning-profile/mistake-patterns/")
        assert response.status_code == 200
        assert response.data["success"] is True
        assert isinstance(response.data["data"], list)

    def test_get_recommendations_200(self, learning_client):
        response = learning_client.get("/api/v1/learning-profile/recommendations/")
        assert response.status_code == 200
        assert response.data["success"] is True
        assert isinstance(response.data["data"], list)

    def test_accept_recommendation_200(self, learning_client, learning_user):
        rec = WordRecommendation.objects.create(
            user=learning_user,
            recommended_word="test",
            translation="sinov",
            reason="test",
            reason_type="high_frequency",
            priority_score=0.5,
        )
        response = learning_client.post(
            "/api/v1/learning-profile/recommendations/",
            {"recommendation_id": str(rec.id)},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["success"] is True

    def test_get_coverage_200(self, learning_client):
        response = learning_client.get("/api/v1/learning-profile/domain-coverage/")
        assert response.status_code == 200
        assert response.data["success"] is True

    def test_get_difficulty_200(self, learning_client):
        response = learning_client.get("/api/v1/learning-profile/difficulty/")
        assert response.status_code == 200
        assert response.data["success"] is True
        assert "difficulty_level" in response.data["data"]

    def test_all_endpoints_require_auth(self, api_client):
        endpoints = [
            ("GET", "/api/v1/learning-profile/"),
            ("POST", "/api/v1/learning-profile/analyze/"),
            ("GET", "/api/v1/learning-profile/mistake-patterns/"),
            ("GET", "/api/v1/learning-profile/recommendations/"),
            ("GET", "/api/v1/learning-profile/domain-coverage/"),
            ("GET", "/api/v1/learning-profile/difficulty/"),
        ]
        unauthenticated = APIClient()
        for method, url in endpoints:
            if method == "GET":
                response = unauthenticated.get(url)
            else:
                response = unauthenticated.post(url)
            assert response.status_code == 401, f"{method} {url} should require auth"
