"""
Tests for MistakePatternService.
"""

import pytest

from apps.users.domain.services.mistake_pattern_service import MistakePatternService


class TestMistakePatternService:

    def setup_method(self):
        self.service = MistakePatternService()

    def test_detect_l1_interference(self):
        """L1 interference pattern detected."""
        result = self.service.detect_pattern("i am agree", "i agree", "Do you agree?")
        assert result is not None
        assert result["type"] == "l1_interference"
        assert "Remove" in result["description"]

    def test_detect_morphological(self):
        """Morphological error (irregular past tense) detected."""
        result = self.service.detect_pattern("goed", "went", "I goed to the store.")
        assert result is not None
        assert result["type"] == "morphological"
        assert "Irregular past tense" in result["description"]

    def test_detect_semantic(self):
        """Semantic confusion detected."""
        result = self.service.detect_pattern("borrow", "lend", "Can you borrow me a pen?")
        assert result is not None
        assert result["type"] == "semantic"
        assert "Direction of transfer" in result["description"]

    def test_detect_spelling(self):
        """Spelling error with small Levenshtein distance detected."""
        result = self.service.detect_pattern("recieve", "receive", "")
        assert result is not None
        assert result["type"] == "spelling"

    def test_no_pattern_found(self):
        """Completely different answers return None."""
        result = self.service.detect_pattern("banana", "democracy", "")
        assert result is None

    def test_get_drill_for_pattern(self):
        """get_drill_for_pattern returns a meaningful drill."""
        for ptype in ("l1_interference", "morphological", "semantic", "spelling", "grammar"):
            drill = self.service.get_drill_for_pattern(ptype)
            assert "type" in drill
            assert "instructions" in drill
            assert "focus" in drill
