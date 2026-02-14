"""
Integration tests for distractor repository operations.
Covers: get_by_word, create, update_or_create
"""

import pytest

from apps.words.infrastructure.repositories.distractor_repo import (
    DjangoWordDistractorRepository,
)


@pytest.fixture
def distractor_repo():
    return DjangoWordDistractorRepository()


@pytest.mark.django_db
class TestDjangoWordDistractorRepository:
    """Tests for DjangoWordDistractorRepository."""

    def test_create_distractor(self, sample_word, distractor_repo):
        entity = distractor_repo.create(
            word_id=sample_word.id,
            distractors=["a", "b", "c"],
            language="en",
            generated_by="test",
        )
        assert entity.word_id == sample_word.id
        assert entity.distractors == ["a", "b", "c"]
        assert entity.language == "en"
        assert entity.generated_by == "test"

    def test_get_by_word(self, sample_word, distractor_repo):
        distractor_repo.create(
            word_id=sample_word.id,
            distractors=["x", "y"],
            language="uz",
        )
        result = distractor_repo.get_by_word(sample_word.id, language="uz")
        assert result is not None
        assert result.distractors == ["x", "y"]

    def test_get_by_word_not_found(self, sample_word, distractor_repo):
        result = distractor_repo.get_by_word(sample_word.id, language="fr")
        assert result is None

    def test_update_or_create_creates(self, sample_word, distractor_repo):
        entity = distractor_repo.update_or_create(
            word_id=sample_word.id,
            distractors=["a", "b"],
            language="uz",
            generated_by="ai",
        )
        assert entity.distractors == ["a", "b"]

    def test_update_or_create_updates(self, sample_word, distractor_repo):
        distractor_repo.create(
            word_id=sample_word.id,
            distractors=["old1", "old2"],
            language="uz",
        )
        entity = distractor_repo.update_or_create(
            word_id=sample_word.id,
            distractors=["new1", "new2", "new3"],
            language="uz",
            generated_by="ai",
        )
        assert entity.distractors == ["new1", "new2", "new3"]
        assert entity.generated_by == "ai"
