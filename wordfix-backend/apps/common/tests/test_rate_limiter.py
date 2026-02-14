"""
Tests for SmartRateLimiter.
"""

import pytest
from unittest.mock import MagicMock

from django.core.cache import cache

from apps.common.rate_limiter import SmartRateLimiter, AuthRateThrottle, CRUDRateThrottle


def _make_request(user=None, ip="127.0.0.1"):
    request = MagicMock()
    request.user = user
    if user:
        request.user.is_authenticated = True
        request.user.pk = user.pk if hasattr(user, "pk") else "test-uid"
    else:
        request.user = MagicMock()
        request.user.is_authenticated = False
    request.META = {"REMOTE_ADDR": ip, "HTTP_X_FORWARDED_FOR": ""}
    return request


@pytest.mark.django_db
class TestRateLimiter:

    def setup_method(self):
        cache.clear()

    def test_allows_under_limit(self):
        throttle = AuthRateThrottle()
        request = _make_request(ip="10.0.0.1")
        assert throttle.allow_request(request) is True

    def test_blocks_over_limit(self):
        throttle = AuthRateThrottle()  # 5 per 60s
        request = _make_request(ip="10.0.0.2")
        for _ in range(5):
            assert throttle.allow_request(request) is True
        assert throttle.allow_request(request) is False

    def test_resets_after_duration(self):
        """After clear, requests are allowed again."""
        throttle = AuthRateThrottle()
        request = _make_request(ip="10.0.0.3")
        for _ in range(5):
            throttle.allow_request(request)
        assert throttle.allow_request(request) is False
        # Clear cache to simulate time passing
        cache.clear()
        assert throttle.allow_request(request) is True

    def test_different_scopes(self):
        auth_throttle = AuthRateThrottle()
        crud_throttle = CRUDRateThrottle()
        request = _make_request(ip="10.0.0.4")
        # Auth allows 5, CRUD allows 60
        for _ in range(5):
            auth_throttle.allow_request(request)
        assert auth_throttle.allow_request(request) is False
        # CRUD should still be fine
        assert crud_throttle.allow_request(request) is True

    def test_user_isolation(self):
        throttle = AuthRateThrottle()
        req1 = _make_request(ip="10.0.0.5")
        req2 = _make_request(ip="10.0.0.6")
        for _ in range(5):
            throttle.allow_request(req1)
        assert throttle.allow_request(req1) is False
        # Different IP should still work
        assert throttle.allow_request(req2) is True
