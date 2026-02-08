"""
Tests for AIProviderFactory.
"""

from unittest.mock import patch

import pytest

from core.services.ai.ai_factory import AIProviderFactory


class TestAIFactory:
    def setup_method(self):
        AIProviderFactory.reset()

    def test_unsupported_provider_raises(self):
        from core.services.ai.ai_factory import UnsupportedProviderError

        with pytest.raises(UnsupportedProviderError):
            AIProviderFactory.get_provider("nonexistent")

    def test_reset_clears_cache(self):
        AIProviderFactory._instances = {"test": "cached"}
        AIProviderFactory.reset()
        assert AIProviderFactory._instances == {}

    @patch("core.services.ai.ai_factory.settings")
    def test_default_provider_from_settings(self, mock_settings):
        mock_settings.AI_PROVIDER = "groq"
        mock_settings.GROQ_API_KEY = "test-key"
        mock_settings.GROQ_MODEL = "test-model"
        mock_settings.AI_MAX_RETRIES = 3
        mock_settings.AI_TIMEOUT = 30

        provider = AIProviderFactory.get_provider()
        assert provider.get_provider_name() == "groq"

    @patch("core.services.ai.ai_factory.settings")
    def test_openai_provider_creation(self, mock_settings):
        mock_settings.OPENAI_API_KEY = "test-key"
        mock_settings.OPENAI_MODEL = "gpt-4o-mini"
        mock_settings.AI_MAX_RETRIES = 3
        mock_settings.AI_TIMEOUT = 30

        provider = AIProviderFactory.get_provider("openai")
        assert provider.get_provider_name() == "openai"

    @patch("core.services.ai.ai_factory.settings")
    def test_provider_caching(self, mock_settings):
        mock_settings.AI_PROVIDER = "groq"
        mock_settings.GROQ_API_KEY = "test-key"
        mock_settings.GROQ_MODEL = "test-model"
        mock_settings.AI_MAX_RETRIES = 3
        mock_settings.AI_TIMEOUT = 30

        p1 = AIProviderFactory.get_provider()
        p2 = AIProviderFactory.get_provider()
        assert p1 is p2
