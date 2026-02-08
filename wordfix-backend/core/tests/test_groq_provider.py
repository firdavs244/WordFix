"""
Tests for GroqProvider.
"""

import json
from unittest.mock import MagicMock, patch

import pytest
from django.test import override_settings

from core.interfaces.ai_provider import AIProviderError


class TestGroqProvider:
    @override_settings(
        GROQ_API_KEY="test", GROQ_MODEL="test-model",
        AI_TIMEOUT=30, AI_MAX_RETRIES=3,
    )
    def test_provider_name(self):
        from core.services.ai.groq_provider import GroqProvider

        provider = GroqProvider()
        assert provider.get_provider_name() == "groq"

    @override_settings(
        GROQ_API_KEY="", GROQ_MODEL="test-model",
        AI_TIMEOUT=30, AI_MAX_RETRIES=3,
    )
    def test_is_available_no_key(self):
        from core.services.ai.groq_provider import GroqProvider

        provider = GroqProvider()
        assert provider.is_available() is False

    @override_settings(
        GROQ_API_KEY="real-key", GROQ_MODEL="test-model",
        AI_TIMEOUT=30, AI_MAX_RETRIES=3,
    )
    def test_is_available_with_key(self):
        from core.services.ai.groq_provider import GroqProvider

        provider = GroqProvider()
        assert provider.is_available() is True

    @override_settings(
        GROQ_API_KEY="test-key", GROQ_MODEL="test-model",
        AI_TIMEOUT=30, AI_MAX_RETRIES=3,
    )
    def test_generate_text(self):
        from core.services.ai.groq_provider import GroqProvider

        provider = GroqProvider()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hello world"

        with patch.object(provider, "_client") as mock_client:
            mock_client.chat.completions.create.return_value = mock_response
            result = provider.generate_text("Say hello")
            assert result == "Hello world"

    @override_settings(
        GROQ_API_KEY="test-key", GROQ_MODEL="test-model",
        AI_TIMEOUT=30, AI_MAX_RETRIES=3,
    )
    def test_generate_json(self):
        from core.services.ai.groq_provider import GroqProvider

        provider = GroqProvider()
        expected = {"translation": "salom", "definition": "A greeting"}
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps(expected)

        with patch.object(provider, "_client") as mock_client:
            mock_client.chat.completions.create.return_value = mock_response
            result = provider.generate_json("Enrich word hello")
            assert result == expected

    @override_settings(
        GROQ_API_KEY="test-key", GROQ_MODEL="test-model",
        AI_TIMEOUT=30, AI_MAX_RETRIES=3,
    )
    def test_generate_json_invalid_json_retries(self):
        from core.services.ai.groq_provider import GroqProvider

        provider = GroqProvider()
        expected = {"key": "val"}
        mock_resp1 = MagicMock()
        mock_resp1.choices = [MagicMock()]
        mock_resp1.choices[0].message.content = "not json at all"

        mock_resp2 = MagicMock()
        mock_resp2.choices = [MagicMock()]
        mock_resp2.choices[0].message.content = json.dumps(expected)

        with patch.object(provider, "_client") as mock_client:
            mock_client.chat.completions.create.side_effect = [mock_resp1, mock_resp2]
            result = provider.generate_json("test")
            assert result == expected

    @override_settings(
        GROQ_API_KEY="test-key", GROQ_MODEL="test-model",
        AI_TIMEOUT=30, AI_MAX_RETRIES=1,
    )
    def test_generate_text_api_error(self):
        from core.services.ai.groq_provider import GroqProvider

        provider = GroqProvider()
        with patch.object(provider, "_client") as mock_client:
            mock_client.chat.completions.create.side_effect = Exception("API down")
            with pytest.raises(AIProviderError):
                provider.generate_text("Hello")

    @override_settings(
        GROQ_API_KEY="test-key", GROQ_MODEL="test-model",
        AI_TIMEOUT=30, AI_MAX_RETRIES=3,
    )
    def test_generate_chat(self):
        from core.services.ai.groq_provider import GroqProvider

        provider = GroqProvider()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Chat reply"

        with patch.object(provider, "_client") as mock_client:
            mock_client.chat.completions.create.return_value = mock_response
            result = provider.generate_chat([{"role": "user", "content": "Hi"}])
            assert result == "Chat reply"
