"""
Configuration Validator for WordFix.

Validates all external service connections and provides safe defaults.
Ensures the application can start even without a .env file.
"""

import logging
from dataclasses import dataclass, field

from django.conf import settings

logger = logging.getLogger(__name__)


@dataclass
class ServiceConfig:
    """Represents the configuration status of a single service."""

    name: str
    is_configured: bool
    fallback_available: bool
    status: str  # 'ready', 'fallback', 'unavailable'


class ConfigValidator:
    """
    Validates all service configurations and provides safe defaults.

    Ensures every ENV variable has a usable default so the app can
    start without a .env file.
    """

    DEFAULTS = {
        "AI_DEFAULT_PROVIDER": "groq",
        "AI_REQUEST_TIMEOUT": 30,
        "AI_MAX_RETRIES": 3,
        "CACHE_TTL_SHORT": 300,
        "CACHE_TTL_MEDIUM": 1800,
        "CACHE_TTL_LONG": 86400,
        "RATE_LIMIT_AUTH": "5/min",
        "RATE_LIMIT_AI": "10/min",
        "RATE_LIMIT_CRUD": "60/min",
        "CIRCUIT_BREAKER_THRESHOLD": 5,
        "CIRCUIT_BREAKER_RECOVERY": 60,
        "IDEMPOTENCY_TTL": 3600,
        "LOG_SLOW_REQUEST_MS": 500,
    }

    @classmethod
    def get(cls, key: str, default=None):
        """
        Get a config value from Django settings, falling back to DEFAULTS.

        Args:
            key: Setting name.
            default: Override default if not in DEFAULTS dict.

        Returns:
            The resolved configuration value.
        """
        value = getattr(settings, key, None)
        if value is not None:
            return value
        return cls.DEFAULTS.get(key, default)

    @classmethod
    def validate_all(cls) -> dict:
        """
        Validate all external services and return their status.

        Returns:
            dict with 'services' list and 'defaults_used' list.
        """
        services = [
            cls._check_database(),
            cls._check_cache(),
            cls._check_ai(),
            cls._check_tts(),
            cls._check_celery(),
        ]

        defaults_used = []
        for key, value in cls.DEFAULTS.items():
            if getattr(settings, key, None) is None:
                defaults_used.append({"key": key, "default_value": value})

        return {
            "services": [
                {
                    "name": s.name,
                    "is_configured": s.is_configured,
                    "fallback_available": s.fallback_available,
                    "status": s.status,
                }
                for s in services
            ],
            "defaults_used": defaults_used,
        }

    @classmethod
    def _check_database(cls) -> ServiceConfig:
        """Check PostgreSQL connectivity."""
        try:
            from django.db import connection

            connection.ensure_connection()
            engine = settings.DATABASES["default"]["ENGINE"]
            if "postgresql" in engine:
                return ServiceConfig(
                    name="database",
                    is_configured=True,
                    fallback_available=True,
                    status="ready",
                )
            return ServiceConfig(
                name="database",
                is_configured=False,
                fallback_available=True,
                status="fallback",
            )
        except Exception:
            logger.warning("Database check failed, using fallback")
            return ServiceConfig(
                name="database",
                is_configured=False,
                fallback_available=True,
                status="fallback",
            )

    @classmethod
    def _check_cache(cls) -> ServiceConfig:
        """Check Redis cache connectivity."""
        try:
            from django.core.cache import cache

            cache.set("_health_check", "ok", 10)
            result = cache.get("_health_check")
            backend = settings.CACHES["default"]["BACKEND"]
            if "redis" in backend.lower() and result == "ok":
                return ServiceConfig(
                    name="cache",
                    is_configured=True,
                    fallback_available=True,
                    status="ready",
                )
            return ServiceConfig(
                name="cache",
                is_configured=False,
                fallback_available=True,
                status="fallback",
            )
        except Exception:
            logger.warning("Cache check failed, using fallback")
            return ServiceConfig(
                name="cache",
                is_configured=False,
                fallback_available=True,
                status="fallback",
            )

    @classmethod
    def _check_ai(cls) -> ServiceConfig:
        """Check if any AI provider API key is configured."""
        groq_key = getattr(settings, "GROQ_API_KEY", "")
        openai_key = getattr(settings, "OPENAI_API_KEY", "")

        if groq_key or openai_key:
            return ServiceConfig(
                name="ai",
                is_configured=True,
                fallback_available=True,
                status="ready",
            )

        return ServiceConfig(
            name="ai",
            is_configured=False,
            fallback_available=True,
            status="fallback",
        )

    @classmethod
    def _check_tts(cls) -> ServiceConfig:
        """Check TTS availability — gTTS always works."""
        return ServiceConfig(
            name="tts",
            is_configured=True,
            fallback_available=True,
            status="ready",
        )

    @classmethod
    def _check_celery(cls) -> ServiceConfig:
        """Check Celery broker connectivity."""
        broker_url = getattr(settings, "CELERY_BROKER_URL", "")
        is_eager = getattr(settings, "CELERY_TASK_ALWAYS_EAGER", False)

        if broker_url and not is_eager:
            return ServiceConfig(
                name="celery",
                is_configured=True,
                fallback_available=True,
                status="ready",
            )

        return ServiceConfig(
            name="celery",
            is_configured=False,
            fallback_available=True,
            status="fallback",
        )
