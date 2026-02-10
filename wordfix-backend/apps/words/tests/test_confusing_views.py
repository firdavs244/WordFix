"""
Tests for confusing pairs API views.
"""

import pytest
from uuid import uuid4

from rest_framework import status


@pytest.mark.django_db
class TestConfusingPairsListView:
    """Test GET /api/v1/words/confusing-pairs/"""

    def test_list_confusing_pairs_authenticated(self, authenticated_client, confusing_pair):
        response = authenticated_client.get("/api/v1/words/confusing-pairs/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert isinstance(response.data["data"], list)

    def test_list_confusing_pairs_unauthenticated(self, api_client):
        response = api_client.get("/api/v1/words/confusing-pairs/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestConfusingPairDetailView:
    """Test GET /api/v1/words/confusing-pairs/{id}/"""

    def test_get_pair_detail(self, authenticated_client, confusing_pair):
        url = f"/api/v1/words/confusing-pairs/{confusing_pair.id}/"
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_nonexistent_pair(self, authenticated_client):
        url = f"/api/v1/words/confusing-pairs/{uuid4()}/"
        response = authenticated_client.get(url)
        assert response.status_code in (status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST)


@pytest.mark.django_db
class TestConfusingPairResolveView:
    """Test POST /api/v1/words/confusing-pairs/{id}/resolve/"""

    def test_resolve_pair(self, authenticated_client, confusing_pair):
        url = f"/api/v1/words/confusing-pairs/{confusing_pair.id}/resolve/"
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestConfusingPairCountView:
    """Test GET /api/v1/words/confusing-pairs/count/"""

    def test_get_count(self, authenticated_client, confusing_pair):
        response = authenticated_client.get("/api/v1/words/confusing-pairs/count/")
        assert response.status_code == status.HTTP_200_OK
        assert "count" in response.data.get("data", {})
