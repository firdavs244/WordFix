"""
Abstract AI Provider interface.

Defines the contract for AI text generation services.
This interface is provider-agnostic — implementations can use
OpenAI, Groq, Google Gemini, or any other provider.
"""

from abc import ABC, abstractmethod
from typing import Any


class AbstractAIProvider(ABC):
    """
    Abstract base class for AI provider implementations.

    All AI providers must implement these methods to be used
    within the WordFix system.
    """

    @abstractmethod
    def generate_text(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str:
        """Generate text based on a prompt."""
        ...

    @abstractmethod
    def generate_json(
        self,
        prompt: str,
        response_schema: dict[str, Any] | None = None,
        max_tokens: int = 1500,
        temperature: float = 0.3,
    ) -> dict[str, Any]:
        """Generate structured JSON output based on a prompt."""
        ...

    @abstractmethod
    def generate_chat(
        self,
        messages: list[dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str:
        """Generate a chat response from a list of messages."""
        ...

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return the name of this provider."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the AI provider is currently available."""
        ...


class AIProviderError(Exception):
    """Exception raised when an AI provider encounters an error."""

    def __init__(self, message: str, provider: str = "unknown") -> None:
        self.provider = provider
        super().__init__(f"[{provider}] {message}")
