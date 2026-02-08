"""
Tests for SpacedRepetitionService (SM-2) and WordEnrichmentDomainService.
"""

from datetime import timedelta

import pytest
from django.utils import timezone

from apps.words.domain.entities import WordEntity
from apps.words.domain.services import SpacedRepetitionService, WordEnrichmentDomainService
from apps.words.tests.conftest import make_word_entity


# =============================================================================
# SM-2 SPACED REPETITION
# =============================================================================


class TestSpacedRepetitionService:
    """Tests for SM-2 algorithm implementation."""

    def setup_method(self):
        self.sr = SpacedRepetitionService()

    def test_quality_0_resets_repetition(self):
        word = make_word_entity(easiness_factor=2.5, repetition_number=3, interval_days=10)
        self.sr.calculate_next_review(word, quality=0)
        assert word.repetition_number == 0
        assert word.interval_days == 1

    def test_quality_1_resets_repetition(self):
        word = make_word_entity(easiness_factor=2.5, repetition_number=5, interval_days=30)
        self.sr.calculate_next_review(word, quality=1)
        assert word.repetition_number == 0
        assert word.interval_days == 1

    def test_quality_2_resets_repetition(self):
        word = make_word_entity(easiness_factor=2.5, repetition_number=2, interval_days=6)
        self.sr.calculate_next_review(word, quality=2)
        assert word.repetition_number == 0

    def test_quality_3_increments_repetition(self):
        word = make_word_entity(easiness_factor=2.5, repetition_number=0, interval_days=0)
        self.sr.calculate_next_review(word, quality=3)
        assert word.repetition_number == 1
        assert word.interval_days == 1

    def test_quality_4_good_answer(self):
        word = make_word_entity(easiness_factor=2.5, repetition_number=0, interval_days=0)
        self.sr.calculate_next_review(word, quality=4)
        assert word.repetition_number == 1
        assert word.interval_days == 1

    def test_quality_5_perfect_answer(self):
        word = make_word_entity(easiness_factor=2.5, repetition_number=0, interval_days=0)
        self.sr.calculate_next_review(word, quality=5)
        assert word.repetition_number == 1
        assert word.interval_days == 1
        assert word.easiness_factor > 2.5  # Should increase

    def test_second_repetition_interval_6(self):
        word = make_word_entity(easiness_factor=2.5, repetition_number=1, interval_days=1)
        self.sr.calculate_next_review(word, quality=4)
        assert word.repetition_number == 2
        assert word.interval_days == 6

    def test_subsequent_repetitions_multiply(self):
        word = make_word_entity(easiness_factor=2.5, repetition_number=2, interval_days=6)
        self.sr.calculate_next_review(word, quality=4)
        assert word.repetition_number == 3
        assert word.interval_days == 15  # round(6 * 2.5) = 15

    def test_ef_minimum_1_3(self):
        word = make_word_entity(easiness_factor=1.3, repetition_number=0, interval_days=0)
        self.sr.calculate_next_review(word, quality=0)
        assert word.easiness_factor >= 1.3

    def test_ef_increases_with_quality_5(self):
        word = make_word_entity(easiness_factor=2.5, repetition_number=0, interval_days=0)
        self.sr.calculate_next_review(word, quality=5)
        assert word.easiness_factor > 2.5

    def test_ef_decreases_with_low_quality(self):
        word = make_word_entity(easiness_factor=2.5, repetition_number=0, interval_days=0)
        self.sr.calculate_next_review(word, quality=0)
        assert word.easiness_factor < 2.5

    def test_next_review_at_set(self):
        word = make_word_entity(easiness_factor=2.5, repetition_number=0, interval_days=0)
        self.sr.calculate_next_review(word, quality=4)
        assert word.next_review_at is not None

    def test_confidence_score_updated(self):
        word = make_word_entity(easiness_factor=2.5, repetition_number=0, interval_days=0, review_count=1, correct_count=1)
        self.sr.calculate_next_review(word, quality=4)
        assert word.confidence_score > 0

    def test_mastery_conditions(self):
        """High confidence + 5+ reps = mastered."""
        word = make_word_entity(
            easiness_factor=2.7,
            repetition_number=5,
            interval_days=30,
            review_count=10,
            correct_count=9,
            incorrect_count=1,
            last_reviewed_at=timezone.now(),
        )
        self.sr.calculate_next_review(word, quality=5)
        # With enough reps and high quality, confidence should be high
        # Mastery is set when confidence >= 95 AND reps >= 5
        assert word.repetition_number == 6

    def test_calculate_confidence_new_word(self):
        word = make_word_entity(review_count=0, correct_count=0, incorrect_count=0)
        conf = self.sr.calculate_confidence(word)
        assert conf == 0.0

    def test_calculate_confidence_with_reviews(self):
        word = make_word_entity(
            review_count=10, correct_count=8, incorrect_count=2,
            last_reviewed_at=timezone.now(),
            repetition_number=3,
        )
        conf = self.sr.calculate_confidence(word)
        assert 0 < conf <= 100

    def test_calculate_confidence_recency_bonus(self):
        """Words reviewed recently get a bonus."""
        recent_word = make_word_entity(
            review_count=5, correct_count=4, incorrect_count=1,
            last_reviewed_at=timezone.now(),
            repetition_number=2,
        )
        old_word = make_word_entity(
            review_count=5, correct_count=4, incorrect_count=1,
            last_reviewed_at=timezone.now() - timedelta(days=30),
            repetition_number=2,
        )
        recent_conf = self.sr.calculate_confidence(recent_word)
        old_conf = self.sr.calculate_confidence(old_word)
        assert recent_conf > old_conf

    def test_get_predicted_intervals(self):
        word = make_word_entity(
            easiness_factor=2.5, repetition_number=2, interval_days=6
        )
        predictions = self.sr.get_predicted_intervals(word)
        # Should have predictions for qualities 0-5
        assert len(predictions) == 6
        # Quality 5 should have longest interval
        assert 5 in predictions
        assert "day" in predictions[5]


# =============================================================================
# WORD ENRICHMENT DOMAIN SERVICE
# =============================================================================


class TestWordEnrichmentDomainService:
    """Tests for enrichment field mapping."""

    def setup_method(self):
        self.service = WordEnrichmentDomainService()

    def test_basic_enrichment(self):
        word = make_word_entity()
        data = {
            "translation": "test tarjima",
            "definition": "A test definition",
            "pronunciation": "/tɛst/",
            "part_of_speech": "noun",
            "example_sentence": "This is a test.",
            "example_translation": "Bu testdir.",
            "synonyms": ["trial", "exam"],
            "antonyms": ["certainty"],
            "collocations": ["test case", "test run"],
            "word_family": ["testing", "tested"],
            "difficulty_level": "easy",
            "mnemonic": "Think of a test paper",
            "usage_notes": "Common word",
        }
        self.service.enrich_word(word, data)

        assert word.translation == "test tarjima"
        assert word.definition == "A test definition"
        assert word.pronunciation == "/tɛst/"
        assert word.is_enriched is True
        assert word.enrichment_status == "enriched"
        assert word.enriched_at is not None

    def test_partial_enrichment(self):
        """Only provided fields should be updated."""
        word = make_word_entity(translation="existing")
        data = {"definition": "New def"}
        self.service.enrich_word(word, data)

        assert word.definition == "New def"
        assert word.translation == "existing"  # Not overwritten
        assert word.is_enriched is True

    def test_empty_data_still_marks_enriched(self):
        word = make_word_entity()
        self.service.enrich_word(word, {})
        assert word.is_enriched is True
        assert word.enrichment_status == "enriched"

    def test_list_fields_enrichment(self):
        word = make_word_entity()
        data = {
            "synonyms": ["a", "b"],
            "antonyms": ["c"],
            "collocations": ["d e"],
            "word_family": ["f"],
        }
        self.service.enrich_word(word, data)
        assert word.synonyms == ["a", "b"]
        assert word.antonyms == ["c"]

    def test_does_not_overwrite_with_empty(self):
        """If AI returns empty translation, keep existing."""
        word = make_word_entity(translation="salom")
        data = {"translation": ""}
        self.service.enrich_word(word, data)
        assert word.translation == "salom"  # Kept existing

    def test_does_not_overwrite_with_empty_list(self):
        word = make_word_entity(synonyms=["existing"])
        data = {"synonyms": []}
        self.service.enrich_word(word, data)
        assert word.synonyms == ["existing"]
