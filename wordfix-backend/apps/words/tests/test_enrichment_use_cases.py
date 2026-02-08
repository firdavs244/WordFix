"""
Tests for enrichment use cases.
"""

from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from django.utils import timezone

from apps.words.application.use_cases import EnrichWordUseCase, BatchEnrichUseCase
from apps.words.domain.entities import WordEntity
from apps.words.tests.conftest import make_word_entity
from core.interfaces.ai_provider import AIProviderError


def _make_user_repo_mock(native_language="uz", proficiency_level="B1"):
    """Create a user_repo mock with get_user_language_info."""
    user_repo = MagicMock()
    user_repo.get_user_language_info.return_value = {
        "native_language": native_language,
        "proficiency_level": proficiency_level,
        "daily_goal": 10,
    }
    return user_repo


class TestEnrichWordUseCase:
    """Tests for EnrichWordUseCase."""

    def _setup_use_case(self, ai_available=True, ai_response=None, tts_provider=None, user_repo=None):
        word_repo = MagicMock()
        ai_provider = MagicMock()
        ai_provider.is_available.return_value = ai_available
        ai_provider.generate_json.return_value = ai_response or {
            "translation": "salom",
            "definition": "A greeting",
            "pronunciation": "/həˈloʊ/",
            "part_of_speech": "interjection",
            "example_sentence": "Hello, world!",
            "example_translation": "Salom, dunyo!",
            "synonyms": ["hi", "hey"],
            "antonyms": ["goodbye"],
            "collocations": ["say hello"],
            "word_family": ["hello"],
            "difficulty_level": "easy",
            "mnemonic": "Think of someone waving",
            "usage_notes": "Very common greeting",
        }

        word_entity = make_word_entity()
        word_repo.get_by_id.return_value = word_entity
        word_repo.update.return_value = word_entity

        uc = EnrichWordUseCase(word_repo, ai_provider, tts_provider, user_repo=user_repo)
        return uc, word_repo, ai_provider, word_entity

    def test_enrich_word_success(self):
        user_repo = _make_user_repo_mock()
        uc, word_repo, ai_provider, word = self._setup_use_case(user_repo=user_repo)
        result = uc.execute(str(word.id), str(word.user_id))

        ai_provider.generate_json.assert_called_once()
        assert word_repo.update.call_count >= 2  # status=enriching then final update

    def test_enrich_word_ai_unavailable_skips(self):
        uc, word_repo, ai_provider, word = self._setup_use_case(ai_available=False)
        result = uc.execute(str(word.id), str(word.user_id))

        ai_provider.generate_json.assert_not_called()

    def test_enrich_word_ai_error_marks_failed(self):
        user_repo = _make_user_repo_mock()
        uc, word_repo, ai_provider, word = self._setup_use_case(user_repo=user_repo)
        ai_provider.generate_json.side_effect = AIProviderError("API down")

        with pytest.raises(AIProviderError):
            uc.execute(str(word.id), str(word.user_id))

        # Should have updated status to failed
        failed_call = word_repo.update.call_args_list[-1]
        assert failed_call.kwargs.get("enrichment_status") == "failed"

    def test_enrich_word_user_not_found_uses_defaults(self):
        # No user_repo passed → uses defaults ("Uzbek", "B1")
        uc, word_repo, ai_provider, word = self._setup_use_case(user_repo=None)
        result = uc.execute(str(word.id), str(word.user_id))

        # Should still call AI with default language
        ai_provider.generate_json.assert_called_once()

    def test_enrich_word_user_repo_error_uses_defaults(self):
        user_repo = MagicMock()
        user_repo.get_user_language_info.side_effect = Exception("User not found")
        uc, word_repo, ai_provider, word = self._setup_use_case(user_repo=user_repo)
        result = uc.execute(str(word.id), str(word.user_id))

        # Should still call AI with default language
        ai_provider.generate_json.assert_called_once()

    def test_enrich_word_with_tts(self):
        user_repo = _make_user_repo_mock()
        tts = MagicMock()
        tts.generate_audio.return_value = b"fake mp3 audio"

        uc, word_repo, ai_provider, word = self._setup_use_case(
            tts_provider=tts, user_repo=user_repo,
        )

        with patch("builtins.open", MagicMock()):
            with patch("os.makedirs"):
                result = uc.execute(str(word.id), str(word.user_id))

        tts.generate_audio.assert_called_once()


class TestBatchEnrichUseCase:
    """Tests for BatchEnrichUseCase."""

    def test_batch_enrich_all_success(self):
        word_repo = MagicMock()
        ai_provider = MagicMock()
        ai_provider.is_available.return_value = True

        word_id1, word_id2 = uuid4(), uuid4()
        user_id = uuid4()

        word1 = make_word_entity(id=word_id1, user_id=user_id)
        word2 = make_word_entity(id=word_id2, user_id=user_id, original_word="world")

        word_repo.get_by_id.side_effect = [word1, word2]
        word_repo.update.side_effect = lambda **kwargs: word1

        ai_provider.generate_json.return_value = {
            "translation": "test", "definition": "test"
        }

        uc = BatchEnrichUseCase(word_repo, ai_provider)

        # BatchEnrichUseCase creates EnrichWordUseCase without user_repo → uses defaults
        with patch("apps.words.application.use_cases.time.sleep"):
            result = uc.execute(str(user_id), [str(word_id1), str(word_id2)])

        assert result["enriched"] == 2
        assert result["failed"] == 0

    def test_batch_enrich_partial_failure(self):
        word_repo = MagicMock()
        ai_provider = MagicMock()
        ai_provider.is_available.return_value = True

        word_id1, word_id2 = uuid4(), uuid4()
        user_id = uuid4()

        word1 = make_word_entity(id=word_id1, user_id=user_id)
        word_repo.get_by_id.side_effect = [
            word1,
            Exception("Word not found"),
        ]
        word_repo.update.return_value = word1

        ai_provider.generate_json.return_value = {"translation": "test"}

        uc = BatchEnrichUseCase(word_repo, ai_provider)

        with patch("apps.words.application.use_cases.time.sleep"):
            result = uc.execute(str(user_id), [str(word_id1), str(word_id2)])

        assert result["enriched"] == 1
        assert result["failed"] == 1
