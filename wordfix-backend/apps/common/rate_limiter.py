"""
Smart Rate Limiter for WordFix.

Scope-based throttling with Redis (or in-memory) fallback.
"""

import logging
import time

from django.core.cache import cache
from rest_framework.throttling import BaseThrottle

logger = logging.getLogger(__name__)


class SmartRateLimiter(BaseThrottle):
    """
    Scope-based rate limiter that uses Django cache (Redis or LocMem).

    Scopes define (max_requests, window_seconds):
        auth    — 5 requests per 60 seconds
        ai      — 10 requests per 60 seconds
        crud    — 60 requests per 60 seconds
        default — 100 requests per 60 seconds
    """

    SCOPES = {
        "auth": (5, 60),
        "ai": (10, 60),
        "crud": (60, 60),
        "default": (100, 60),
    }

    scope = "default"

    def get_cache_key(self, request, view=None) -> str:
        """Build a unique key from scope + user/IP."""
        if request.user and request.user.is_authenticated:
            ident = str(request.user.pk)
        else:
            ident = self.get_ident(request) or "anon"
        return f"rate_limit:{self.scope}:{ident}"

    def allow_request(self, request, view=None) -> bool:
        """Check whether the request is within the rate limit."""
        max_requests, window = self.SCOPES.get(self.scope, self.SCOPES["default"])

        key = self.get_cache_key(request, view)
        now = time.time()

        history: list = cache.get(key, [])
        # Remove expired entries
        history = [ts for ts in history if ts > now - window]

        if len(history) >= max_requests:
            self._wait_seconds = history[0] - (now - window) if history else window
            return False

        history.append(now)
        cache.set(key, history, timeout=window * 2)
        return True

    def wait(self) -> float | None:
        """Return seconds to wait before next request is allowed."""
        return getattr(self, "_wait_seconds", None)


class AuthRateThrottle(SmartRateLimiter):
    """Rate throttle for authentication endpoints."""

    scope = "auth"


class AIRateThrottle(SmartRateLimiter):
    """Rate throttle for AI-powered endpoints."""

    scope = "ai"


class CRUDRateThrottle(SmartRateLimiter):
    """Rate throttle for standard CRUD endpoints."""

    scope = "crud"
