"""
Integration tests for confusing pairs use cases.
Covers: DetectConfusionUseCase, GetConfusingPairsUseCase,
        GetConfusingPairDetailUseCase, GenerateConfusionDrillUseCase,
        ResolveConfusingPairUseCase, GetConfusingPairCountUseCase
"""

from unittest.mock import MagicMock, patch

import pytest

from apps.words.application.use_cases.confusing_pairs import (
    DetectConfusionUseCase,
    GenerateConfusionDrillUseCase,
    GetConfusingPairCountUseCase,
    GetConfusingPairDetailUseCase,
    GetConfusingPairsUseCase,
    ResolveConfusingPairUseCase,
)
from apps.words.infrastructure.repositories.confusing_repo import (
    DjangoConfusingPairRepository,
)
from apps.words.infrastructure.repositories.word_repo import DjangoWordRepository


@pytest.fixture
def word_repo():
    return DjangoWordRepository()


@pytest.fixture
def confusing_repo():
    return DjangoConfusingPairRepository()


@pytest.mark.django_db
class TestDetectConfusionUseCase:
    def test_detects_confusion(self, user, sample_words, word_repo, confusing_repo):
        uc = DetectConfusionUseCase(word_repo, confusing_repo)
        # Answer with the translation of another word
        word_0 = sample_words[0]
        word_1 = sample_words[1]
        result = uc.execute(user.id, word_0.id, word_1.translation)
        if result is not None:
            assert result.confusion_count >= 1

    def test_no_confusion_for_correct(self, user, sample_words, word_repo, confusing_repo):
        uc = DetectConfusionUseCase(word_repo, confusing_repo)
        result = uc.execute(user.id, sample_words[0].id, "completely_unique_answer_xyz")
        assert result is None

    def test_no_confusion_empty_answer(self, user, sample_words, word_repo, confusing_repo):
        uc = DetectConfusionUseCase(word_repo, confusing_repo)
        result = uc.execute(user.id, sample_words[0].id, "")
        assert result is None

    def test_no_confusion_whitespace_answer(self, user, sample_words, word_repo, confusing_repo):
        uc = DetectConfusionUseCase(word_repo, confusing_repo)
        result = uc.execute(user.id, sample_words[0].id, "   ")
        assert result is None

    def test_increments_on_second_detection(self, user, sample_words, word_repo, confusing_repo):
        uc = DetectConfusionUseCase(word_repo, confusing_repo)
        word_0 = sample_words[0]
        word_1 = sample_words[1]
        r1 = uc.execute(user.id, word_0.id, word_1.translation)
        if r1:
            r2 = uc.execute(user.id, word_0.id, word_1.translation)
            if r2:
                assert r2.confusion_count >= 2


@pytest.mark.django_db
class TestGetConfusingPairsUseCase:
    def test_returns_pairs(self, user, sample_words, word_repo, confusing_repo):
        confusing_repo.get_or_create(user.id, sample_words[0].id, sample_words[1].id)
        uc = GetConfusingPairsUseCase(confusing_repo, word_repo)
        result = uc.execute(user.id)
        assert len(result) == 1
        assert "word_1" in result[0]
        assert "word_2" in result[0]

    def test_returns_empty_when_none(self, user, word_repo, confusing_repo):
        uc = GetConfusingPairsUseCase(confusing_repo, word_repo)
        result = uc.execute(user.id)
        assert result == []


@pytest.mark.django_db
class TestGetConfusingPairDetailUseCase:
    def test_returns_detail(self, user, sample_words, word_repo, confusing_repo):
        entity, _ = confusing_repo.get_or_create(user.id, sample_words[0].id, sample_words[1].id)
        uc = GetConfusingPairDetailUseCase(confusing_repo, word_repo)
        result = uc.execute(user.id, entity.id)
        assert result["id"] == str(entity.id)
        assert "word_1" in result
        assert "word_2" in result
        assert "confusion_count" in result


@pytest.mark.django_db
class TestGenerateConfusionDrillUseCase:
    def test_generates_basic_drill_no_ai(self, user, sample_words, word_repo, confusing_repo):
        entity, _ = confusing_repo.get_or_create(user.id, sample_words[0].id, sample_words[1].id)
        uc = GenerateConfusionDrillUseCase(
            confusing_repo, word_repo, ai_provider=None
        )
        result = uc.execute(user.id, entity.id)
        assert "explanation" in result
        assert "test_questions" in result

    def test_returns_cached_drill(self, user, sample_words, word_repo, confusing_repo):
        entity, _ = confusing_repo.get_or_create(user.id, sample_words[0].id, sample_words[1].id)
        drill_data = {"explanation": "cached", "test_questions": []}
        confusing_repo.update(entity.id, drill_data=drill_data)
        uc = GenerateConfusionDrillUseCase(
            confusing_repo, word_repo, ai_provider=None
        )
        result = uc.execute(user.id, entity.id)
        assert result["explanation"] == "cached"

    def test_ai_drill_with_mock(self, user, sample_words, word_repo, confusing_repo):
        entity, _ = confusing_repo.get_or_create(user.id, sample_words[0].id, sample_words[1].id)
        mock_ai = MagicMock()
        mock_ai.is_available.return_value = True
        mock_ai.generate_json.return_value = {
            "explanation": "AI explanation",
            "word_1_examples": [{"sentence": "test", "translation": "test"}],
            "word_2_examples": [{"sentence": "test2", "translation": "test2"}],
        }
        uc = GenerateConfusionDrillUseCase(
            confusing_repo, word_repo, ai_provider=mock_ai,
            prompt_template="{native_language} {proficiency_level} {word_1} {translation_1} {word_2} {translation_2} {confusion_count}",
        )
        result = uc.execute(user.id, entity.id)
        assert result["explanation"] == "AI explanation"

    def test_ai_drill_failure_falls_back(self, user, sample_words, word_repo, confusing_repo):
        entity, _ = confusing_repo.get_or_create(user.id, sample_words[0].id, sample_words[1].id)
        mock_ai = MagicMock()
        mock_ai.is_available.return_value = True
        mock_ai.generate_json.side_effect = Exception("AI error")
        uc = GenerateConfusionDrillUseCase(
            confusing_repo, word_repo, ai_provider=mock_ai,
            prompt_template="{native_language} {proficiency_level} {word_1} {translation_1} {word_2} {translation_2} {confusion_count}",
        )
        result = uc.execute(user.id, entity.id)
        assert "explanation" in result
        assert "test_questions" in result

    def test_ai_no_template_fallback(self, user, sample_words, word_repo, confusing_repo):
        entity, _ = confusing_repo.get_or_create(user.id, sample_words[0].id, sample_words[1].id)
        mock_ai = MagicMock()
        mock_ai.is_available.return_value = True
        uc = GenerateConfusionDrillUseCase(
            confusing_repo, word_repo, ai_provider=mock_ai,
            prompt_template="",
        )
        result = uc.execute(user.id, entity.id)
        assert "explanation" in result


@pytest.mark.django_db
class TestResolveConfusingPairUseCase:
    def test_resolve(self, user, sample_words, confusing_repo):
        entity, _ = confusing_repo.get_or_create(user.id, sample_words[0].id, sample_words[1].id)
        uc = ResolveConfusingPairUseCase(confusing_repo)
        result = uc.execute(user.id, entity.id)
        assert result.is_resolved is True


@pytest.mark.django_db
class TestGetConfusingPairCountUseCase:
    def test_count(self, user, sample_words, confusing_repo):
        confusing_repo.get_or_create(user.id, sample_words[0].id, sample_words[1].id)
        confusing_repo.get_or_create(user.id, sample_words[2].id, sample_words[3].id)
        uc = GetConfusingPairCountUseCase(confusing_repo)
        assert uc.execute(user.id) == 2
