"""
Tests for Django settings configuration.
"""

from django.conf import settings


class TestBaseSettings:
    def test_secret_key_set(self):
        assert settings.SECRET_KEY is not None
        assert len(settings.SECRET_KEY) > 0

    def test_installed_apps_contains_custom_apps(self):
        assert any("apps.users" in app for app in settings.INSTALLED_APPS)
        assert any("apps.words" in app for app in settings.INSTALLED_APPS)

    def test_installed_apps_contains_drf(self):
        assert "rest_framework" in settings.INSTALLED_APPS

    def test_auth_user_model(self):
        assert settings.AUTH_USER_MODEL == "users.CustomUser"

    def test_rest_framework_configured(self):
        assert "DEFAULT_RENDERER_CLASSES" in settings.REST_FRAMEWORK
        assert "DEFAULT_AUTHENTICATION_CLASSES" in settings.REST_FRAMEWORK

    def test_celery_broker_configured(self):
        assert hasattr(settings, "CELERY_BROKER_URL")
        assert settings.CELERY_BROKER_URL is not None

    def test_cors_configured(self):
        assert hasattr(settings, "CORS_ALLOWED_ORIGINS") or hasattr(
            settings, "CORS_ALLOW_ALL_ORIGINS"
        )

    def test_database_configured(self):
        assert "default" in settings.DATABASES
        assert "ENGINE" in settings.DATABASES["default"]

    def test_language_code(self):
        assert settings.LANGUAGE_CODE is not None

    def test_time_zone(self):
        assert settings.TIME_ZONE is not None
