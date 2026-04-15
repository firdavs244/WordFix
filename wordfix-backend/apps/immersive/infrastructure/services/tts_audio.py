"""
TTS audio generation and storage utility for immersive sessions.

Saves NPC audio to media/audio/immersive/{session_id}/{turn_number}.mp3
"""

import logging
import os

from django.conf import settings

logger = logging.getLogger(__name__)


def save_npc_audio(tts_provider, text: str, session_id, turn_number: int, language: str = "en") -> str:
    """
    Generate TTS audio and save to disk.

    Returns:
        URL path to the audio file (e.g., /media/audio/immersive/{session_id}/{turn_number}.mp3)
        or empty string if generation fails.
    """
    if not tts_provider:
        return ""

    try:
        audio_bytes = tts_provider.generate_audio(text=text, language=language)
        if not audio_bytes:
            return ""

        # Ensure directory exists
        rel_dir = os.path.join("audio", "immersive", str(session_id))
        abs_dir = os.path.join(settings.MEDIA_ROOT, rel_dir)
        os.makedirs(abs_dir, exist_ok=True)

        # Save file
        filename = f"{turn_number}.mp3"
        abs_path = os.path.join(abs_dir, filename)
        with open(abs_path, "wb") as f:
            f.write(audio_bytes)

        # Return URL
        rel_path = os.path.join(rel_dir, filename)
        audio_url = f"/{settings.MEDIA_URL}{rel_path}"
        logger.info("TTS audio saved: %s (%d bytes)", audio_url, len(audio_bytes))
        return audio_url

    except Exception as e:
        logger.warning("TTS audio generation/save failed: %s", e)
        return ""
