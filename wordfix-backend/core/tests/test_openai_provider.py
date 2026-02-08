"""
Tests for OpenAIProvider.
"""

import json
from unittest.mock import MagicMock, patch

from django.test import override_settings


class TestOpenAIProvider:
    @override_settings(
        OPENAI_API_KEY="test", OPENAI_MODEL="gpt-4o-mini",
        AI_TIMEOUT=30, AI_MAX_RETRIES=3,
    )
    def test_provider_name(self):
        from core.services.ai.openai_provider import OpenAIProvider

        provider = OpenAIProvider()
        assert provider.get_provider_name() == "openai"

    @override_settings(
        OPENAI_API_KEY="", OPENAI_MODEL="gpt-4o-mini",
        AI_TIMEOUT=30, AI_MAX_RETRIES=3,
    )
    def test_is_available_no_key(self):
        from core.services.ai.openai_provider import OpenAIProvider

        provider = OpenAIProvider()
        assert provider.is_available() is False

    @override_settings(
        OPENAI_API_KEY="test-key", OPENAI_MODEL="gpt-4o-mini",
        AI_TIMEOUT=30, AI_MAX_RETRIES=3,
    )
    def test_generate_text(self):
        from core.services.ai.openai_provider import OpenAIProvider

        provider = OpenAIProvider()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "OpenAI text"

        with patch.object(provider, "_client") as mock_client:
            mock_client.chat.completions.create.return_value = mock_response
            result = provider.generate_text("Say hello")
            assert result == "OpenAI text"

    @override_settings(
        OPENAI_API_KEY="test-key", OPENAI_MODEL="gpt-4o-mini",
        AI_TIMEOUT=30, AI_MAX_RETRIES=3,
    )
    def test_generate_json(self):
        from core.services.ai.openai_provider import OpenAIProvider

        provider = OpenAIProvider()
        expected = {"translation": "salom"}
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps(expected)

        with patch.object(provider, "_client") as mock_client:
            mock_client.chat.completions.create.return_value = mock_response
            result = provider.generate_json("Enrich")
            assert result == expected

    @override_settings(
        OPENAI_API_KEY="test-key", OPENAI_MODEL="gpt-4o-mini",
        AI_TIMEOUT=30, AI_MAX_RETRIES=3,
    )
    def test_generate_chat(self):
        from core.services.ai.openai_provider import OpenAIProvider

        provider = OpenAIProvider()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Response"

        with patch.object(provider, "_client") as mock_client:
            mock_client.chat.completions.create.return_value = mock_response
            result = provider.generate_chat([{"role": "user", "content": "test"}])
            assert result == "Response"
