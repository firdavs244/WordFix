"""
Tests for Word serializers.
"""

import pytest

from apps.words.presentation.serializers import (
    BulkWordCreateSerializer,
    WordCategorySerializer,
    WordCreateSerializer,
    WordUpdateSerializer,
)


class TestWordCreateSerializer:
    def test_valid_minimal(self):
        s = WordCreateSerializer(data={"original_word": "test", "translation": "sinov"})
        assert s.is_valid(), s.errors

    def test_missing_word(self):
        s = WordCreateSerializer(data={"translation": "sinov"})
        assert not s.is_valid()

    def test_translation_is_optional(self):
        s = WordCreateSerializer(data={"original_word": "test"})
        assert s.is_valid()  # translation has default=''

    def test_valid_full_data(self):
        data = {
            "original_word": "test",
            "translation": "sinov",
            "pronunciation": "/test/",
            "part_of_speech": "noun",
            "definition": "A test.",
            "example_sentence": "This is a test.",
            "difficulty_level": "easy",
            "tags": ["tag1"],
            "synonyms": ["exam"],
        }
        s = WordCreateSerializer(data=data)
        assert s.is_valid(), s.errors

    def test_invalid_difficulty(self):
        data = {
            "original_word": "test",
            "translation": "sinov",
            "difficulty_level": "extreme",
        }
        s = WordCreateSerializer(data=data)
        assert not s.is_valid()

    def test_word_max_length(self):
        data = {"original_word": "a" * 101, "translation": "t"}
        s = WordCreateSerializer(data=data)
        assert not s.is_valid()


class TestWordUpdateSerializer:
    def test_valid_partial(self):
        s = WordUpdateSerializer(data={"translation": "new"}, partial=True)
        assert s.is_valid()

    def test_valid_difficulty(self):
        s = WordUpdateSerializer(data={"difficulty_level": "hard"}, partial=True)
        assert s.is_valid()

    def test_invalid_difficulty(self):
        s = WordUpdateSerializer(data={"difficulty_level": "extreme"}, partial=True)
        assert not s.is_valid()


class TestBulkWordCreateSerializer:
    def test_valid(self):
        data = {
            "words": [
                {"original_word": "w1", "translation": "t1"},
                {"original_word": "w2", "translation": "t2"},
            ]
        }
        s = BulkWordCreateSerializer(data=data)
        assert s.is_valid(), s.errors

    def test_empty_list(self):
        s = BulkWordCreateSerializer(data={"words": []})
        assert not s.is_valid()

    def test_missing_words(self):
        s = BulkWordCreateSerializer(data={})
        assert not s.is_valid()


class TestWordCategorySerializer:
    def test_valid(self):
        s = WordCategorySerializer(data={"name": "Cat1"})
        assert s.is_valid()

    def test_missing_name(self):
        s = WordCategorySerializer(data={})
        assert not s.is_valid()

    def test_with_color(self):
        s = WordCategorySerializer(data={"name": "Cat", "color": "#FF0000"})
        assert s.is_valid()

    def test_with_icon(self):
        s = WordCategorySerializer(data={"name": "Cat", "icon": "star"})
        assert s.is_valid()
