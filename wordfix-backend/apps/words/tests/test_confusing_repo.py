"""
Integration tests for confusing pair repository operations.
Covers: get_or_create, increment_confusion, get_by_user, get_by_id, update,
        resolve, get_unresolved_count
"""

import uuid

import pytest

from apps.common.exceptions import EntityNotFoundError
from apps.words.infrastructure.models import ConfusingPair
from apps.words.infrastructure.repositories.confusing_repo import (
    DjangoConfusingPairRepository,
)


@pytest.fixture
def confusing_repo():
    return DjangoConfusingPairRepository()


@pytest.mark.django_db
class TestDjangoConfusingPairRepository:
    """Tests for DjangoConfusingPairRepository."""

    def test_get_or_create_new(self, user, sample_words, confusing_repo):
        w1, w2 = sample_words[0], sample_words[1]
        entity, created = confusing_repo.get_or_create(user.id, w1.id, w2.id)
        assert created is True
        assert entity.user_id == user.id
        assert entity.confusion_count == 1

    def test_get_or_create_existing(self, user, sample_words, confusing_repo):
        w1, w2 = sample_words[0], sample_words[1]
        _, created1 = confusing_repo.get_or_create(user.id, w1.id, w2.id)
        _, created2 = confusing_repo.get_or_create(user.id, w1.id, w2.id)
        assert created1 is True
        assert created2 is False

    def test_get_or_create_order_invariant(self, user, sample_words, confusing_repo):
        w1, w2 = sample_words[0], sample_words[1]
        e1, _ = confusing_repo.get_or_create(user.id, w1.id, w2.id)
        e2, created = confusing_repo.get_or_create(user.id, w2.id, w1.id)
        assert created is False
        assert e1.id == e2.id

    def test_increment_confusion(self, user, sample_words, confusing_repo):
        w1, w2 = sample_words[0], sample_words[1]
        entity, _ = confusing_repo.get_or_create(user.id, w1.id, w2.id)
        updated = confusing_repo.increment_confusion(entity.id)
        assert updated.confusion_count == 2
        assert updated.is_resolved is False

    def test_increment_confusion_nonexistent(self, confusing_repo):
        with pytest.raises(EntityNotFoundError):
            confusing_repo.increment_confusion(uuid.uuid4())

    def test_get_by_user(self, user, sample_words, confusing_repo):
        confusing_repo.get_or_create(user.id, sample_words[0].id, sample_words[1].id)
        confusing_repo.get_or_create(user.id, sample_words[2].id, sample_words[3].id)
        pairs = confusing_repo.get_by_user(user.id)
        assert len(pairs) == 2

    def test_get_by_user_excludes_resolved(self, user, sample_words, confusing_repo):
        e1, _ = confusing_repo.get_or_create(user.id, sample_words[0].id, sample_words[1].id)
        confusing_repo.get_or_create(user.id, sample_words[2].id, sample_words[3].id)
        confusing_repo.resolve(e1.id)
        pairs = confusing_repo.get_by_user(user.id, include_resolved=False)
        assert len(pairs) == 1

    def test_get_by_user_includes_resolved(self, user, sample_words, confusing_repo):
        e1, _ = confusing_repo.get_or_create(user.id, sample_words[0].id, sample_words[1].id)
        confusing_repo.resolve(e1.id)
        pairs = confusing_repo.get_by_user(user.id, include_resolved=True)
        assert len(pairs) == 1

    def test_get_by_id(self, user, sample_words, confusing_repo):
        entity, _ = confusing_repo.get_or_create(user.id, sample_words[0].id, sample_words[1].id)
        result = confusing_repo.get_by_id(entity.id, user.id)
        assert result.id == entity.id

    def test_get_by_id_not_found(self, user, confusing_repo):
        with pytest.raises(EntityNotFoundError):
            confusing_repo.get_by_id(uuid.uuid4(), user.id)

    def test_update(self, user, sample_words, confusing_repo):
        entity, _ = confusing_repo.get_or_create(user.id, sample_words[0].id, sample_words[1].id)
        updated = confusing_repo.update(entity.id, confusion_count=10)
        assert updated.confusion_count == 10

    def test_update_nonexistent(self, confusing_repo):
        with pytest.raises(EntityNotFoundError):
            confusing_repo.update(uuid.uuid4(), confusion_count=5)

    def test_resolve(self, user, sample_words, confusing_repo):
        entity, _ = confusing_repo.get_or_create(user.id, sample_words[0].id, sample_words[1].id)
        resolved = confusing_repo.resolve(entity.id)
        assert resolved.is_resolved is True

    def test_resolve_nonexistent(self, confusing_repo):
        with pytest.raises(EntityNotFoundError):
            confusing_repo.resolve(uuid.uuid4())

    def test_get_unresolved_count(self, user, sample_words, confusing_repo):
        confusing_repo.get_or_create(user.id, sample_words[0].id, sample_words[1].id)
        confusing_repo.get_or_create(user.id, sample_words[2].id, sample_words[3].id)
        count = confusing_repo.get_unresolved_count(user.id)
        assert count == 2

    def test_get_unresolved_count_after_resolve(self, user, sample_words, confusing_repo):
        e1, _ = confusing_repo.get_or_create(user.id, sample_words[0].id, sample_words[1].id)
        confusing_repo.resolve(e1.id)
        count = confusing_repo.get_unresolved_count(user.id)
        assert count == 0
