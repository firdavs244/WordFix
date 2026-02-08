"""
Tests for HealthCheck endpoint.
"""

import pytest


@pytest.mark.django_db
class TestHealthCheck:
    def test_health_check_returns_response(self, api_client):
        response = api_client.get("/api/v1/health/")
        assert response.status_code in (200, 503)

    def test_health_check_returns_version(self, api_client):
        response = api_client.get("/api/v1/health/")
        assert "version" in response.data

    def test_health_check_returns_services(self, api_client):
        response = api_client.get("/api/v1/health/")
        assert "services" in response.data
        assert "db" in response.data["services"]

    def test_health_check_db_up(self, api_client):
        response = api_client.get("/api/v1/health/")
        assert response.data["services"]["db"] == "up"
