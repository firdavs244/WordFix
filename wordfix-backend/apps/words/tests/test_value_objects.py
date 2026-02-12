"""
Tests for word domain value objects.
"""

import pytest

from apps.words.domain.value_objects import WordText, Definition


class TestWordText:
    """Tests for WordText value object."""

    def test_valid_word(self):
        wt = WordText("Apple")
        assert wt.value == "apple"

    def test_strips_whitespace(self):
        wt = WordText("  hello  ")
        assert wt.value == "hello"

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            WordText("")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            WordText("   ")

    def test_too_long_raises(self):
        with pytest.raises(ValueError, match="exceed 100"):
            WordText("a" * 101)

    def test_exactly_100_chars_ok(self):
        wt = WordText("a" * 100)
        assert len(wt.value) == 100

    def test_str(self):
        wt = WordText("Hello")
        assert str(wt) == "hello"


class TestDefinition:
    """Tests for Definition value object."""

    def test_valid_definition(self):
        d = Definition("A fruit")
        assert d.value == "A fruit"

    def test_strips_whitespace(self):
        d = Definition("  trimmed  ")
        assert d.value == "trimmed"

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            Definition("")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            Definition("   ")

    def test_str(self):
        d = Definition("A greeting")
        assert str(d) == "A greeting"
