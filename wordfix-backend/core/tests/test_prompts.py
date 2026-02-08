"""
Tests for AI prompt templates and language map.
"""

from core.services.ai.prompts import NATIVE_LANGUAGE_MAP, WORD_ENRICHMENT_PROMPT


class TestNativeLanguageMap:
    def test_contains_common_languages(self):
        assert "uz" in NATIVE_LANGUAGE_MAP
        assert "ru" in NATIVE_LANGUAGE_MAP
        assert "tr" in NATIVE_LANGUAGE_MAP
        assert "ko" in NATIVE_LANGUAGE_MAP
        assert NATIVE_LANGUAGE_MAP["uz"] == "Uzbek"

    def test_minimum_count(self):
        assert len(NATIVE_LANGUAGE_MAP) >= 12


class TestWordEnrichmentPrompt:
    def test_template_formatting(self):
        prompt = WORD_ENRICHMENT_PROMPT.format(
            native_language="Uzbek",
            learning_language="English",
            proficiency_level="B1",
            word="hello",
        )
        assert "hello" in prompt
        assert "Uzbek" in prompt
        assert "B1" in prompt
        assert "JSON" in prompt

    def test_contains_json_keys(self):
        prompt = WORD_ENRICHMENT_PROMPT.format(
            native_language="Russian",
            learning_language="English",
            proficiency_level="A2",
            word="test",
        )
        assert "translation" in prompt
        assert "definition" in prompt
        assert "example_sentence" in prompt
