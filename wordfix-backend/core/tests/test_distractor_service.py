"""
Tests for DistractorGeneratorService — AI smart distractor generation.
"""

import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from core.services.ai.distractor_service import DistractorGeneratorService


class TestDistractorGeneratorService:
    """Test distractor generation logic."""

    def _make_service(self, ai_provider=None, distractor_repo=None, word_repo=None):
        return DistractorGeneratorService(
            ai_provider=ai_provider or MagicMock(),
            distractor_repo=distractor_repo or MagicMock(),
            word_repo=word_repo or MagicMock(),
        )

    def _call_generate(self, service, word_id, user_id, **kwargs):
        """Helper to call generate_distractors with full signature."""
        defaults = {
            "word": "hello",
            "translation": "salom",
            "part_of_speech": "noun",
            "synonyms": [],
            "difficulty": "beginner",
        }
        defaults.update(kwargs)
        return service.generate_distractors(
            word_id=word_id,
            user_id=user_id,
            **defaults,
        )

    def test_returns_cached_distractors(self):
        """Should return cached distractors if available."""
        word_id = uuid4()
        cached = MagicMock()
        cached.distractors = ["goodbye", "sorry", "thanks"]

        distractor_repo = MagicMock()
        distractor_repo.get_by_word.return_value = cached

        service = self._make_service(distractor_repo=distractor_repo)
        result = self._call_generate(service, word_id, uuid4())

        assert result == ["goodbye", "sorry", "thanks"]
        distractor_repo.get_by_word.assert_called_once()

    def test_uses_ai_when_no_cache(self):
        """Should use AI provider when no cached distractors."""
        word_id = uuid4()
        user_id = uuid4()

        distractor_repo = MagicMock()
        distractor_repo.get_by_word.return_value = None

        ai_provider = MagicMock()
        ai_provider.is_available.return_value = True
        ai_provider.generate_json.return_value = {
            "distractors": ["goodbye", "sorry", "thanks"]
        }

        service = self._make_service(
            ai_provider=ai_provider,
            distractor_repo=distractor_repo,
        )
        result = self._call_generate(service, word_id, user_id)

        assert len(result) == 3
        ai_provider.generate_json.assert_called_once()

    def test_fallback_when_ai_unavailable(self):
        """Should use fallback when AI is not available."""
        word_id = uuid4()
        user_id = uuid4()

        distractor_repo = MagicMock()
        distractor_repo.get_by_word.return_value = None

        ai_provider = MagicMock()
        ai_provider.is_available.return_value = False

        other_words = []
        for t in ["goodbye", "sorry", "thanks", "please"]:
            w = MagicMock()
            w.id = uuid4()
            w.translation = t
            w.part_of_speech = "noun"
            other_words.append(w)

        word_repo = MagicMock()
        word_repo.get_all_by_user.return_value = (other_words, 4)

        service = self._make_service(
            ai_provider=ai_provider,
            distractor_repo=distractor_repo,
            word_repo=word_repo,
        )
        result = self._call_generate(service, word_id, user_id)

        assert len(result) >= 3
        assert "salom" not in result

    def test_fallback_excludes_correct_translation(self):
        """Fallback distractors should not include the correct answer."""
        word_id = uuid4()
        user_id = uuid4()

        distractor_repo = MagicMock()
        distractor_repo.get_by_word.return_value = None

        ai_provider = MagicMock()
        ai_provider.is_available.return_value = False

        other_words = []
        for t in ["salom", "goodbye", "sorry", "thanks"]:
            w = MagicMock()
            w.id = uuid4()
            w.translation = t
            w.part_of_speech = "noun"
            other_words.append(w)

        word_repo = MagicMock()
        word_repo.get_all_by_user.return_value = (other_words, 4)

        service = self._make_service(
            ai_provider=ai_provider,
            distractor_repo=distractor_repo,
            word_repo=word_repo,
        )
        result = self._call_generate(service, word_id, user_id)

        assert "salom" not in result

    def test_caches_generated_distractors(self):
        """Generated distractors should be cached in repo."""
        word_id = uuid4()
        user_id = uuid4()

        distractor_repo = MagicMock()
        distractor_repo.get_by_word.return_value = None

        ai_provider = MagicMock()
        ai_provider.is_available.return_value = True
        ai_provider.generate_json.return_value = {
            "distractors": ["goodbye", "sorry", "thanks"]
        }

        service = self._make_service(
            ai_provider=ai_provider,
            distractor_repo=distractor_repo,
        )
        self._call_generate(service, word_id, user_id)

        distractor_repo.update_or_create.assert_called_once()
