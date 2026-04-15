"""
Auto-provisioning JWT authentication backend.

When a valid JWT arrives but the user doesn't exist in Django's DB
(because they registered via auth-service which uses a separate DB),
this backend fetches the user profile from auth-service and creates
the user locally.
"""

import logging
import uuid

import httpx
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from apps.users.infrastructure.models.user_models import CustomUser
from apps.users.infrastructure.models.progress_models import UserProgress

logger = logging.getLogger(__name__)

AUTH_SERVICE_URL = getattr(
    settings, "AUTH_SERVICE_URL", "http://auth-service:8001"
)


class AutoProvisionJWTAuthentication(JWTAuthentication):
    """
    Extends SimpleJWT's JWTAuthentication to auto-provision users
    from the auth-service when they don't exist in Django's DB.
    """

    def get_user(self, validated_token):
        try:
            return super().get_user(validated_token)
        except AuthenticationFailed:
            # User not in Django DB — try to provision from auth-service
            user_id = validated_token.get("user_id")
            if not user_id:
                raise

            return self._provision_user(user_id, validated_token)

    def _provision_user(self, user_id, validated_token):
        """Fetch user profile from auth-service and create locally."""
        profile = self._fetch_auth_profile(user_id, validated_token)

        try:
            user_uuid = uuid.UUID(str(user_id))
        except (ValueError, AttributeError):
            raise AuthenticationFailed("Invalid user_id in token")

        try:
            user, created = CustomUser.objects.get_or_create(
                id=user_uuid,
                defaults=self._build_user_defaults(profile, user_uuid),
            )
            if created:
                UserProgress.objects.get_or_create(user=user)
                logger.info("Auto-provisioned user %s from auth-service", user.email)
            return user
        except Exception:
            logger.exception("Failed to auto-provision user %s", user_id)
            raise AuthenticationFailed("Could not provision user")

    def _fetch_auth_profile(self, user_id, validated_token):
        """Call auth-service /auth/profile/ to get user data."""
        try:
            raw_token = self._get_raw_token_from_validated(validated_token)
            resp = httpx.get(
                f"{AUTH_SERVICE_URL}/auth/profile/",
                headers={"Authorization": f"Bearer {raw_token}"},
                timeout=5.0,
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            logger.warning(
                "Could not reach auth-service for user %s, using stub", user_id
            )
        return None

    def _get_raw_token_from_validated(self, validated_token):
        """Extract the raw JWT string from the validated token object."""
        # The validated_token is a Token instance; its str() gives the encoded JWT
        return str(validated_token)

    def _build_user_defaults(self, profile, user_uuid):
        """Build the defaults dict for get_or_create."""
        if profile:
            email = profile.get("email", f"{user_uuid}@provisioned.local")
            username = profile.get("username", str(user_uuid)[:20])
            return {
                "email": email,
                "username": username,
                "full_name": profile.get("full_name", ""),
                "native_language": profile.get("native_language", "uz"),
                "learning_language": profile.get("learning_language", "en"),
                "proficiency_level": profile.get("proficiency_level", "A1"),
                "daily_goal": profile.get("daily_goal", 10),
                "timezone": profile.get("timezone", "Asia/Tashkent"),
                "is_premium": profile.get("is_premium", False),
                "has_completed_onboarding": profile.get(
                    "has_completed_onboarding", False
                ),
                "is_active": True,
            }
        # Stub user when auth-service is unreachable
        return {
            "email": f"{user_uuid}@provisioned.local",
            "username": str(user_uuid)[:20],
            "full_name": "",
            "is_active": True,
        }
