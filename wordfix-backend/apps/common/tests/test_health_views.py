"""
Tests for health/config system views.
"""

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestHealthViews:

    def test_detailed_health_200(self, api_client):
        response = api_client.get("/api/v1/system/health/detailed/")
        assert response.status_code == 200
        assert response.data["success"] is True
        assert "services" in response.data["data"]

    def test_config_status_200(self, api_client):
        response = api_client.get("/api/v1/system/config/status/")
        assert response.status_code == 200
        assert response.data["success"] is True
        assert "services" in response.data["data"]
        assert "defaults_used" in response.data["data"]

    def test_allows_anonymous(self):
        """Health endpoints don't require authentication."""
        client = APIClient()
        response = client.get("/api/v1/system/health/detailed/")
        assert response.status_code == 200
        response = client.get("/api/v1/system/config/status/")
        assert response.status_code == 200
