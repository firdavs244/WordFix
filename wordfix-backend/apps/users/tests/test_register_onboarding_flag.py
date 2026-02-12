"""
Tests for has_completed_onboarding flag in register/login responses.
"""

import pytest
from rest_framework.test import APIClient

from apps.users.infrastructure.models import CustomUser, UserProgress


@pytest.fixture
def api_client():
    return APIClient()


class TestRegisterOnboardingFlag:
    """Test has_completed_onboarding in register/login responses."""

    def test_register_returns_onboarding_flag(self, api_client, db):
        """Register response includes has_completed_onboarding = False."""
        response = api_client.post(
            "/api/v1/auth/register/",
            {
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "testpass123",
                "password_confirm": "testpass123",
            },
            format="json",
        )
        assert response.status_code == 201
        data = response.json()["data"]
        assert "has_completed_onboarding" in data["user"]
        assert data["user"]["has_completed_onboarding"] is False

    def test_login_returns_onboarding_flag(self, api_client, db):
        """Login response includes has_completed_onboarding."""
        CustomUser.objects.create_user(
            email="loginuser@example.com",
            username="loginuser",
            password="testpass123",
        )
        response = api_client.post(
            "/api/v1/auth/login/",
            {
                "email": "loginuser@example.com",
                "password": "testpass123",
            },
            format="json",
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert "has_completed_onboarding" in data["user"]
