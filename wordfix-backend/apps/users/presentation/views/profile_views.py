"""
Profile and health check views.
"""

import logging

from django.conf import settings
from django.core.cache import cache
from django.db import connection
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.helpers import build_success_response
from ..dependencies import (
    get_profile_use_case,
    get_update_profile_use_case,
    get_change_password_use_case,
)
from ..serializers import (
    UserProfileSerializer,
    ChangePasswordSerializer,
)
from .helpers import _user_entity_to_dict

logger = logging.getLogger(__name__)


class ProfileView(APIView):
    """GET, PATCH /api/v1/auth/profile/ — Get or update user profile."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        use_case = get_profile_use_case()
        user_entity = use_case.execute(request.user.id)
        return Response(
            build_success_response(
                data=_user_entity_to_dict(user_entity),
                message="Profile retrieved.",
            ),
            status=status.HTTP_200_OK,
        )

    def patch(self, request) -> Response:
        serializer = UserProfileSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        use_case = get_update_profile_use_case()
        user_entity = use_case.execute(request.user.id, serializer.validated_data)

        return Response(
            build_success_response(
                data=_user_entity_to_dict(user_entity),
                message="Profile updated.",
            ),
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(APIView):
    """POST /api/v1/auth/change-password/ — Change password."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_change_password_use_case()
        use_case.execute(
            user_id=request.user.id,
            old_password=serializer.validated_data["old_password"],
            new_password=serializer.validated_data["new_password"],
        )

        return Response(
            build_success_response(message="Password changed successfully."),
            status=status.HTTP_200_OK,
        )


class HealthCheckView(APIView):
    """
    Health check endpoint to verify all services are running.

    GET /api/v1/health/

    Used by Docker healthcheck — returns 200 if DB is up, 503 otherwise.
    Celery worker connectivity is not checked (would cause timeout),
    instead we report whether eager mode is active.
    """

    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = []

    def get(self, request) -> Response:
        services = {
            "db": self._check_database(),
            "redis": self._check_redis(),
            "celery": self._check_celery(),
        }

        # DB is the critical service — if it's down, we're unhealthy
        db_up = services["db"] == "up"
        overall_status = "healthy" if db_up else "unhealthy"

        health_status = {
            "status": overall_status,
            "version": getattr(settings, "APP_VERSION", "1.0.0"),
            "services": services,
        }

        http_status = (
            status.HTTP_200_OK if db_up else status.HTTP_503_SERVICE_UNAVAILABLE
        )

        return Response(health_status, status=http_status)

    @staticmethod
    def _check_database() -> str:
        """Check DB with a lightweight SELECT 1 query."""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            return "up"
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return "down"

    @staticmethod
    def _check_redis() -> str:
        """Check Redis with cache set/get ping."""
        try:
            cache.set("health_check", "ok", timeout=5)
            result = cache.get("health_check")
            return "up" if result == "ok" else "unavailable"
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return "unavailable"

    @staticmethod
    def _check_celery() -> str:
        """Check if Celery is in eager mode or has broker configured."""
        try:
            from django.conf import settings as django_settings

            if getattr(django_settings, "CELERY_TASK_ALWAYS_EAGER", False):
                return "eager_mode"
            return "up"
        except Exception as e:
            logger.error(f"Celery health check failed: {e}")
            return "down"
