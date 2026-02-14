"""
Tests for IdempotencyMiddleware.
"""

import json

import pytest
from django.core.cache import cache
from django.test import RequestFactory

from apps.common.idempotency import IdempotencyMiddleware


def _get_response(request):
    """Stub view that returns a JSON response."""
    from django.http import JsonResponse
    return JsonResponse({"success": True, "data": "created"}, status=201)


@pytest.mark.django_db
class TestIdempotencyMiddleware:

    def setup_method(self):
        cache.clear()
        self.factory = RequestFactory()
        self.middleware = IdempotencyMiddleware(_get_response)

    def test_no_header_normal_flow(self):
        """Without the header, request passes through normally."""
        request = self.factory.post("/api/v1/words/", content_type="application/json")
        request.user = type("User", (), {"is_authenticated": False, "pk": None})()
        response = self.middleware(request)
        assert response.status_code == 201
        assert response.get("X-Idempotency-Replayed") is None

    def test_first_request_cached(self):
        """First request with key is processed and cached."""
        request = self.factory.post(
            "/api/v1/words/",
            content_type="application/json",
            HTTP_X_IDEMPOTENCY_KEY="key-123",
        )
        request.user = type("User", (), {"is_authenticated": False, "pk": None})()
        request.META["REMOTE_ADDR"] = "127.0.0.1"
        response = self.middleware(request)
        assert response.status_code == 201
        assert response.get("X-Idempotency-Replayed") is None

    def test_replay_returns_cached(self):
        """Second request with same key returns cached response."""
        request = self.factory.post(
            "/api/v1/words/",
            content_type="application/json",
            HTTP_X_IDEMPOTENCY_KEY="key-456",
        )
        request.user = type("User", (), {"is_authenticated": False, "pk": None})()
        request.META["REMOTE_ADDR"] = "127.0.0.1"

        # First call
        self.middleware(request)

        # Second call with same key
        request2 = self.factory.post(
            "/api/v1/words/",
            content_type="application/json",
            HTTP_X_IDEMPOTENCY_KEY="key-456",
        )
        request2.user = type("User", (), {"is_authenticated": False, "pk": None})()
        request2.META["REMOTE_ADDR"] = "127.0.0.1"
        response2 = self.middleware(request2)
        assert response2.get("X-Idempotency-Replayed") == "true"

    def test_different_keys_separate(self):
        """Different keys produce independent caching."""
        for key in ("key-A", "key-B"):
            request = self.factory.post(
                "/api/v1/words/",
                content_type="application/json",
                HTTP_X_IDEMPOTENCY_KEY=key,
            )
            request.user = type("User", (), {"is_authenticated": False, "pk": None})()
            request.META["REMOTE_ADDR"] = "127.0.0.1"
            response = self.middleware(request)
            assert response.status_code == 201
            assert response.get("X-Idempotency-Replayed") is None
