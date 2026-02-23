"""
Tests for GeminiProvider and AI factory Gemini integration.
"""

from unittest.mock import MagicMock, patch

import pytest

from core.interfaces.ai_provider import AIProviderError


# ─── GeminiProvider tests ─────────────────────────────────────────────────────


class TestGeminiProvider:
    """Tests for the Gemini AI provider."""

    @patch("apps.common.circuit_breaker.get_circuit")
    @patch("core.services.ai.gemini_provider.settings")
    def _make_provider(self, mock_settings, mock_circuit, api_key="test-key", model="gemini-2.0-flash"):
        mock_settings.GEMINI_API_KEY = api_key
        mock_settings.GEMINI_MODEL = model
        mock_settings.AI_TIMEOUT = 30
        mock_settings.AI_MAX_RETRIES = 3
        mock_circuit.return_value = MagicMock(is_available=MagicMock(return_value=True))

        from core.services.ai.gemini_provider import GeminiProvider
        provider = GeminiProvider()
        return provider

    def test_gemini_provider_name(self):
        provider = self._make_provider()
        assert provider.get_provider_name() == "gemini"

    @patch("google.generativeai.GenerativeModel")
    @patch("google.generativeai.configure")
    def test_gemini_generate_text(self, mock_configure, mock_model_cls):
        provider = self._make_provider()
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Hello!"
        mock_model.generate_content.return_value = mock_response
        mock_model_cls.return_value = mock_model

        result = provider.generate_text("Say hello")
        assert result == "Hello!"

    @patch("google.generativeai.GenerativeModel")
    @patch("google.generativeai.configure")
    def test_gemini_generate_json(self, mock_configure, mock_model_cls):
        provider = self._make_provider()
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"key": "value"}'
        mock_model.generate_content.return_value = mock_response
        mock_model_cls.return_value = mock_model

        result = provider.generate_json("Return JSON")
        assert result == {"key": "value"}

    @patch("google.generativeai.GenerativeModel")
    @patch("google.generativeai.configure")
    def test_gemini_generate_chat(self, mock_configure, mock_model_cls):
        provider = self._make_provider()
        mock_model = MagicMock()
        mock_chat = MagicMock()
        mock_chat_response = MagicMock()
        mock_chat_response.text = "Chat response"
        mock_chat.send_message.return_value = mock_chat_response
        mock_model.start_chat.return_value = mock_chat
        mock_model_cls.return_value = mock_model

        messages = [
            {"role": "system", "content": "You are helpful"},
            {"role": "user", "content": "Hi"},
        ]
        result = provider.generate_chat(messages)
        assert result == "Chat response"

    def test_gemini_not_available_without_key(self):
        provider = self._make_provider(api_key="")
        assert provider.is_available() is False


# ─── AI Factory Gemini fallback tests ────────────────────────────────────────


class TestAIFactoryGeminiFallback:
    """Test that AI factory properly handles Gemini in fallback chain."""

    def setup_method(self):
        from core.services.ai.ai_factory import AIProviderFactory
        AIProviderFactory.reset()

    @patch("core.services.ai.ai_factory.settings")
    def test_ai_factory_gemini_fallback(self, mock_settings):
        mock_settings.AI_PROVIDER = "groq"

        from core.services.ai.ai_factory import AIProviderFactory

        # When groq is unavailable and gemini is available, should fall back
        mock_groq = MagicMock()
        mock_groq.is_available.return_value = False
        mock_groq.get_provider_name.return_value = "groq"

        mock_gemini = MagicMock()
        mock_gemini.is_available.return_value = True
        mock_gemini.get_provider_name.return_value = "gemini"
        mock_gemini.circuit = None

        AIProviderFactory._instances = {"groq": mock_groq, "gemini": mock_gemini}
        provider = AIProviderFactory.get_provider()
        assert provider.get_provider_name() == "gemini"
        AIProviderFactory.reset()


# ─── AI Status endpoint test ─────────────────────────────────────────────────


@pytest.mark.django_db
class TestAIStatusEndpoint:
    """Test the AI status endpoint."""

    def test_ai_status_endpoint(self, api_client, user):
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/v1/system/ai-status/")
        assert response.status_code == 200
        data = response.data.get("data", response.data)
        assert "active_provider" in data
        assert "providers" in data
        assert "fallback_active" in data
