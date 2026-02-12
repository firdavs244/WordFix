"""
Tests for Google OAuth functionality.
"""

from unittest.mock import patch, MagicMock

import pytest
from rest_framework.test import APIClient

from apps.users.infrastructure.models import CustomUser, UserProgress


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def existing_user(db):
    user = CustomUser.objects.create_user(
        email="google@example.com",
        username="googleuser",
        password="testpass123",
    )
    UserProgress.objects.create(user=user)
    return user


class TestGoogleOAuth:
    """Tests for Google OAuth views."""

    @patch("apps.users.presentation.views.GoogleLoginView._verify_google_token")
    def test_google_login_success(self, mock_verify, api_client, db):
        """Test successful Google login creates user + JWT."""
        mock_verify.return_value = {
            "email": "newgoogle@example.com",
            "name": "Google User",
            "google_id": "12345",
        }

        with patch.dict(
            "django.conf.settings.SOCIALACCOUNT_PROVIDERS",
            {"google": {"APP": {"client_id": "test-client-id", "secret": "test-secret"}}},
        ):
            response = api_client.post(
                "/api/v1/auth/google/",
                {"access_token": "fake-google-token"},
                format="json",
            )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "tokens" in data["data"]
        assert "user" in data["data"]
        assert data["data"]["is_new_user"] is True
        assert data["data"]["user"]["email"] == "newgoogle@example.com"

    @patch("apps.users.presentation.views.GoogleLoginView._verify_google_token")
    def test_google_login_existing_email(self, mock_verify, api_client, existing_user):
        """Test Google login with existing email links account."""
        mock_verify.return_value = {
            "email": "google@example.com",
            "name": "Google User",
            "google_id": "12345",
        }

        with patch.dict(
            "django.conf.settings.SOCIALACCOUNT_PROVIDERS",
            {"google": {"APP": {"client_id": "test-client-id", "secret": "test-secret"}}},
        ):
            response = api_client.post(
                "/api/v1/auth/google/",
                {"access_token": "fake-google-token"},
                format="json",
            )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["is_new_user"] is False
        assert data["data"]["user"]["email"] == "google@example.com"

    @patch("apps.users.presentation.views.GoogleLoginView._verify_google_token")
    def test_google_login_creates_progress(self, mock_verify, api_client, db):
        """Test Google login creates UserProgress for new user."""
        mock_verify.return_value = {
            "email": "progress@example.com",
            "name": "Progress User",
            "google_id": "67890",
        }

        with patch.dict(
            "django.conf.settings.SOCIALACCOUNT_PROVIDERS",
            {"google": {"APP": {"client_id": "test-client-id", "secret": "test-secret"}}},
        ):
            response = api_client.post(
                "/api/v1/auth/google/",
                {"access_token": "fake-google-token"},
                format="json",
            )

        assert response.status_code == 200
        user = CustomUser.objects.get(email="progress@example.com")
        assert UserProgress.objects.filter(user=user).exists()

    def test_google_login_missing_token(self, api_client, db):
        """Test Google login without token returns 400."""
        with patch.dict(
            "django.conf.settings.SOCIALACCOUNT_PROVIDERS",
            {"google": {"APP": {"client_id": "test-client-id", "secret": "test-secret"}}},
        ):
            response = api_client.post(
                "/api/v1/auth/google/",
                {},
                format="json",
            )

        assert response.status_code == 400

    def test_google_auth_status_configured(self, api_client, db):
        """Test auth providers status endpoint."""
        response = api_client.get("/api/v1/auth/providers/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "google_enabled" in data["data"]

    @patch("apps.users.presentation.views.GoogleLoginView._verify_google_token")
    def test_google_login_invalid_token(self, mock_verify, api_client, db):
        """Test Google login with invalid token returns 400."""
        mock_verify.return_value = None

        with patch.dict(
            "django.conf.settings.SOCIALACCOUNT_PROVIDERS",
            {"google": {"APP": {"client_id": "test-client-id", "secret": "test-secret"}}},
        ):
            response = api_client.post(
                "/api/v1/auth/google/",
                {"access_token": "invalid-token"},
                format="json",
            )

        assert response.status_code == 400

    @patch("apps.users.presentation.views.GoogleLoginView._verify_google_token")
    def test_google_login_sets_onboarding_false(self, mock_verify, api_client, db):
        """Test Google login sets has_completed_onboarding = False for new user."""
        mock_verify.return_value = {
            "email": "onboarding@example.com",
            "name": "Onboarding User",
            "google_id": "11111",
        }

        with patch.dict(
            "django.conf.settings.SOCIALACCOUNT_PROVIDERS",
            {"google": {"APP": {"client_id": "test-client-id", "secret": "test-secret"}}},
        ):
            response = api_client.post(
                "/api/v1/auth/google/",
                {"access_token": "fake-google-token"},
                format="json",
            )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["user"]["has_completed_onboarding"] is False
