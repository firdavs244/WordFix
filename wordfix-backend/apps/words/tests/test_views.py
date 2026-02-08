"""
Tests for Word API views.
"""

import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.words.infrastructure.models import Word, WordCategory


# =============================================================================
# WORD LIST / CREATE TESTS
# =============================================================================


@pytest.mark.django_db
class TestWordListCreateView:
    URL = "/api/v1/words/"

    def test_list_words(self, authenticated_client, sample_words):
        response = authenticated_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert len(response.data["data"]) == 5

    def test_list_words_empty(self, authenticated_client):
        response = authenticated_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"] == []

    def test_list_words_pagination(self, authenticated_client, sample_words):
        response = authenticated_client.get(f"{self.URL}?page_size=2&page=1")
        assert len(response.data["data"]) == 2
        assert response.data["meta"]["total_count"] == 5

    def test_list_filter_difficulty(self, authenticated_client, sample_words):
        response = authenticated_client.get(f"{self.URL}?difficulty_level=easy")
        assert response.status_code == status.HTTP_200_OK
        for w in response.data["data"]:
            assert w["difficulty_level"] == "easy"

    def test_list_filter_search(self, authenticated_client, sample_words):
        response = authenticated_client.get(f"{self.URL}?search=apple")
        assert response.data["meta"]["total_count"] == 1

    def test_list_unauthenticated(self, api_client):
        response = api_client.get(self.URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_word(self, authenticated_client):
        data = {"original_word": "create_test", "translation": "sinov"}
        response = authenticated_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["data"]["original_word"] == "create_test"

    def test_create_word_duplicate(self, authenticated_client, sample_word):
        data = {
            "original_word": sample_word.original_word,
            "translation": "dup",
        }
        response = authenticated_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_create_word_invalid(self, authenticated_client):
        response = authenticated_client.post(self.URL, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_word_unauthenticated(self, api_client):
        data = {"original_word": "test", "translation": "t"}
        response = api_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_meta_format(self, authenticated_client, sample_words):
        response = authenticated_client.get(self.URL)
        meta = response.data["meta"]
        assert "page" in meta
        assert "total_pages" in meta
        assert "total_count" in meta
        assert "page_size" in meta

    def test_user_isolation(self, authenticated_client, another_user, sample_words):
        # Create a word for another_user
        Word.objects.create(
            user=another_user,
            original_word="isolated",
            translation="izolyatsiya",
        )
        response = authenticated_client.get(self.URL)
        words = response.data["data"]
        for w in words:
            assert w["original_word"] != "isolated"


# =============================================================================
# WORD DETAIL TESTS
# =============================================================================


@pytest.mark.django_db
class TestWordDetailView:
    def _url(self, word_id):
        return f"/api/v1/words/{word_id}/"

    def test_get_detail(self, authenticated_client, sample_word):
        response = authenticated_client.get(self._url(sample_word.id))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["original_word"] == sample_word.original_word

    def test_get_detail_not_found(self, authenticated_client):
        response = authenticated_client.get(self._url(uuid.uuid4()))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_detail_wrong_user(self, another_authenticated_client, sample_word):
        response = another_authenticated_client.get(self._url(sample_word.id))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_word(self, authenticated_client, sample_word):
        response = authenticated_client.patch(
            self._url(sample_word.id),
            {"translation": "yangilangan"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["translation"] == "yangilangan"

    def test_update_not_found(self, authenticated_client):
        response = authenticated_client.patch(
            self._url(uuid.uuid4()),
            {"translation": "x"},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_word(self, authenticated_client, sample_word):
        response = authenticated_client.delete(self._url(sample_word.id))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Word.objects.filter(id=sample_word.id).exists()

    def test_delete_not_found(self, authenticated_client):
        response = authenticated_client.delete(self._url(uuid.uuid4()))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_wrong_user(self, another_authenticated_client, sample_word):
        response = another_authenticated_client.delete(self._url(sample_word.id))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_detail_unauthenticated(self, api_client, sample_word):
        response = api_client.get(self._url(sample_word.id))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# =============================================================================
# BULK CREATE TESTS
# =============================================================================


@pytest.mark.django_db
class TestWordBulkCreateView:
    URL = "/api/v1/words/bulk/"

    def test_bulk_create(self, authenticated_client):
        data = {
            "words": [
                {"original_word": "bulk1", "translation": "t1"},
                {"original_word": "bulk2", "translation": "t2"},
            ]
        }
        response = authenticated_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["data"]["created"] == 2

    def test_bulk_create_skip_dup(self, authenticated_client, sample_word):
        data = {
            "words": [
                {"original_word": sample_word.original_word, "translation": "dup"},
                {"original_word": "brand_new", "translation": "yangi"},
            ]
        }
        response = authenticated_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["data"]["created"] == 1
        assert response.data["data"]["skipped"] == 1

    def test_bulk_unauthenticated(self, api_client):
        response = api_client.post(self.URL, {"words": []}, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_bulk_empty_list(self, authenticated_client):
        response = authenticated_client.post(
            self.URL, {"words": []}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# =============================================================================
# STATS TESTS
# =============================================================================


@pytest.mark.django_db
class TestWordStatsView:
    URL = "/api/v1/words/stats/"

    def test_stats(self, authenticated_client, sample_words):
        response = authenticated_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        assert "total" in response.data["data"]
        assert response.data["data"]["total"] == 5

    def test_stats_empty(self, authenticated_client):
        response = authenticated_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["total"] == 0

    def test_stats_unauthenticated(self, api_client):
        response = api_client.get(self.URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# =============================================================================
# REVIEW TESTS
# =============================================================================


@pytest.mark.django_db
class TestWordReviewView:
    URL = "/api/v1/words/review/"

    def test_review_words(self, authenticated_client, sample_word):
        from django.utils import timezone

        sample_word.next_review_at = timezone.now() - timezone.timedelta(hours=1)
        sample_word.save()
        response = authenticated_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK

    def test_review_unauthenticated(self, api_client):
        response = api_client.get(self.URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# =============================================================================
# CATEGORY TESTS
# =============================================================================


@pytest.mark.django_db
class TestWordCategoryViews:
    URL = "/api/v1/words/categories/"

    def test_list_categories(self, authenticated_client, word_category):
        response = authenticated_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 1

    def test_list_empty(self, authenticated_client):
        response = authenticated_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"] == []

    def test_create_category(self, authenticated_client):
        data = {"name": "NewCat", "color": "#FF0000"}
        response = authenticated_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["data"]["name"] == "NewCat"

    def test_create_category_minimal(self, authenticated_client):
        data = {"name": "Minimal"}
        response = authenticated_client.post(self.URL, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_category_unauthenticated(self, api_client):
        response = api_client.post(self.URL, {"name": "x"}, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_category(self, authenticated_client, word_category):
        url = f"{self.URL}{word_category.id}/"
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_category_not_found(self, authenticated_client):
        url = f"{self.URL}{uuid.uuid4()}/"
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_category_wrong_user(self, another_authenticated_client, word_category):
        url = f"{self.URL}{word_category.id}/"
        response = another_authenticated_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_category_isolation(self, authenticated_client, another_user):
        WordCategory.objects.create(user=another_user, name="OtherCat")
        response = authenticated_client.get(self.URL)
        for c in response.data["data"]:
            assert c["name"] != "OtherCat"
