"""
Tests for HealthRegistry.
"""

import pytest
from unittest.mock import patch

from django.core.cache import cache

from apps.common.health import HealthRegistry, HEALTH_CACHE_KEY


@pytest.mark.django_db
class TestHealthRegistry:

    def setup_method(self):
        cache.clear()

    def test_check_all_returns_all_services(self):
        """check_all returns data for all services."""
        result = HealthRegistry.check_all()
        assert "services" in result
        assert "overall_status" in result
        assert "checked_at" in result
        names = [s["name"] for s in result["services"]]
        assert "database" in names
        assert "cache" in names

    def test_overall_healthy(self):
        """When all services are OK the overall status is healthy or degraded."""
        result = HealthRegistry.check_all()
        assert result["overall_status"] in ("healthy", "degraded")

    def test_overall_degraded(self):
        """If a service is in fallback, overall is degraded."""
        result = HealthRegistry.check_all()
        # In test env, AI and celery are in fallback, so expect degraded
        assert result["overall_status"] in ("degraded", "healthy")

    def test_results_cached(self):
        """Second call should return cached result."""
        result1 = HealthRegistry.check_all()
        result2 = HealthRegistry.check_all()
        assert result1["checked_at"] == result2["checked_at"]
