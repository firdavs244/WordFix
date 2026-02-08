"""
Shared fixtures and helpers for words app tests.
"""

from uuid import uuid4

from django.utils import timezone

from apps.words.domain.entities import WordEntity


def make_word_entity(**overrides):
    """Create a minimal WordEntity for testing."""
    defaults = dict(
        id=uuid4(),
        user_id=uuid4(),
        original_word="hello",
        translation="",
        pronunciation="",
        part_of_speech="",
        definition="",
        example_sentence="",
        example_translation="",
        synonyms=[],
        antonyms=[],
        collocations=[],
        word_family=[],
        image_url="",
        audio_url="",
        notes="",
        mnemonic="",
        usage_notes="",
        category_id=None,
        category=None,
        tags=[],
        difficulty_level="medium",
        is_enriched=False,
        enrichment_status="pending",
        enrichment_error="",
        enriched_at=None,
        confidence_score=0.0,
        next_review_at=None,
        review_count=0,
        correct_count=0,
        incorrect_count=0,
        last_reviewed_at=None,
        is_mastered=False,
        easiness_factor=2.5,
        repetition_number=0,
        interval_days=0,
        is_active=True,
        created_at=timezone.now(),
        updated_at=timezone.now(),
    )
    defaults.update(overrides)
    return WordEntity(**defaults)
