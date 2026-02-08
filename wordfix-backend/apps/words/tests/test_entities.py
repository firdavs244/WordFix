"""
Tests for Word domain layer — entities.
"""

import pytest
from uuid import uuid4

from apps.words.domain.entities import WordCategoryEntity, WordEntity


class TestWordEntity:
    def test_default_values(self):
        w = WordEntity()
        assert w.original_word == ""
        assert w.difficulty_level == "medium"
        assert w.is_enriched is False
        assert w.confidence_score == 0.0
        assert w.review_count == 0
        assert w.is_mastered is False

    def test_accuracy_rate_zero(self):
        w = WordEntity(review_count=0, correct_count=0)
        assert w.accuracy_rate == 0.0

    def test_accuracy_rate_50(self):
        w = WordEntity(review_count=10, correct_count=5)
        assert w.accuracy_rate == 50.0

    def test_accuracy_rate_100(self):
        w = WordEntity(review_count=5, correct_count=5)
        assert w.accuracy_rate == 100.0

    def test_validate_valid(self):
        w = WordEntity(original_word="hello", difficulty_level="easy")
        w.validate()

    def test_validate_empty_word(self):
        w = WordEntity(original_word="")
        with pytest.raises(ValueError, match="required"):
            w.validate()

    def test_validate_whitespace_word(self):
        w = WordEntity(original_word="   ")
        with pytest.raises(ValueError, match="required"):
            w.validate()

    def test_validate_invalid_difficulty(self):
        w = WordEntity(original_word="test", difficulty_level="extreme")
        with pytest.raises(ValueError, match="Invalid difficulty"):
            w.validate()

    def test_validate_negative_confidence(self):
        w = WordEntity(original_word="test", confidence_score=-1)
        with pytest.raises(ValueError, match="negative"):
            w.validate()

    def test_validate_confidence_over_100(self):
        w = WordEntity(original_word="test", confidence_score=101)
        with pytest.raises(ValueError, match="exceed 100"):
            w.validate()

    def test_tags_default_list(self):
        w = WordEntity()
        assert w.tags == []

    def test_synonyms_default_list(self):
        w = WordEntity()
        assert w.synonyms == []

    def test_category_none_by_default(self):
        w = WordEntity()
        assert w.category is None


class TestWordCategoryEntity:
    def test_default_values(self):
        c = WordCategoryEntity()
        assert c.name == ""
        assert c.color == "#6C5CE7"
        assert c.icon == "book"
        assert c.words_count == 0

    def test_validate_valid(self):
        c = WordCategoryEntity(name="Test")
        c.validate()

    def test_validate_empty_name(self):
        c = WordCategoryEntity(name="")
        with pytest.raises(ValueError, match="required"):
            c.validate()

    def test_validate_whitespace_name(self):
        c = WordCategoryEntity(name="   ")
        with pytest.raises(ValueError, match="required"):
            c.validate()
