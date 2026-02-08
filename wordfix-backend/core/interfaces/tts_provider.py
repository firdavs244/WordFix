"""
Abstract TTS (Text-to-Speech) Provider interface.
"""

from abc import ABC, abstractmethod


class AbstractTTSProvider(ABC):
    """Abstract base class for TTS provider implementations."""

    @abstractmethod
    def generate_audio(self, text: str, language: str = "en") -> bytes:
        """
        Generate audio from text.

        Args:
            text: The text to convert to speech.
            language: The language code (e.g., 'en', 'uz').

        Returns:
            Audio bytes (MP3 format).
        """
        ...

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return the name of this TTS provider."""
        ...
