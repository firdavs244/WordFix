"""
Tests for word archive functionality.
"""

import pytest
from rest_framework import status

from apps.words.application.use_cases.word_archive import (
    ArchiveWordUseCase,
    BulkArchiveUseCase,
    GetArchivedWordsUseCase,
    UnarchiveWordUseCase,
)
from apps.words.infrastructure.models import Word


@pytest.mark.django_db
class TestArchiveWordUseCase:
    """Test archive use cases."""

    def test_archive_word(self, user, sample_word):
        from apps.words.infrastructure.repositories import DjangoWordRepository

        repo = DjangoWordRepository()
        use_case = ArchiveWordUseCase(word_repo=repo)
        result = use_case.execute(user.id, sample_word.id)

        assert result["is_archived"] is True
        assert result["archived_at"] is not None
        sample_word.refresh_from_db()
        assert sample_word.is_archived is True

    def test_unarchive_word(self, user, sample_word):
        from apps.words.infrastructure.repositories import DjangoWordRepository

        # First archive
        sample_word.is_archived = True
        sample_word.save(update_fields=["is_archived"])

        repo = DjangoWordRepository()
        use_case = UnarchiveWordUseCase(word_repo=repo)
        result = use_case.execute(user.id, sample_word.id)

        assert result["is_archived"] is False
        sample_word.refresh_from_db()
        assert sample_word.is_archived is False

    def test_get_archived_words(self, user, sample_words):
        from apps.words.infrastructure.repositories import DjangoWordRepository

        # Archive some words
        for w in sample_words[:3]:
            w.is_archived = True
            w.save(update_fields=["is_archived"])

        repo = DjangoWordRepository()
        use_case = GetArchivedWordsUseCase(word_repo=repo)
        result = use_case.execute(user.id)

        assert result["total"] == 3
        assert len(result["words"]) == 3

    def test_bulk_archive(self, user, sample_words):
        from apps.words.infrastructure.repositories import DjangoWordRepository

        repo = DjangoWordRepository()
        word_ids = [str(w.id) for w in sample_words[:4]]
        use_case = BulkArchiveUseCase(word_repo=repo)
        result = use_case.execute(user.id, word_ids)

        assert result["archived_count"] == 4
        assert Word.objects.filter(
            user=user, is_archived=True
        ).count() == 4

    def test_archived_not_in_main_list(self, user, sample_words):
        from apps.words.infrastructure.repositories import DjangoWordRepository

        # Archive one word
        sample_words[0].is_archived = True
        sample_words[0].save(update_fields=["is_archived"])

        repo = DjangoWordRepository()
        words, total = repo.get_all_by_user(user_id=user.id, page=1, page_size=100)

        archived_ids = {sample_words[0].id}
        for w in words:
            assert w.id not in archived_ids

    def test_archive_nonexistent_word(self, user):
        from uuid import uuid4

        from apps.common.exceptions import EntityNotFoundError
        from apps.words.infrastructure.repositories import DjangoWordRepository

        repo = DjangoWordRepository()
        use_case = ArchiveWordUseCase(word_repo=repo)
        with pytest.raises(EntityNotFoundError):
            use_case.execute(user.id, uuid4())


@pytest.mark.django_db
class TestArchiveViews:
    """Test archive API endpoints."""

    def test_archive_endpoint(self, authenticated_client, sample_word):
        resp = authenticated_client.post(f"/api/v1/words/{sample_word.id}/archive/")
        assert resp.status_code == status.HTTP_200_OK
        sample_word.refresh_from_db()
        assert sample_word.is_archived is True

    def test_unarchive_endpoint(self, authenticated_client, sample_word):
        sample_word.is_archived = True
        sample_word.save(update_fields=["is_archived"])

        resp = authenticated_client.post(f"/api/v1/words/{sample_word.id}/unarchive/")
        assert resp.status_code == status.HTTP_200_OK
        sample_word.refresh_from_db()
        assert sample_word.is_archived is False

    def test_archived_list_endpoint(self, authenticated_client, sample_words):
        for w in sample_words[:2]:
            w.is_archived = True
            w.save(update_fields=["is_archived"])

        resp = authenticated_client.get("/api/v1/words/archived/")
        assert resp.status_code == status.HTTP_200_OK

    def test_bulk_archive_endpoint(self, authenticated_client, sample_words):
        word_ids = [str(w.id) for w in sample_words[:3]]
        resp = authenticated_client.post(
            "/api/v1/words/archive/bulk/",
            {"word_ids": word_ids},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK

    def test_archive_unauth(self, api_client, sample_word):
        resp = api_client.post(f"/api/v1/words/{sample_word.id}/archive/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
