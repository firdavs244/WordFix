"""
Notification repository implementation using Django ORM.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from apps.users.infrastructure.models import Notification


@dataclass
class NotificationEntity:
    id: UUID
    user_id: UUID
    type: str
    title: str
    message: str
    is_read: bool
    data: dict
    created_at: datetime


class DjangoNotificationRepository:
    """Repository for Notification."""

    def _to_entity(self, n: Notification) -> NotificationEntity:
        return NotificationEntity(
            id=n.id, user_id=n.user_id, type=n.type, title=n.title,
            message=n.message, is_read=n.is_read, data=n.data,
            created_at=n.created_at,
        )

    def create(self, user_id: UUID, notification_type: str, title: str,
               message: str, data: dict | None = None) -> NotificationEntity:
        n = Notification.objects.create(
            user_id=user_id, type=notification_type, title=title,
            message=message, data=data or {},
        )
        return self._to_entity(n)

    def get_unread_count(self, user_id: UUID) -> int:
        return Notification.objects.filter(user_id=user_id, is_read=False).count()

    def get_by_user(self, user_id: UUID, page: int = 1,
                    page_size: int = 20) -> tuple[list[NotificationEntity], int]:
        qs = Notification.objects.filter(user_id=user_id)
        total = qs.count()
        offset = (page - 1) * page_size
        notifications = qs[offset:offset + page_size]
        return [self._to_entity(n) for n in notifications], total

    def mark_as_read(self, notification_id: UUID, user_id: UUID) -> bool:
        updated = Notification.objects.filter(
            id=notification_id, user_id=user_id,
        ).update(is_read=True)
        return updated > 0

    def mark_all_as_read(self, user_id: UUID) -> int:
        return Notification.objects.filter(
            user_id=user_id, is_read=False,
        ).update(is_read=True)
