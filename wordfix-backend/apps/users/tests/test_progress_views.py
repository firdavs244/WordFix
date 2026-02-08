"""
Tests for Progress, XP, Badge, and Notification API views.
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.domain.services import BADGE_DEFINITIONS
from apps.users.infrastructure.models import (
    Badge,
    Notification,
    UserProgress,
    XPTransaction,
)


@pytest.fixture
def _create_badges(db):
    for defn in BADGE_DEFINITIONS:
        Badge.objects.get_or_create(
            code=defn["code"],
            defaults={
                "name": defn["name"],
                "description": defn["description"],
                "icon": defn["icon"],
                "category": defn["category"],
                "xp_reward": defn["xp_reward"],
                "rarity": defn["rarity"],
            },
        )


# =============================================================================
# PROGRESS VIEW TESTS
# =============================================================================


@pytest.mark.django_db
class TestUserProgressView:
    URL = "/api/v1/users/progress/"

    def test_get_progress_unauthenticated(self, api_client):
        response = api_client.get(self.URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_progress_default(self, authenticated_client, user):
        response = authenticated_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        data = response.data["data"]
        assert data["level"] == 1
        assert data["total_xp"] == 0

    def test_get_progress_with_xp(self, authenticated_client, user):
        # Create some progress
        p, _ = UserProgress.objects.get_or_create(user=user)
        p.total_xp = 300
        p.level = 3
        p.words_learned_total = 15
        p.save()

        response = authenticated_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        data = response.data["data"]
        assert data["level"] == 3
        assert data["total_xp"] == 300
        assert data["words_learned_total"] == 15


# =============================================================================
# XP HISTORY VIEW TESTS
# =============================================================================


@pytest.mark.django_db
class TestXPHistoryView:
    URL = "/api/v1/users/xp-history/"

    def test_xp_history_default_7_days(self, authenticated_client, user):
        response = authenticated_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 7

    def test_xp_history_custom_days(self, authenticated_client, user):
        response = authenticated_client.get(f"{self.URL}?days=14")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 14

    def test_xp_history_includes_today(self, authenticated_client, user):
        # Create a transaction for today
        XPTransaction.objects.create(
            user=user, amount=50, reason="word_added", description="Test",
        )
        response = authenticated_client.get(self.URL)
        data = response.data["data"]
        today_entry = data[-1]
        assert today_entry["xp"] == 50


# =============================================================================
# BADGE VIEW TESTS
# =============================================================================


@pytest.mark.django_db
class TestBadgeViews:
    def test_user_badges_view(self, authenticated_client, user, _create_badges):
        response = authenticated_client.get("/api/v1/users/badges/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data["data"]
        assert "badges" in data
        assert data["total_count"] == len(BADGE_DEFINITIONS)
        assert data["earned_count"] == 0

    def test_all_badges_view(self, authenticated_client, user, _create_badges):
        response = authenticated_client.get("/api/v1/badges/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == len(BADGE_DEFINITIONS)


# =============================================================================
# NOTIFICATION VIEW TESTS
# =============================================================================


@pytest.mark.django_db
class TestNotificationViews:
    def test_list_notifications_empty(self, authenticated_client, user):
        response = authenticated_client.get("/api/v1/notifications/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data["data"]
        assert data["notifications"] == []
        assert data["unread_count"] == 0

    def test_list_notifications_with_data(self, authenticated_client, user):
        for i in range(3):
            Notification.objects.create(
                user=user, type="badge_earned",
                title=f"Badge {i}", message=f"Msg {i}",
            )
        response = authenticated_client.get("/api/v1/notifications/")
        assert response.status_code == status.HTTP_200_OK
        data = response.data["data"]
        assert len(data["notifications"]) == 3
        assert data["unread_count"] == 3

    def test_mark_notification_read(self, authenticated_client, user):
        notif = Notification.objects.create(
            user=user, type="level_up", title="Level Up", message="You leveled up!",
        )
        response = authenticated_client.post(
            "/api/v1/notifications/read/",
            {"notification_id": str(notif.id)},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        notif.refresh_from_db()
        assert notif.is_read is True

    def test_mark_all_read(self, authenticated_client, user):
        for i in range(3):
            Notification.objects.create(
                user=user, type="badge_earned",
                title=f"Badge {i}", message=f"Msg {i}",
            )
        response = authenticated_client.post(
            "/api/v1/notifications/read/",
            {"all": True},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert Notification.objects.filter(user=user, is_read=False).count() == 0

    def test_unread_count(self, authenticated_client, user):
        Notification.objects.create(
            user=user, type="badge_earned", title="T", message="M",
        )
        Notification.objects.create(
            user=user, type="level_up", title="T2", message="M2", is_read=True,
        )
        response = authenticated_client.get("/api/v1/notifications/unread-count/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["count"] == 1

    def test_mark_read_missing_id(self, authenticated_client, user):
        response = authenticated_client.post(
            "/api/v1/notifications/read/",
            {},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_notifications_paginated(self, authenticated_client, user):
        for i in range(25):
            Notification.objects.create(
                user=user, type="badge_earned",
                title=f"Badge {i}", message=f"Msg {i}",
            )
        response = authenticated_client.get("/api/v1/notifications/?page=1&page_size=10")
        assert response.status_code == status.HTTP_200_OK
        data = response.data["data"]
        assert len(data["notifications"]) == 10
        meta = response.data["meta"]
        assert meta["total_count"] == 25
        assert meta["total_pages"] == 3
