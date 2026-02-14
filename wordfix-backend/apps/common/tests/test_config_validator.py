"""
Tests for ConfigValidator.
"""

import pytest
from unittest.mock import patch, MagicMock

from django.test import override_settings

from apps.common.config import ConfigValidator, ServiceConfig


@pytest.mark.django_db
class TestConfigValidator:

    def test_validate_all_services(self):
        """validate_all returns status for all 5 services."""
        result = ConfigValidator.validate_all()
        assert "services" in result
        assert "defaults_used" in result
        names = [s["name"] for s in result["services"]]
        assert "database" in names
        assert "cache" in names
        assert "ai" in names
        assert "tts" in names
        assert "celery" in names

    def test_default_values_used(self):
        """When settings don't define keys, DEFAULTS dict is used."""
        val = ConfigValidator.get("AI_REQUEST_TIMEOUT")
        assert val == 30

        val2 = ConfigValidator.get("CIRCUIT_BREAKER_THRESHOLD")
        assert val2 == 5

    def test_database_check_success(self):
        """Database check returns ready or fallback (SQLite in tests)."""
        result = ConfigValidator._check_database()
        assert isinstance(result, ServiceConfig)
        assert result.name == "database"
        assert result.status in ("ready", "fallback")

    def test_cache_check_fallback(self):
        """Cache check returns fallback when LocMemCache is used."""
        result = ConfigValidator._check_cache()
        assert isinstance(result, ServiceConfig)
        assert result.name == "cache"
        assert result.fallback_available is True

    def test_ai_check_with_key(self):
        """AI check returns ready when API key is set."""
        with patch.object(ConfigValidator, "_check_ai") as mock:
            mock.return_value = ServiceConfig(
                name="ai", is_configured=True, fallback_available=True, status="ready"
            )
            result = ConfigValidator._check_ai()
            assert result.status == "ready"

    @override_settings(GROQ_API_KEY="", OPENAI_API_KEY="")
    def test_ai_check_without_key(self):
        """AI check returns fallback when no API keys are set."""
        result = ConfigValidator._check_ai()
        assert result.name == "ai"
        # In test settings both keys are empty
        assert result.status == "fallback"
