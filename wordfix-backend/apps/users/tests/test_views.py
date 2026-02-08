"""
Tests for User API views (auth endpoints).
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.infrastructure.models import CustomUser


# =============================================================================
# REGISTER VIEW TESTS
# =============================================================================


@pytest.mark.django_db
class TestRegisterView:
    URL = "/api/v1/auth/register/"

    def test_register_success(self, api_client):
        data = {
            "email": "new@example.com",
            "username": "newuser",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }
        response = api_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True
        assert "tokens" in response.data["data"]
        assert "user" in response.data["data"]

    def test_register_returns_user_data(self, api_client):
        data = {
            "email": "new@example.com",
            "username": "newuser",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }
        response = api_client.post(self.URL, data, format="json")
        user_data = response.data["data"]["user"]
        assert user_data["email"] == "new@example.com"
        assert user_data["username"] == "newuser"

    def test_register_duplicate_email(self, api_client, user):
        data = {
            "email": user.email,
            "username": "other",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }
        response = api_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_register_invalid_data(self, api_client):
        data = {"email": "bad"}
        response = api_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_password_mismatch(self, api_client):
        data = {
            "email": "t@t.com",
            "username": "test",
            "password": "testpass123",
            "password_confirm": "different1",
        }
        response = api_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_no_auth_required(self, api_client):
        data = {
            "email": "anon@test.com",
            "username": "anonuser",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }
        response = api_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED


# =============================================================================
# LOGIN VIEW TESTS
# =============================================================================


@pytest.mark.django_db
class TestLoginView:
    URL = "/api/v1/auth/login/"

    def test_login_success(self, api_client, user):
        data = {"email": user.email, "password": "testpass123"}
        response = api_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["tokens"]["access"]

    def test_login_wrong_password(self, api_client, user):
        data = {"email": user.email, "password": "wrongpass"}
        response = api_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, api_client):
        data = {"email": "noone@test.com", "password": "pass123"}
        response = api_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_inactive_user(self, api_client, user):
        user.is_active = False
        user.save()
        data = {"email": user.email, "password": "testpass123"}
        response = api_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_returns_user_data(self, api_client, user):
        data = {"email": user.email, "password": "testpass123"}
        response = api_client.post(self.URL, data, format="json")
        assert response.data["data"]["user"]["email"] == user.email

    def test_login_no_auth_required(self, api_client, user):
        data = {"email": user.email, "password": "testpass123"}
        response = api_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_200_OK


# =============================================================================
# LOGOUT VIEW TESTS
# =============================================================================


@pytest.mark.django_db
class TestLogoutView:
    URL = "/api/v1/auth/logout/"

    def test_logout_success(self, authenticated_client, user):
        refresh = RefreshToken.for_user(user)
        response = authenticated_client.post(
            self.URL, {"refresh": str(refresh)}, format="json"
        )
        assert response.status_code == status.HTTP_200_OK

    def test_logout_without_token(self, authenticated_client):
        response = authenticated_client.post(self.URL, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_logout_invalid_token(self, authenticated_client):
        response = authenticated_client.post(
            self.URL, {"refresh": "invalid-token"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_logout_requires_auth(self, api_client):
        response = api_client.post(self.URL, {}, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# =============================================================================
# TOKEN REFRESH VIEW TESTS
# =============================================================================


@pytest.mark.django_db
class TestTokenRefreshView:
    URL = "/api/v1/auth/token/refresh/"

    def test_refresh_success(self, api_client, user):
        refresh = RefreshToken.for_user(user)
        response = api_client.post(
            self.URL, {"refresh": str(refresh)}, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["access"]

    def test_refresh_invalid_token(self, api_client):
        response = api_client.post(
            self.URL, {"refresh": "bad-token"}, format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_missing_token(self, api_client):
        response = api_client.post(self.URL, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# =============================================================================
# PROFILE VIEW TESTS
# =============================================================================


@pytest.mark.django_db
class TestProfileView:
    URL = "/api/v1/auth/profile/"

    def test_get_profile(self, authenticated_client, user):
        response = authenticated_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["email"] == user.email

    def test_get_profile_unauthenticated(self, api_client):
        response = api_client.get(self.URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_profile(self, authenticated_client):
        response = authenticated_client.patch(
            self.URL, {"full_name": "Updated"}, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["full_name"] == "Updated"

    def test_update_profile_timezone(self, authenticated_client):
        response = authenticated_client.patch(
            self.URL, {"timezone": "US/Eastern"}, format="json"
        )
        assert response.status_code == status.HTTP_200_OK

    def test_update_profile_daily_goal(self, authenticated_client):
        response = authenticated_client.patch(
            self.URL, {"daily_goal": 30}, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["daily_goal"] == 30

    def test_profile_response_format(self, authenticated_client):
        response = authenticated_client.get(self.URL)
        assert "success" in response.data
        assert "data" in response.data
        assert "message" in response.data


# =============================================================================
# CHANGE PASSWORD VIEW TESTS
# =============================================================================


@pytest.mark.django_db
class TestChangePasswordView:
    URL = "/api/v1/auth/change-password/"

    def test_change_password_success(self, authenticated_client):
        data = {
            "old_password": "testpass123",
            "new_password": "newpass456",
            "new_password_confirm": "newpass456",
        }
        response = authenticated_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_change_password_wrong_old(self, authenticated_client):
        data = {
            "old_password": "wrong123",
            "new_password": "newpass456",
            "new_password_confirm": "newpass456",
        }
        response = authenticated_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_password_unauthenticated(self, api_client):
        data = {
            "old_password": "old123456",
            "new_password": "new123456",
            "new_password_confirm": "new123456",
        }
        response = api_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_change_password_mismatch(self, authenticated_client):
        data = {
            "old_password": "testpass123",
            "new_password": "newpass456",
            "new_password_confirm": "different1",
        }
        response = authenticated_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
