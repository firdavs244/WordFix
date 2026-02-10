"""
Notification service — creating and managing user notifications.
"""


class NotificationService:
    """Domain service for notifications."""

    def __init__(self, notification_repo):
        self.notification_repo = notification_repo

    def create_notification(self, user_id, notification_type: str, title: str,
                            message: str, data: dict | None = None):
        """Create a new notification."""
        return self.notification_repo.create(
            user_id=user_id,
            notification_type=notification_type,
            title=title,
            message=message,
            data=data or {},
        )

    def get_unread_count(self, user_id) -> int:
        return self.notification_repo.get_unread_count(user_id)

    def get_notifications(self, user_id, page: int = 1, page_size: int = 20):
        return self.notification_repo.get_by_user(user_id, page=page, page_size=page_size)

    def mark_as_read(self, notification_id, user_id):
        return self.notification_repo.mark_as_read(notification_id, user_id)

    def mark_all_as_read(self, user_id):
        return self.notification_repo.mark_all_as_read(user_id)
