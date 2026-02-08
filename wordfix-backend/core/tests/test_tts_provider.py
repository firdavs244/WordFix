"""
Tests for TTS providers.
"""

from unittest.mock import MagicMock, patch

import pytest

from core.interfaces.tts_provider import AbstractTTSProvider


class TestAbstractTTSProvider:
    def test_cannot_instantiate(self):
        with pytest.raises(TypeError):
            AbstractTTSProvider()


class TestGoogleTTSProvider:
    def test_provider_name(self):
        from core.services.tts.google_tts import GoogleTTSProvider

        provider = GoogleTTSProvider()
        assert provider.get_provider_name() == "google_tts"

    @patch("gtts.gTTS")
    def test_generate_audio(self, mock_gtts_class):
        from core.services.tts.google_tts import GoogleTTSProvider

        mock_tts_instance = MagicMock()
        mock_tts_instance.write_to_fp = MagicMock(
            side_effect=lambda fp: fp.write(b"fake audio data")
        )
        mock_gtts_class.return_value = mock_tts_instance

        provider = GoogleTTSProvider()
        audio = provider.generate_audio("hello")
        assert isinstance(audio, bytes)
        assert len(audio) > 0

    @patch("gtts.gTTS")
    def test_generate_audio_custom_language(self, mock_gtts_class):
        from core.services.tts.google_tts import GoogleTTSProvider

        mock_tts_instance = MagicMock()
        mock_tts_instance.write_to_fp = MagicMock(
            side_effect=lambda fp: fp.write(b"french audio")
        )
        mock_gtts_class.return_value = mock_tts_instance

        provider = GoogleTTSProvider()
        audio = provider.generate_audio("bonjour", language="fr")
        assert len(audio) > 0
        mock_gtts_class.assert_called_once_with(text="bonjour", lang="fr")
