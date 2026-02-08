"""
Google TTS Provider using gTTS (free, no API key needed).
"""

import logging
from io import BytesIO

from core.interfaces.ai_provider import AIProviderError
from core.interfaces.tts_provider import AbstractTTSProvider

logger = logging.getLogger(__name__)


class GoogleTTSProvider(AbstractTTSProvider):
    """TTS provider using Google's free gTTS library."""

    def generate_audio(self, text: str, language: str = "en") -> bytes:
        """Generate MP3 audio from text."""
        try:
            from gtts import gTTS

            tts = gTTS(text=text, lang=language)
            buffer = BytesIO()
            tts.write_to_fp(buffer)
            buffer.seek(0)
            return buffer.read()
        except ImportError:
            raise AIProviderError("gTTS package not installed", provider="google_tts")
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            raise AIProviderError(f"TTS generation failed: {e}", provider="google_tts")

    def get_provider_name(self) -> str:
        return "google_tts"
