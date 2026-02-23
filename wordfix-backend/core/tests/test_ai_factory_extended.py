"""
Extended tests for AIProviderFactory — fallback chains, Gemini integration, endpoints.
"""

from unittest.mock import MagicMock, patch

import pytest

from core.services.ai.ai_factory import AIProviderFactory, FallbackAIProvider


class TestAIFactoryExtended:
    """Extended AI factory tests."""

    def setup_method(self):
        AIProviderFactory.reset()

    def teardown_method(self):
        AIProviderFactory.reset()

    def test_factory_groq_primary(self):
        """When AI_PROVIDER=groq, should return GroqProvider."""
        mock_groq = MagicMock()
        mock_groq.is_available.return_value = True
        mock_groq.get_provider_name.return_value = "groq"
        mock_groq.circuit = None

        AIProviderFactory._instances = {"groq": mock_groq}

        with patch("core.services.ai.ai_factory.settings") as mock_settings:
            mock_settings.AI_PROVIDER = "groq"
            provider = AIProviderFactory.get_provider()
            assert provider.get_provider_name() == "groq"

    def test_factory_gemini_primary(self):
        """When AI_PROVIDER=gemini, should return GeminiProvider."""
        mock_gemini = MagicMock()
        mock_gemini.is_available.return_value = True
        mock_gemini.get_provider_name.return_value = "gemini"
        mock_gemini.circuit = None

        AIProviderFactory._instances = {"gemini": mock_gemini}

        with patch("core.services.ai.ai_factory.settings") as mock_settings:
            mock_settings.AI_PROVIDER = "gemini"
            provider = AIProviderFactory.get_provider()
            assert provider.get_provider_name() == "gemini"

    def test_factory_fallback_chain(self):
        """When primary is unavailable, falls back to next in chain."""
        mock_groq = MagicMock()
        mock_groq.is_available.return_value = False
        mock_groq.get_provider_name.return_value = "groq"

        mock_gemini = MagicMock()
        mock_gemini.is_available.return_value = True
        mock_gemini.get_provider_name.return_value = "gemini"
        mock_gemini.circuit = None

        AIProviderFactory._instances = {"groq": mock_groq, "gemini": mock_gemini}

        with patch("core.services.ai.ai_factory.settings") as mock_settings:
            mock_settings.AI_PROVIDER = "groq"
            provider = AIProviderFactory.get_provider()
            assert provider.get_provider_name() == "gemini"

    def test_factory_all_unavailable_returns_fallback(self):
        """When all providers are unavailable, returns FallbackAIProvider."""
        for name in ("groq", "gemini", "openai"):
            mock = MagicMock()
            mock.is_available.return_value = False
            mock.get_provider_name.return_value = name
            AIProviderFactory._instances[name] = mock

        with patch("core.services.ai.ai_factory.settings") as mock_settings:
            mock_settings.AI_PROVIDER = "groq"
            provider = AIProviderFactory.get_provider()
            assert isinstance(provider, FallbackAIProvider)
            assert provider.get_provider_name() == "fallback"

    def test_fallback_provider_never_raises(self):
        """FallbackAIProvider should never raise exceptions."""
        fb = FallbackAIProvider()
        assert fb.is_available() is True
        assert isinstance(fb.generate_text("test"), str)
        assert isinstance(fb.generate_json("test"), dict)
        assert isinstance(fb.generate_chat([{"role": "user", "content": "hi"}]), str)

    def test_get_all_provider_status(self):
        """get_all_provider_status returns proper dict."""
        mock = MagicMock()
        mock.is_available.return_value = True
        mock.get_provider_name.return_value = "groq"
        mock.circuit = None

        AIProviderFactory._instances = {"groq": mock}

        with patch("core.services.ai.ai_factory.settings") as mock_settings:
            mock_settings.AI_PROVIDER = "groq"
            status = AIProviderFactory.get_all_provider_status()
            assert "active_provider" in status
            assert "providers" in status
            assert "fallback_active" in status


@pytest.mark.django_db
class TestAIStatusEndpoint:
    """Test AI status endpoint."""

    def test_ai_status_anonymous(self, api_client):
        """AI status should be accessible without auth."""
        response = api_client.get("/api/v1/system/ai-status/")
        assert response.status_code == 200
        data = response.data.get("data", response.data)
        assert "configured_providers" in data
        assert "settings_ai_provider" in data

    def test_ai_status_has_providers(self, api_client):
        """AI status should list all providers."""
        response = api_client.get("/api/v1/system/ai-status/")
        data = response.data.get("data", response.data)
        configured = data.get("configured_providers", {})
        assert "groq" in configured
        assert "gemini" in configured
        assert "openai" in configured


@pytest.mark.django_db
class TestAIPingEndpoint:
    """Test AI ping endpoint."""

    def test_ai_ping_requires_auth(self, api_client):
        response = api_client.post("/api/v1/system/ai-ping/")
        assert response.status_code == 401

    @patch("core.services.ai.ai_factory.AIProviderFactory")
    def test_ai_ping_success(self, mock_factory, authenticated_client):
        mock_provider = MagicMock()
        mock_provider.get_provider_name.return_value = "groq"
        mock_provider.generate_text.return_value = "WORKING"
        mock_factory.get_provider.return_value = mock_provider

        response = authenticated_client.post("/api/v1/system/ai-ping/")
        assert response.status_code == 200
        data = response.data.get("data", response.data)
        assert data["status"] == "working"
        assert data["provider"] == "groq"
