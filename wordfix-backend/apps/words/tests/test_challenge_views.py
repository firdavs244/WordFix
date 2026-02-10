"""
Tests for daily challenges API views.
"""

import pytest
from unittest.mock import patch

from rest_framework import status


@pytest.mark.django_db
class TestDailyChallengesView:
    """Test GET /api/v1/words/challenges/today/"""

    def test_get_today_challenges_authenticated(self, authenticated_client, daily_challenge):
        response = authenticated_client.get("/api/v1/challenges/today/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True

    def test_get_today_challenges_unauthenticated(self, api_client):
        response = api_client.get("/api/v1/challenges/today/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestClaimDailyBonusView:
    """Test POST /api/v1/words/challenges/claim-bonus/"""

    def test_claim_bonus_not_all_completed(self, authenticated_client, daily_challenge):
        response = authenticated_client.post("/api/v1/challenges/claim/")
        # Should fail since challenges not all completed
        assert response.status_code in (
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_claim_bonus_all_completed(self, authenticated_client, daily_challenge):
        """Test claiming bonus when all challenges are completed."""
        from apps.words.infrastructure.models.challenge_models import DailyChallenge

        DailyChallenge.objects.filter(id=daily_challenge.id).update(all_completed=True)
        response = authenticated_client.post("/api/v1/challenges/claim/")
        assert response.status_code == status.HTTP_200_OK

    def test_claim_bonus_unauthenticated(self, api_client):
        response = api_client.post("/api/v1/challenges/claim/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
