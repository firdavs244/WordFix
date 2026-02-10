"""
Tests for confusing pairs detection, drill generation, and management.
"""

import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from apps.words.application.use_cases.confusing_pairs import (
    DetectConfusionUseCase,
    GetConfusingPairsUseCase,
    GetConfusingPairDetailUseCase,
    GenerateConfusionDrillUseCase,
    ResolveConfusingPairUseCase,
    GetConfusingPairCountUseCase,
)


class TestDetectConfusionUseCase:
    """Test confusion detection logic."""

    def _make_word_entity(self, word_id, translation):
        word = MagicMock()
        word.id = word_id
        word.original_word = f"word_{translation}"
        word.translation = translation
        return word

    def test_detects_confusion_when_wrong_matches_another(self):
        """If user answers with another word's translation, detect confusion."""
        user_id = uuid4()
        word_1_id = uuid4()
        word_2_id = uuid4()

        word_1 = self._make_word_entity(word_1_id, "apple")
        word_2 = self._make_word_entity(word_2_id, "orange")

        word_repo = MagicMock()
        word_repo.get_all_by_user.return_value = ([word_1, word_2], 2)

        pair_entity = MagicMock()
        pair_entity.id = uuid4()
        pair_entity.confusion_count = 1
        confusing_pair_repo = MagicMock()
        confusing_pair_repo.get_or_create.return_value = (pair_entity, True)

        uc = DetectConfusionUseCase(word_repo, confusing_pair_repo)
        result = uc.execute(user_id, word_1_id, "orange")

        assert result is not None
        confusing_pair_repo.get_or_create.assert_called_once()

    def test_no_confusion_when_no_match(self):
        """No confusion detected when wrong answer doesn't match any word."""
        user_id = uuid4()
        word_1_id = uuid4()
        word_2_id = uuid4()

        word_1 = self._make_word_entity(word_1_id, "apple")
        word_2 = self._make_word_entity(word_2_id, "orange")

        word_repo = MagicMock()
        word_repo.get_all_by_user.return_value = ([word_1, word_2], 2)

        confusing_pair_repo = MagicMock()
        uc = DetectConfusionUseCase(word_repo, confusing_pair_repo)
        result = uc.execute(user_id, word_1_id, "banana")

        assert result is None

    def test_empty_wrong_answer_returns_none(self):
        uc = DetectConfusionUseCase(MagicMock(), MagicMock())
        assert uc.execute(uuid4(), uuid4(), "") is None
        assert uc.execute(uuid4(), uuid4(), "  ") is None

    def test_increments_existing_pair(self):
        """If pair already exists, increment confusion count."""
        user_id = uuid4()
        word_1_id = uuid4()
        word_2_id = uuid4()

        word_1 = self._make_word_entity(word_1_id, "apple")
        word_2 = self._make_word_entity(word_2_id, "orange")

        word_repo = MagicMock()
        word_repo.get_all_by_user.return_value = ([word_1, word_2], 2)

        existing_pair = MagicMock()
        existing_pair.id = uuid4()
        existing_pair.confusion_count = 3
        confusing_pair_repo = MagicMock()
        confusing_pair_repo.get_or_create.return_value = (existing_pair, False)
        confusing_pair_repo.increment_confusion.return_value = existing_pair

        uc = DetectConfusionUseCase(word_repo, confusing_pair_repo)
        result = uc.execute(user_id, word_1_id, "orange")

        confusing_pair_repo.increment_confusion.assert_called_once_with(existing_pair.id)


class TestGetConfusingPairsUseCase:
    """Test listing confusing pairs."""

    def test_returns_pairs_with_word_details(self):
        user_id = uuid4()
        pair = MagicMock()
        pair.id = uuid4()
        pair.word_1_id = uuid4()
        pair.word_2_id = uuid4()
        pair.confusion_count = 5
        pair.last_confused_at = MagicMock(isoformat=lambda: "2024-01-01T00:00:00")
        pair.is_resolved = False

        word_1 = MagicMock()
        word_1.id = pair.word_1_id
        word_1.original_word = "apple"
        word_1.translation = "olma"

        word_2 = MagicMock()
        word_2.id = pair.word_2_id
        word_2.original_word = "orange"
        word_2.translation = "apelsin"

        confusing_pair_repo = MagicMock()
        confusing_pair_repo.get_by_user.return_value = [pair]

        word_repo = MagicMock()
        word_repo.get_by_id.side_effect = [word_1, word_2]

        uc = GetConfusingPairsUseCase(confusing_pair_repo, word_repo)
        result = uc.execute(user_id)

        assert len(result) == 1
        assert result[0]["word_1"]["original_word"] == "apple"
        assert result[0]["word_2"]["original_word"] == "orange"
        assert result[0]["confusion_count"] == 5


class TestResolveConfusingPairUseCase:
    """Test resolving a confusing pair."""

    def test_resolves_pair(self):
        user_id = uuid4()
        pair_id = uuid4()

        pair = MagicMock()
        pair.id = pair_id
        pair.user_id = user_id
        pair.is_resolved = False

        confusing_pair_repo = MagicMock()
        confusing_pair_repo.get_by_id.return_value = pair
        confusing_pair_repo.resolve.return_value = pair

        uc = ResolveConfusingPairUseCase(confusing_pair_repo)
        result = uc.execute(user_id, pair_id)

        confusing_pair_repo.resolve.assert_called_once_with(pair_id=pair_id)


class TestGetConfusingPairCountUseCase:
    """Test getting count of unresolved confusing pairs."""

    def test_returns_count(self):
        user_id = uuid4()
        confusing_pair_repo = MagicMock()
        confusing_pair_repo.get_unresolved_count.return_value = 7

        uc = GetConfusingPairCountUseCase(confusing_pair_repo)
        result = uc.execute(user_id)

        assert result == 7
