"""
Dependency injection for progress, badges, and notifications.
"""

from apps.users.domain.services import BadgeService, NotificationService, XPService
from apps.users.infrastructure.repositories import (
    DjangoBadgeRepository,
    DjangoNotificationRepository,
    DjangoProgressRepository,
    DjangoUserBadgeRepository,
    DjangoXPTransactionRepository,
)


def get_progress_repository() -> DjangoProgressRepository:
    return DjangoProgressRepository()


def get_xp_transaction_repository() -> DjangoXPTransactionRepository:
    return DjangoXPTransactionRepository()


def get_badge_repository() -> DjangoBadgeRepository:
    return DjangoBadgeRepository()


def get_user_badge_repository() -> DjangoUserBadgeRepository:
    return DjangoUserBadgeRepository()


def get_notification_repository() -> DjangoNotificationRepository:
    return DjangoNotificationRepository()


def get_notification_service() -> NotificationService:
    return NotificationService(
        notification_repo=get_notification_repository(),
    )


def get_xp_service() -> XPService:
    return XPService(
        progress_repo=get_progress_repository(),
        xp_transaction_repo=get_xp_transaction_repository(),
        notification_service=get_notification_service(),
    )


def get_badge_service() -> BadgeService:
    return BadgeService(
        badge_repo=get_badge_repository(),
        user_badge_repo=get_user_badge_repository(),
        progress_repo=get_progress_repository(),
        xp_service=get_xp_service(),
        notification_service=get_notification_service(),
    )
