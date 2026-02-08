"""
Tests for AbstractBaseModel.
"""

import uuid

import pytest

from apps.words.infrastructure.models import Word


@pytest.mark.django_db
class TestAbstractBaseModel:
    def test_uuid_pk_auto_generated(self, sample_word):
        assert sample_word.id is not None
        assert isinstance(sample_word.id, uuid.UUID)

    def test_created_at_auto_set(self, sample_word):
        assert sample_word.created_at is not None

    def test_updated_at_auto_set(self, sample_word):
        assert sample_word.updated_at is not None

    def test_is_active_default_true(self, sample_word):
        assert sample_word.is_active is True

    def test_soft_delete(self, sample_word):
        sample_word.soft_delete()
        sample_word.refresh_from_db()
        assert sample_word.is_active is False

    def test_restore(self, sample_word):
        sample_word.soft_delete()
        sample_word.restore()
        sample_word.refresh_from_db()
        assert sample_word.is_active is True
