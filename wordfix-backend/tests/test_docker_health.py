"""
Tests for Docker health check endpoint integration.
"""

import pytest


@pytest.mark.django_db
class TestDockerHealthEndpoint:
    """Integration-level tests for the health check used by Docker."""

    def test_health_endpoint_accessible(self, api_client):
        response = api_client.get("/api/v1/health/")
        assert response.status_code in (200, 503)

    def test_health_response_structure(self, api_client):
        response = api_client.get("/api/v1/health/")
        data = response.data
        assert "status" in data
        assert "version" in data
        assert "services" in data
        assert data["status"] in ("healthy", "unhealthy")

    def test_health_services_include_db(self, api_client):
        response = api_client.get("/api/v1/health/")
        assert "db" in response.data["services"]

    def test_health_services_include_redis(self, api_client):
        response = api_client.get("/api/v1/health/")
        assert "redis" in response.data["services"]

    def test_health_services_include_celery(self, api_client):
        response = api_client.get("/api/v1/health/")
        assert "celery" in response.data["services"]
