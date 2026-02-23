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
        import json as _json
        # Extract user's last message for context-aware fallback
        user_msg = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                user_msg = m.get("content", "")
                break
        words = user_msg.split()
        word_count = len(words)
        if word_count <= 3:
            msg = "Could you tell me more about that? Try using a complete sentence so I can help you better."
        elif word_count <= 10:
            msg = f"I see you're talking about something interesting! Can you explain what you mean by '{words[-1]}' in more detail?"
        else:
            msg = "That's a great explanation! You're doing well with your English. Let me ask you a follow-up question — what made you think about this topic?"
        return _json.dumps({
            "message": msg,
            "corrections": [],
            "words_used_by_student": [],
            "encouragement": "Keep practicing! The more you write, the better you'll get."
        })

    def get_provider_name(self) -> str:
        return "fallback"

    def is_available(self) -> bool:
        return True


class AIProviderFactory:
    """Factory for creating AI provider instances with singleton caching."""

    _instances: dict[str, AbstractAIProvider] = {}
    _fallback: FallbackAIProvider | None = None

    # Fallback chains per primary provider
    _FALLBACK_CHAINS: dict[str, list[str]] = {
        "gemini": ["gemini", "groq", "openai"],
        "groq": ["groq", "gemini", "openai"],
        "openai": ["openai", "gemini", "groq"],
    }

    @classmethod
    def get_provider(cls, name: str | None = None) -> AbstractAIProvider:
        """
        Get an AI provider instance by name.

        If the requested provider's circuit breaker is open, tries the
        alternative providers in fallback chain order, then falls back
        to FallbackAIProvider.

        Args:
            name: Provider name ('groq', 'openai', 'gemini'). Defaults to settings.AI_PROVIDER.

        Returns:
            AI provider instance.
        """
        if name is None:
            name = getattr(settings, "AI_PROVIDER", "gemini")

        chain = cls._FALLBACK_CHAINS.get(name, [name, "gemini", "groq", "openai"])

        for provider_name in chain:
            provider = cls._get_or_create(provider_name)
            if provider and provider.is_available() and cls._is_circuit_ok(provider):
                if provider_name != chain[0]:
                    logger.warning(
                        f"Primary provider '{chain[0]}' unavailable, using '{provider_name}'"
                    )
                return provider

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
            "gemini": "core.services.ai.gemini_provider.GeminiProvider",
        }

        if name not in providers:
            raise UnsupportedProviderError(name)

        module_path, class_name = providers[name].rsplit(".", 1)
        import importlib

        module = importlib.import_module(module_path)
        provider_class = getattr(module, class_name)
        return provider_class()

    @classmethod
    def get_all_provider_status(cls) -> dict:
        """
        Get the status of all configured AI providers.
        Returns dict with provider info for the AI status endpoint.
        """
        provider_names = ["groq", "openai", "gemini"]
        active_provider = cls.get_provider()
        active_name = active_provider.get_provider_name()

        providers_status = {}
        for pname in provider_names:
            provider = cls._get_or_create(pname)
            if provider:
                circuit = getattr(provider, "circuit", None)
                circuit_state = "closed"
                if circuit:
                    state = circuit.get_state()
                    circuit_state = state.value
                providers_status[pname] = {
                    "configured": provider.is_available(),
                    "available": provider.is_available() and cls._is_circuit_ok(provider),
                    "circuit_breaker": circuit_state,
                }
            else:
                providers_status[pname] = {
                    "configured": False,
                    "available": False,
                    "circuit_breaker": "closed",
                }

        return {
            "active_provider": active_name,
            "providers": providers_status,
            "fallback_active": active_name == "fallback",
        }

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
