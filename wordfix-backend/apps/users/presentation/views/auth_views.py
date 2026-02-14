"""
Authentication views — register, login, logout, token refresh, Google OAuth.
"""

import logging

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.utils.helpers import build_success_response, build_error_response
from ..dependencies import (
    get_register_use_case,
    get_login_use_case,
    get_google_login_use_case,
)
from ..serializers import (
    RegisterSerializer,
    LoginSerializer,
    GoogleLoginSerializer,
)
from .helpers import _user_entity_to_dict

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    """POST /api/v1/auth/register/ — Register a new user."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_register_use_case()
        user_entity, tokens = use_case.execute(serializer.validated_data)

        return Response(
            build_success_response(
                data={
                    "user": _user_entity_to_dict(user_entity),
                    "tokens": tokens,
                },
                message="Registration successful.",
            ),
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """POST /api/v1/auth/login/ — Login with email and password."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_login_use_case()
        user_entity, tokens = use_case.execute(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        return Response(
            build_success_response(
                data={
                    "user": _user_entity_to_dict(user_entity),
                    "tokens": tokens,
                },
                message="Login successful.",
            ),
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """POST /api/v1/auth/logout/ — Blacklist refresh token."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                build_error_response(message="Refresh token is required."),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                build_error_response(message="Invalid or expired token."),
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            build_success_response(message="Logout successful."),
            status=status.HTTP_200_OK,
        )


class TokenRefreshView(APIView):
    """POST /api/v1/auth/token/refresh/ — Refresh access token."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request) -> Response:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                build_error_response(message="Refresh token is required."),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            new_access = str(token.access_token)
        except TokenError:
            return Response(
                build_error_response(message="Invalid or expired refresh token."),
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            build_success_response(
                data={"access": new_access},
                message="Token refreshed.",
            ),
            status=status.HTTP_200_OK,
        )


class GoogleLoginView(APIView):
    """POST /api/v1/auth/google/ — Login with Google token."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request) -> Response:
        serializer = GoogleLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access_token = serializer.validated_data.get("access_token")
        id_token = serializer.validated_data.get("id_token")

        # Check if Google OAuth is configured
        google_cfg = getattr(settings, "SOCIALACCOUNT_PROVIDERS", {}).get("google", {})
        client_id = google_cfg.get("APP", {}).get("client_id", "")
        if not client_id:
            return Response(
                build_error_response(message="Google OAuth is not configured."),
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        # Verify token with Google
        token = access_token or id_token
        google_user_info = self._verify_google_token(token, client_id)
        if not google_user_info:
            return Response(
                build_error_response(message="Invalid Google token."),
                status=status.HTTP_400_BAD_REQUEST,
            )

        use_case = get_google_login_use_case()
        user_entity, tokens, is_new_user = use_case.execute(google_user_info)

        # Ensure UserProgress exists
        from apps.users.infrastructure.models import UserProgress
        UserProgress.objects.get_or_create(user_id=user_entity.id)

        return Response(
            build_success_response(
                data={
                    "user": _user_entity_to_dict(user_entity),
                    "tokens": tokens,
                    "is_new_user": is_new_user,
                },
                message="Google login successful.",
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _verify_google_token(token: str, client_id: str) -> dict | None:
        """Verify Google token and return user info."""
        import urllib.request
        import json

        try:
            # Try userinfo endpoint with access_token
            req = urllib.request.Request(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {token}"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                if data.get("email"):
                    return {
                        "email": data["email"],
                        "name": data.get("name", ""),
                        "google_id": data.get("sub", ""),
                    }
        except Exception:
            pass

        try:
            # Try tokeninfo endpoint for id_token
            url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                if data.get("email") and data.get("aud") == client_id:
                    return {
                        "email": data["email"],
                        "name": data.get("name", ""),
                        "google_id": data.get("sub", ""),
                    }
        except Exception:
            pass

        return None


class GoogleAuthStatusView(APIView):
    """GET /api/v1/auth/providers/ — Check Google OAuth status."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request) -> Response:
        is_configured = bool(
            getattr(settings, "SOCIALACCOUNT_PROVIDERS", {})
            .get("google", {})
            .get("APP", {})
            .get("client_id")
        )
        return Response(
            build_success_response(
                data={"google_enabled": is_configured},
                message="Auth providers status.",
            ),
            status=status.HTTP_200_OK,
        )
