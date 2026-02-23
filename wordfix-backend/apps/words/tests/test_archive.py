"""
Tests for word archive functionality.
"""

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from apps.words.infrastructure.models import Word


@pytest.mark.django_db
class TestWordArchive:
    """Test word archive endpoints."""

    def test_archive_word(self, authenticated_client, sample_word):
        """Test archiving a word."""
        response = authenticated_client.post(f"/api/v1/words/{sample_word.id}/archive/")
        assert response.status_code == 200
        data = response.data.get("data", response.data)
        assert data["is_archived"] is True
        assert data["archived_at"] is not None

    def test_unarchive_word(self, authenticated_client, sample_word):
        """Test unarchiving a word."""
        # First archive
        sample_word.is_archived = True
        sample_word.archived_at = timezone.now()
        sample_word.save()

        response = authenticated_client.post(f"/api/v1/words/{sample_word.id}/unarchive/")
        assert response.status_code == 200
        data = response.data.get("data", response.data)
        assert data["is_archived"] is False

    def test_archived_words_list(self, authenticated_client, sample_words):
        """Test listing archived words."""
        # Archive 2 words
        for w in sample_words[:2]:
            w.is_archived = True
            w.archived_at = timezone.now()
            w.save()

        response = authenticated_client.get("/api/v1/words/archived/")
        assert response.status_code == 200
        data = response.data.get("data", response.data)
        assert len(data) == 2

    def test_bulk_archive(self, authenticated_client, sample_words):
        """Test bulk archiving words."""
        word_ids = [str(w.id) for w in sample_words[:3]]
        response = authenticated_client.post(
            "/api/v1/words/archive/bulk/",
            {"word_ids": word_ids},
            format="json",
        )
        assert response.status_code == 200
        data = response.data.get("data", response.data)
        assert data["archived_count"] == 3

    def test_archived_not_in_main_list(self, authenticated_client, sample_words):
        """Test archived words are excluded from main word list."""
        # Archive 2 words
        for w in sample_words[:2]:
            w.is_archived = True
            w.archived_at = timezone.now()
            w.save()

        response = authenticated_client.get("/api/v1/words/")
        assert response.status_code == 200
        data = response.data.get("data", response.data)
        # Should only show non-archived words (5 total - 2 archived = 3)
        # Plus sample_word from conftest might not be here, just check count is less
        word_ids = [w["id"] for w in data]
        archived_ids = [str(w.id) for w in sample_words[:2]]
        for aid in archived_ids:
            assert aid not in word_ids

    def test_archived_not_in_review(self, authenticated_client, sample_words):
        """Test archived words don't appear in review."""
        # Set words up for review and archive some
        for w in sample_words:
            w.next_review_at = timezone.now()
            w.save()
        for w in sample_words[:2]:
            w.is_archived = True
            w.archived_at = timezone.now()
            w.save()

        response = authenticated_client.get("/api/v1/words/review/")
        assert response.status_code == 200
        data = response.data.get("data", response.data)
        archived_ids = [str(w.id) for w in sample_words[:2]]
        for word_data in data:
            assert word_data.get("id") not in archived_ids
