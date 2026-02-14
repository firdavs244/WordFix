"""
Idempotency Middleware for WordFix.

Ensures that POST requests with an X-Idempotency-Key header are
only processed once. Subsequent requests return the cached response.
"""

import hashlib
import json
import logging

from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

IDEMPOTENCY_TTL = 3600  # 1 hour


class IdempotencyMiddleware(MiddlewareMixin):
    """
    Cache POST responses by X-Idempotency-Key header.

    - Only applies to POST requests.
    - If the key has been seen, returns the previous response with
      an ``X-Idempotency-Replayed: true`` header.
    - If not, processes the request and caches a successful response.
    """

    def process_request(self, request):
        if request.method != "POST":
            return None

        idempotency_key = request.META.get("HTTP_X_IDEMPOTENCY_KEY")
        if not idempotency_key:
            return None

        # Build cache key
        user_id = ""
        if hasattr(request, "user") and request.user and request.user.is_authenticated:
            user_id = str(request.user.pk)
        else:
            user_id = request.META.get("REMOTE_ADDR", "anon")

        cache_key = f"idempotency:{user_id}:{idempotency_key}"
        cached = cache.get(cache_key)

        if cached is not None:
            response = JsonResponse(
                cached["body"],
                status=cached["status_code"],
                content_type="application/json",
            )
            response["X-Idempotency-Replayed"] = "true"
            return response

        # Store the cache key on the request for use in process_response
        request._idempotency_cache_key = cache_key
        return None

    def process_response(self, request, response):
        cache_key = getattr(request, "_idempotency_cache_key", None)
        if cache_key is None:
            return response

        # Only cache successful responses
        if 200 <= response.status_code < 300:
            try:
                body = json.loads(response.content.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                return response

            cache.set(
                cache_key,
                {"body": body, "status_code": response.status_code},
                IDEMPOTENCY_TTL,
            )

        return response
