"""
Tests for Notification service and repository.
"""

import pytest

from apps.users.domain.services import NotificationService
from apps.users.infrastructure.models import Notification
from apps.users.infrastructure.repositories import DjangoNotificationRepository


@pytest.fixture
def notification_service(db):
    return NotificationService(
        notification_repo=DjangoNotificationRepository(),
    )


@pytest.mark.django_db
class TestNotificationService:
    def test_create_notification(self, user, notification_service):
        notif = notification_service.create_notification(
            user_id=user.id,
            notification_type="badge_earned",
            title="Test Badge",
            message="You earned a badge!",
            data={"badge_code": "test"},
        )
        assert notif.title == "Test Badge"
        assert notif.type == "badge_earned"
        assert Notification.objects.count() == 1

    def test_get_unread_count(self, user, notification_service):
        notification_service.create_notification(
            user.id, "badge_earned", "T1", "M1",
        )
        notification_service.create_notification(
            user.id, "level_up", "T2", "M2",
        )
        assert notification_service.get_unread_count(user.id) == 2

    def test_mark_as_read(self, user, notification_service):
        notif = notification_service.create_notification(
            user.id, "badge_earned", "T1", "M1",
        )
        result = notification_service.mark_as_read(notif.id, user.id)
        assert result is True
        assert notification_service.get_unread_count(user.id) == 0

    def test_mark_all_as_read(self, user, notification_service):
        notification_service.create_notification(user.id, "badge_earned", "T1", "M1")
        notification_service.create_notification(user.id, "level_up", "T2", "M2")
        count = notification_service.mark_all_as_read(user.id)
        assert count == 2
        assert notification_service.get_unread_count(user.id) == 0

    def test_get_notifications_paginated(self, user, notification_service):
        for i in range(5):
            notification_service.create_notification(
                user.id, "badge_earned", f"Title {i}", f"Message {i}",
            )
        notifications, total = notification_service.get_notifications(
            user.id, page=1, page_size=3,
        )
        assert len(notifications) == 3
        assert total == 5

    def test_get_notifications_page_2(self, user, notification_service):
        for i in range(5):
            notification_service.create_notification(
                user.id, "badge_earned", f"Title {i}", f"Message {i}",
            )
        notifications, total = notification_service.get_notifications(
            user.id, page=2, page_size=3,
        )
        assert len(notifications) == 2
        assert total == 5

    def test_mark_read_wrong_user(self, user, another_user, notification_service):
        notif = notification_service.create_notification(
            user.id, "badge_earned", "T1", "M1",
        )
        # another_user should not be able to mark it read
        result = notification_service.mark_as_read(notif.id, another_user.id)
        assert result is False
        assert notification_service.get_unread_count(user.id) == 1

    def test_notification_data_json(self, user, notification_service):
        notif = notification_service.create_notification(
            user.id, "weekly_report", "Weekly Report", "Summary",
            data={"words_learned": 10, "xp_earned": 200},
        )
        assert notif.data["words_learned"] == 10
        assert notif.data["xp_earned"] == 200
