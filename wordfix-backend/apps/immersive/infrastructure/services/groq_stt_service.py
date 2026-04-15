"""
Groq Whisper Speech-to-Text service.

Uses the Groq API to transcribe audio files to text.
"""

import logging

import httpx
from django.conf import settings

logger = logging.getLogger(__name__)

GROQ_STT_URL = "https://api.groq.com/openai/v1/audio/transcriptions"
GROQ_STT_MODEL = "whisper-large-v3-turbo"
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB
SUPPORTED_FORMATS = {"mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"}


class GroqSTTService:
    """Speech-to-Text service using Groq Whisper API."""

    def __init__(self):
        self._api_key = getattr(settings, "GROQ_API_KEY", "")
        self._timeout = getattr(settings, "STT_TIMEOUT", 30)

    def transcribe(
        self,
        audio_data: bytes,
        language: str = "en",
        filename: str = "audio.webm",
    ) -> str:
        """
        Transcribe audio data to text.

        Args:
            audio_data: Raw audio bytes.
            language: Language code for better accuracy.
            filename: Filename with extension for format detection.

        Returns:
            Transcribed text string.

        Raises:
            ValueError: If file is too large or format unsupported.
            RuntimeError: If Groq API call fails.
        """
        if len(audio_data) > MAX_FILE_SIZE:
            raise ValueError(f"Audio file too large: {len(audio_data)} bytes (max {MAX_FILE_SIZE})")

        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if ext and ext not in SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported audio format: {ext}. Supported: {SUPPORTED_FORMATS}")

        if not self._api_key:
            raise RuntimeError("GROQ_API_KEY not configured")

        try:
            with httpx.Client(timeout=self._timeout) as client:
                response = client.post(
                    GROQ_STT_URL,
                    headers={"Authorization": f"Bearer {self._api_key}"},
                    files={"file": (filename, audio_data)},
                    data={
                        "model": GROQ_STT_MODEL,
                        "language": language,
                        "response_format": "json",
                    },
                )
                response.raise_for_status()
                result = response.json()
                text = result.get("text", "").strip()
                logger.info("STT transcription successful: %d chars", len(text))
                return text

        except httpx.HTTPStatusError as e:
            logger.error("Groq STT API error: %s — %s", e.response.status_code, e.response.text)
            raise RuntimeError(f"Groq STT API error: {e.response.status_code}") from e
        except httpx.RequestError as e:
            logger.error("Groq STT request failed: %s", str(e))
            raise RuntimeError(f"STT request failed: {str(e)}") from e

    def is_available(self) -> bool:
        """Check if Groq STT API key is configured."""
        return bool(self._api_key)
