"""
Tests for Google OAuth view edge cases and additional coverage.
"""

from unittest.mock import patch, MagicMock

import pytest
from rest_framework.test import APIClient

from apps.users.infrastructure.models import CustomUser, UserProgress


@pytest.fixture
def api_client():
    return APIClient()


class TestGoogleLoginViewEdgeCases:
    """Tests for GoogleLoginView edge cases to improve coverage."""

    def test_google_login_not_configured_503(self, api_client, db):
        """Google OAuth returns 503 when not configured (empty client_id)."""
        with patch.dict(
            "django.conf.settings.SOCIALACCOUNT_PROVIDERS",
            {"google": {"APP": {"client_id": "", "secret": ""}}},
        ):
            response = api_client.post(
                "/api/v1/auth/google/",
                {"access_token": "some-token"},
                format="json",
            )
        assert response.status_code == 503
        assert "not configured" in response.json()["message"].lower()

    def test_google_login_no_socialaccount_providers(self, api_client, db):
        """Google OAuth returns 503 when SOCIALACCOUNT_PROVIDERS is missing google."""
        with patch.dict(
            "django.conf.settings.SOCIALACCOUNT_PROVIDERS",
            {},
            clear=True,
        ):
            response = api_client.post(
                "/api/v1/auth/google/",
                {"access_token": "some-token"},
                format="json",
            )
        assert response.status_code == 503

    def test_google_login_id_token_used(self, api_client, db):
        """Google login works with id_token instead of access_token."""
        with patch(
            "apps.users.presentation.views.GoogleLoginView._verify_google_token"
        ) as mock_verify:
            mock_verify.return_value = {
                "email": "idtoken@example.com",
                "name": "ID Token User",
                "google_id": "99999",
            }
            with patch.dict(
                "django.conf.settings.SOCIALACCOUNT_PROVIDERS",
                {"google": {"APP": {"client_id": "test-id", "secret": "test-secret"}}},
            ):
                response = api_client.post(
                    "/api/v1/auth/google/",
                    {"id_token": "fake-id-token"},
                    format="json",
                )
        assert response.status_code == 200
        assert response.json()["data"]["user"]["email"] == "idtoken@example.com"

    @patch("urllib.request.urlopen")
    def test_verify_google_token_userinfo_success(self, mock_urlopen, api_client, db):
        """_verify_google_token returns user info from userinfo endpoint."""
        import json
        from apps.users.presentation.views import GoogleLoginView

        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps({
            "email": "verified@example.com",
            "name": "Verified User",
            "sub": "google-sub-123",
        }).encode()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        result = GoogleLoginView._verify_google_token("valid-access-token", "client-id")

        assert result is not None
        assert result["email"] == "verified@example.com"
        assert result["google_id"] == "google-sub-123"

    @patch("urllib.request.urlopen")
    def test_verify_google_token_tokeninfo_fallback(self, mock_urlopen, api_client, db):
        """_verify_google_token falls back to tokeninfo endpoint."""
        import json
        from apps.users.presentation.views import GoogleLoginView

        # First call (userinfo) raises error
        # Second call (tokeninfo) succeeds
        mock_resp_fail = MagicMock()
        mock_resp_fail.__enter__ = MagicMock(side_effect=Exception("auth error"))
        mock_resp_fail.__exit__ = MagicMock(return_value=False)

        mock_resp_ok = MagicMock()
        mock_resp_ok.read.return_value = json.dumps({
            "email": "tokeninfo@example.com",
            "name": "TokenInfo User",
            "sub": "google-sub-456",
            "aud": "test-client-id",
        }).encode()
        mock_resp_ok.__enter__ = MagicMock(return_value=mock_resp_ok)
        mock_resp_ok.__exit__ = MagicMock(return_value=False)

        mock_urlopen.side_effect = [Exception("first fail"), mock_resp_ok]

        result = GoogleLoginView._verify_google_token("valid-id-token", "test-client-id")

        assert result is not None
        assert result["email"] == "tokeninfo@example.com"

    @patch("urllib.request.urlopen")
    def test_verify_google_token_both_fail(self, mock_urlopen, api_client, db):
        """_verify_google_token returns None when both endpoints fail."""
        from apps.users.presentation.views import GoogleLoginView

        mock_urlopen.side_effect = Exception("network error")

        result = GoogleLoginView._verify_google_token("bad-token", "client-id")
        assert result is None

    @patch("urllib.request.urlopen")
    def test_verify_google_token_no_email(self, mock_urlopen, api_client, db):
        """_verify_google_token returns None when no email in response."""
        import json
        from apps.users.presentation.views import GoogleLoginView

        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps({
            "name": "No Email User",
            "sub": "123",
        }).encode()
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        # Both calls return data without email
        result = GoogleLoginView._verify_google_token("token", "client-id")
        assert result is None

    @patch("urllib.request.urlopen")
    def test_verify_google_token_wrong_aud(self, mock_urlopen, api_client, db):
        """_verify_google_token returns None when tokeninfo aud doesn't match."""
        import json
        from apps.users.presentation.views import GoogleLoginView

        # userinfo fails
        # tokeninfo returns wrong aud
        mock_resp_ok = MagicMock()
        mock_resp_ok.read.return_value = json.dumps({
            "email": "wrong-aud@example.com",
            "aud": "wrong-client-id",
        }).encode()
        mock_resp_ok.__enter__ = MagicMock(return_value=mock_resp_ok)
        mock_resp_ok.__exit__ = MagicMock(return_value=False)

        mock_urlopen.side_effect = [Exception("first fail"), mock_resp_ok]

        result = GoogleLoginView._verify_google_token("token", "correct-client-id")
        assert result is None
