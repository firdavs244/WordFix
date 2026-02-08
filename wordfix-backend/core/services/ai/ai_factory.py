"""
AI Provider Factory — singleton cache, configurable via settings.
"""

import logging

from django.conf import settings

from core.interfaces.ai_provider import AbstractAIProvider, AIProviderError

logger = logging.getLogger(__name__)


class UnsupportedProviderError(AIProviderError):
    """Raised when an unsupported AI provider is requested."""

    def __init__(self, name: str):
        super().__init__(f"Unsupported AI provider: {name}", provider=name)


class AIProviderFactory:
    """Factory for creating AI provider instances with singleton caching."""

    _instances: dict[str, AbstractAIProvider] = {}

    @classmethod
    def get_provider(cls, name: str | None = None) -> AbstractAIProvider:
        """
        Get an AI provider instance by name.

        Args:
            name: Provider name ('groq', 'openai'). Defaults to settings.AI_PROVIDER.

        Returns:
            AI provider instance.
        """
        if name is None:
            name = getattr(settings, "AI_PROVIDER", "groq")

        if name in cls._instances:
            return cls._instances[name]

        provider = cls._create_provider(name)
        cls._instances[name] = provider
        return provider

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
    def reset(cls) -> None:
        """Clear the instance cache (useful for testing)."""
        cls._instances.clear()
