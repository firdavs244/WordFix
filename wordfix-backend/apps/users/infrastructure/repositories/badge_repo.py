"""
Badge and UserBadge repository implementations using Django ORM.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from apps.users.infrastructure.models import Badge, UserBadge


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
