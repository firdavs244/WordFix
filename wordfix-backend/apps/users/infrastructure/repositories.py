"""
User repository implementation using Django ORM.
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from uuid import UUID

from django.db.models import Sum
from django.db.models.functions import TruncDate

from apps.common.exceptions import EntityNotFoundError
from apps.users.domain.entities import UserEntity
from apps.users.domain.repositories import AbstractUserRepository
from apps.users.infrastructure.models import (
    Badge,
    CustomUser,
    Notification,
    UserBadge,
    UserProgress,
    XPTransaction,
)


class DjangoUserRepository(AbstractUserRepository):
    """Concrete implementation of AbstractUserRepository using Django ORM."""

    def _to_entity(self, user: CustomUser) -> UserEntity:
        """Convert Django model instance to domain entity."""
        return UserEntity(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            avatar=str(user.avatar) if user.avatar else "",
            native_language=user.native_language,
            learning_language=user.learning_language,
            proficiency_level=user.proficiency_level,
            daily_goal=user.daily_goal,
            timezone=user.timezone,
            is_premium=user.is_premium,
            premium_until=user.premium_until,
            is_active=user.is_active,
            is_staff=user.is_staff,
            date_joined=user.date_joined,
            last_login=user.last_login,
        )

    def get_by_id(self, user_id: UUID) -> UserEntity:
        try:
            user = CustomUser.objects.get(id=user_id)
            return self._to_entity(user)
        except CustomUser.DoesNotExist:
            raise EntityNotFoundError("User not found.")

    def get_by_email(self, email: str) -> UserEntity:
        try:
            user = CustomUser.objects.get(email=email.lower())
            return self._to_entity(user)
        except CustomUser.DoesNotExist:
            raise EntityNotFoundError("User not found.")

    def create(self, email: str, username: str, password: str, **kwargs) -> UserEntity:
        user = CustomUser.objects.create_user(
            email=email,
            username=username,
            password=password,
            **kwargs,
        )
        return self._to_entity(user)

    def update(self, user_id: UUID, **kwargs) -> UserEntity:
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise EntityNotFoundError("User not found.")

        for field, value in kwargs.items():
            setattr(user, field, value)
        user.save()
        return self._to_entity(user)

    def exists_by_email(self, email: str) -> bool:
        return CustomUser.objects.filter(email=email.lower()).exists()

    def exists_by_username(self, username: str) -> bool:
        return CustomUser.objects.filter(username=username).exists()

    def set_password(self, user_id: UUID, password: str) -> None:
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise EntityNotFoundError("User not found.")
        user.set_password(password)
        user.save(update_fields=["password"])

    def check_password(self, user_id: UUID, password: str) -> bool:
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise EntityNotFoundError("User not found.")
        return user.check_password(password)

    def get_user_language_info(self, user_id: UUID) -> dict:
        try:
            user = CustomUser.objects.get(id=user_id)
            return {
                "native_language": user.native_language,
                "proficiency_level": user.proficiency_level,
                "daily_goal": user.daily_goal,
            }
        except CustomUser.DoesNotExist:
            return {
                "native_language": "uz",
                "proficiency_level": "B1",
                "daily_goal": 10,
            }


# =============================================================================
# PROGRESS REPOSITORY
# =============================================================================

@dataclass
class ProgressEntity:
    id: UUID
    user_id: UUID
    total_xp: int
    level: int
    words_learned_total: int
    words_mastered_total: int
    tests_completed: int
    games_played: int
    reviews_completed: int
    perfect_scores: int
    total_study_time_seconds: int


class DjangoProgressRepository:
    """Repository for UserProgress."""

    def _to_entity(self, p: UserProgress) -> ProgressEntity:
        return ProgressEntity(
            id=p.id, user_id=p.user_id, total_xp=p.total_xp, level=p.level,
            words_learned_total=p.words_learned_total,
            words_mastered_total=p.words_mastered_total,
            tests_completed=p.tests_completed, games_played=p.games_played,
            reviews_completed=p.reviews_completed, perfect_scores=p.perfect_scores,
            total_study_time_seconds=p.total_study_time_seconds,
        )

    def get_or_create(self, user_id: UUID) -> ProgressEntity:
        p, _ = UserProgress.objects.get_or_create(user_id=user_id)
        return self._to_entity(p)

    def update(self, progress_id: UUID, **kwargs) -> ProgressEntity:
        UserProgress.objects.filter(id=progress_id).update(**kwargs)
        p = UserProgress.objects.get(id=progress_id)
        return self._to_entity(p)

    def increment(self, user_id: UUID, **kwargs):
        """Increment counters atomically."""
        from django.db.models import F
        p, _ = UserProgress.objects.get_or_create(user_id=user_id)
        updates = {k: F(k) + v for k, v in kwargs.items()}
        UserProgress.objects.filter(id=p.id).update(**updates)


# =============================================================================
# XP TRANSACTION REPOSITORY
# =============================================================================

@dataclass
class XPTransactionEntity:
    id: UUID
    user_id: UUID
    amount: int
    reason: str
    description: str
    created_at: datetime


class DjangoXPTransactionRepository:
    """Repository for XPTransaction."""

    def create(self, user_id: UUID, amount: int, reason: str,
               description: str = "") -> XPTransactionEntity:
        t = XPTransaction.objects.create(
            user_id=user_id, amount=amount, reason=reason, description=description,
        )
        return XPTransactionEntity(
            id=t.id, user_id=t.user_id, amount=t.amount,
            reason=t.reason, description=t.description, created_at=t.created_at,
        )

    def get_daily_totals(self, user_id: UUID, days: int = 7) -> list:
        """Get daily XP totals for the last N days."""
        since = datetime.now(timezone.utc) - timedelta(days=days)
        qs = (
            XPTransaction.objects.filter(user_id=user_id, created_at__gte=since)
            .annotate(date=TruncDate("created_at"))
            .values("date")
            .annotate(total_xp=Sum("amount"))
            .order_by("date")
        )
        # Fill missing days with 0
        result = {}
        for i in range(days):
            d = (datetime.now(timezone.utc) - timedelta(days=days - 1 - i)).date()
            result[str(d)] = 0
        for row in qs:
            result[str(row["date"])] = row["total_xp"]
        return [{"date": k, "xp": v} for k, v in result.items()]


# =============================================================================
# BADGE REPOSITORY
# =============================================================================

@dataclass
class BadgeEntity:
    id: UUID
    code: str
    name: str
    description: str
    icon: str
    category: str
    xp_reward: int
    rarity: str


class DjangoBadgeRepository:
    """Repository for Badge."""

    def _to_entity(self, b: Badge) -> BadgeEntity:
        return BadgeEntity(
            id=b.id, code=b.code, name=b.name, description=b.description,
            icon=b.icon, category=b.category, xp_reward=b.xp_reward, rarity=b.rarity,
        )

    def get_all(self) -> list[BadgeEntity]:
        return [self._to_entity(b) for b in Badge.objects.all()]

    def get_by_code(self, code: str) -> BadgeEntity | None:
        try:
            return self._to_entity(Badge.objects.get(code=code))
        except Badge.DoesNotExist:
            return None


# =============================================================================
# USER BADGE REPOSITORY
# =============================================================================

@dataclass
class UserBadgeEntity:
    id: UUID
    user_id: UUID
    badge_id: UUID
    badge_code: str
    badge_name: str
    badge_icon: str
    badge_category: str
    badge_rarity: str
    badge_description: str
    badge_xp_reward: int
    earned_at: datetime


class DjangoUserBadgeRepository:
    """Repository for UserBadge."""

    def create(self, user_id: UUID, badge_id: UUID) -> UserBadgeEntity:
        ub, created = UserBadge.objects.get_or_create(user_id=user_id, badge_id=badge_id)
        return self._to_entity(ub)

    def _to_entity(self, ub: UserBadge) -> UserBadgeEntity:
        return UserBadgeEntity(
            id=ub.id, user_id=ub.user_id, badge_id=ub.badge_id,
            badge_code=ub.badge.code, badge_name=ub.badge.name,
            badge_icon=ub.badge.icon, badge_category=ub.badge.category,
            badge_rarity=ub.badge.rarity, badge_description=ub.badge.description,
            badge_xp_reward=ub.badge.xp_reward, earned_at=ub.earned_at,
        )

    def get_by_user(self, user_id: UUID) -> list[UserBadgeEntity]:
        ubs = UserBadge.objects.filter(user_id=user_id).select_related("badge")
        return [self._to_entity(ub) for ub in ubs]

    def get_earned_codes(self, user_id: UUID) -> list[str]:
        return list(
            UserBadge.objects.filter(user_id=user_id)
            .select_related("badge")
            .values_list("badge__code", flat=True)
        )


# =============================================================================
# NOTIFICATION REPOSITORY
# =============================================================================

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
