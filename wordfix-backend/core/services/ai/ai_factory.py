"""
AI Provider Factory — singleton cache, configurable via settings.

Includes circuit-breaker-aware fallback: if the primary provider's circuit
is open, the factory tries the alternative provider, then falls back to
a hardcoded FallbackAIProvider that never raises.
"""

import logging
from typing import Any

from django.conf import settings

from core.interfaces.ai_provider import AbstractAIProvider, AIProviderError

logger = logging.getLogger(__name__)


class UnsupportedProviderError(AIProviderError):
    """Raised when an unsupported AI provider is requested."""

    def __init__(self, name: str):
        super().__init__(f"Unsupported AI provider: {name}", provider=name)


class FallbackAIProvider(AbstractAIProvider):
    """
    Hardcoded fallback provider that returns safe default responses
    when all real providers are unavailable.  Never raises.
    """

    def generate_text(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        return "Service temporarily unavailable. Please try again later."

    def generate_json(
        self,
        prompt: str,
        response_schema: dict[str, Any] | None = None,
        max_tokens: int = 1500,
        temperature: float = 0.3,
    ) -> dict[str, Any]:
        return {
            "status": "fallback",
            "message": "AI service temporarily unavailable",
            "data": {},
        }

    def generate_chat(
        self,
        messages: list[dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str:
        return "I'm sorry, the AI service is temporarily unavailable. Please try again later."

    def get_provider_name(self) -> str:
        return "fallback"

    def is_available(self) -> bool:
        return True


class AIProviderFactory:
    """Factory for creating AI provider instances with singleton caching."""

    _instances: dict[str, AbstractAIProvider] = {}
    _fallback: FallbackAIProvider | None = None

    @classmethod
    def get_provider(cls, name: str | None = None) -> AbstractAIProvider:
        """
        Get an AI provider instance by name.

        If the requested provider's circuit breaker is open, tries the
        alternative provider, then falls back to FallbackAIProvider.

        Args:
            name: Provider name ('groq', 'openai'). Defaults to settings.AI_PROVIDER.

        Returns:
            AI provider instance.
        """
        if name is None:
            name = getattr(settings, "AI_PROVIDER", "groq")

        # Try the requested provider
        provider = cls._get_or_create(name)
        if provider and cls._is_circuit_ok(provider):
            return provider

        # Try the alternative
        alternative = "openai" if name == "groq" else "groq"
        alt_provider = cls._get_or_create(alternative)
        if alt_provider and alt_provider.is_available() and cls._is_circuit_ok(alt_provider):
            logger.warning(f"Primary provider '{name}' unavailable, using '{alternative}'")
            return alt_provider

        # All real providers exhausted → return fallback
        logger.warning("All AI providers unavailable, using fallback")
        return cls._get_fallback()

    @classmethod
    def _get_or_create(cls, name: str) -> AbstractAIProvider | None:
        if name in cls._instances:
            return cls._instances[name]
        try:
            provider = cls._create_provider(name)
            cls._instances[name] = provider
            return provider
        except Exception:
            return None

    @classmethod
    def _is_circuit_ok(cls, provider: AbstractAIProvider) -> bool:
        circuit = getattr(provider, "circuit", None)
        if circuit is None:
            return True
        return circuit.is_available()

    @classmethod
    def _create_provider(cls, name: str) -> AbstractAIProvider:
        providers = {
            "groq": "core.services.ai.groq_provider.GroqProvider",
            "openai": "core.services.ai.openai_provider.OpenAIProvider",
        }

        if name not in providers:
            raise UnsupportedProviderError(name)

        module_path, class_name = providers[name].rsplit(".", 1)
        import importlib

        module = importlib.import_module(module_path)
        provider_class = getattr(module, class_name)
        return provider_class()

    @classmethod
    def _get_fallback(cls) -> FallbackAIProvider:
        if cls._fallback is None:
            cls._fallback = FallbackAIProvider()
        return cls._fallback

    @classmethod
    def reset(cls) -> None:
        """Clear the instance cache (useful for testing)."""
        cls._instances.clear()
        cls._fallback = None
