"""
DailyChallenge repository implementation using Django ORM.
"""

from datetime import date
from uuid import UUID

from apps.common.exceptions import EntityNotFoundError
from apps.words.domain.entities import DailyChallengeEntity
from apps.words.domain.repositories import AbstractDailyChallengeRepository
from apps.words.infrastructure.models import DailyChallenge


class DjangoDailyChallengeRepository(AbstractDailyChallengeRepository):
    """Concrete implementation of AbstractDailyChallengeRepository."""

    def _to_entity(self, challenge: DailyChallenge) -> DailyChallengeEntity:
        return DailyChallengeEntity(
            id=challenge.id,
            user_id=challenge.user_id,
            date=challenge.date,
            challenges=challenge.challenges,
            all_completed=challenge.all_completed,
            bonus_claimed=challenge.bonus_claimed,
            is_active=challenge.is_active,
            created_at=challenge.created_at,
            updated_at=challenge.updated_at,
        )

    def get_or_create_today(self, user_id: UUID, challenges: list | None = None) -> tuple[DailyChallengeEntity, bool]:
        today = date.today()
        defaults = {}
        if challenges is not None:
            defaults["challenges"] = challenges

        challenge, created = DailyChallenge.objects.get_or_create(
            user_id=user_id,
            date=today,
            defaults=defaults,
        )
        return self._to_entity(challenge), created

    def update(self, challenge_id: UUID, **kwargs) -> DailyChallengeEntity:
        try:
            challenge = DailyChallenge.objects.get(id=challenge_id)
        except DailyChallenge.DoesNotExist:
            raise EntityNotFoundError("Daily challenge not found.")
        for field, value in kwargs.items():
            setattr(challenge, field, value)
        challenge.save()
        return self._to_entity(challenge)

    def get_by_date(self, user_id: UUID, target_date) -> DailyChallengeEntity | None:
        try:
            challenge = DailyChallenge.objects.get(user_id=user_id, date=target_date)
            return self._to_entity(challenge)
        except DailyChallenge.DoesNotExist:
            return None

    def get_consecutive_completed_days(self, user_id: UUID) -> int:
        """Count consecutive days where all_completed=True ending today."""
        from datetime import timedelta

        today = date.today()
        count = 0
        current_date = today

        while True:
            try:
                challenge = DailyChallenge.objects.get(
                    user_id=user_id,
                    date=current_date,
                    all_completed=True,
                )
                count += 1
                current_date -= timedelta(days=1)
            except DailyChallenge.DoesNotExist:
                break

        return count
