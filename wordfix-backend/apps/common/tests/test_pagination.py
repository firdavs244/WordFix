"""
Tests for StandardResultsPagination.
"""

import pytest
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

from apps.common.pagination import StandardResultsPagination
from apps.users.infrastructure.models import CustomUser


class TestStandardResultsPagination:
    def test_default_page_size(self):
        p = StandardResultsPagination()
        assert p.page_size == 20

    def test_max_page_size(self):
        p = StandardResultsPagination()
        assert p.max_page_size == 100


@pytest.mark.django_db
class TestPaginatedResponse:
    def test_paginated_response_format(self):
        factory = APIRequestFactory()
        wsgi_request = factory.get("/?page=1&page_size=2")
        request = Request(wsgi_request)

        paginator = StandardResultsPagination()
        paginator.page_size = 2

        for i in range(3):
            CustomUser.objects.create_user(
                email=f"pagtest{i}@test.com",
                username=f"pagtest{i}",
                password="testpass123",
            )

        qs = CustomUser.objects.all()
        paginator.paginate_queryset(qs, request)
        response = paginator.get_paginated_response(["item1", "item2"])

        assert response.data["success"] is True
        assert response.data["data"] == ["item1", "item2"]
        assert response.data["meta"]["page"] == 1
        assert response.data["meta"]["total_count"] == 3
        assert response.data["meta"]["page_size"] == 2
