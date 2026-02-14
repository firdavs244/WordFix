"""
Integration tests for challenge repository operations.
Covers: get_or_create_today, update, get_by_date, get_consecutive_completed_days
"""

import uuid
from datetime import date, timedelta

import pytest

from apps.words.infrastructure.models import DailyChallenge
from apps.words.infrastructure.repositories.challenge_repo import (
    DjangoDailyChallengeRepository,
)


@pytest.fixture
def challenge_repo():
    return DjangoDailyChallengeRepository()


@pytest.mark.django_db
class TestDjangoDailyChallengeRepository:
    """Tests for DjangoDailyChallengeRepository."""

    def test_get_or_create_today_creates_new(self, user, challenge_repo):
        challenges_data = [
            {"type": "review_words", "target": 5, "current": 0, "completed": False}
        ]
        entity, created = challenge_repo.get_or_create_today(
            user_id=user.id, challenges=challenges_data
        )
        assert created is True
        assert entity.user_id == user.id
        assert entity.date == date.today()
        assert entity.challenges == challenges_data

    def test_get_or_create_today_returns_existing(self, user, challenge_repo):
        challenges_data = [
            {"type": "review_words", "target": 5, "current": 0, "completed": False}
        ]
        entity1, created1 = challenge_repo.get_or_create_today(
            user_id=user.id, challenges=challenges_data
        )
        entity2, created2 = challenge_repo.get_or_create_today(user_id=user.id)
        assert created1 is True
        assert created2 is False
        assert entity1.id == entity2.id

    def test_update_challenge(self, user, challenge_repo):
        entity, _ = challenge_repo.get_or_create_today(
            user_id=user.id,
            challenges=[{"type": "x", "target": 1, "current": 0, "completed": False}],
        )
        updated = challenge_repo.update(
            entity.id, all_completed=True, bonus_claimed=True
        )
        assert updated.all_completed is True
        assert updated.bonus_claimed is True

    def test_update_nonexistent_raises(self, challenge_repo):
        from apps.common.exceptions import EntityNotFoundError

        with pytest.raises(EntityNotFoundError):
            challenge_repo.update(uuid.uuid4(), all_completed=True)

    def test_get_by_date(self, user, challenge_repo):
        challenge_repo.get_or_create_today(
            user_id=user.id,
            challenges=[{"type": "x", "target": 1, "current": 0, "completed": False}],
        )
        entity = challenge_repo.get_by_date(user.id, date.today())
        assert entity is not None
        assert entity.date == date.today()

    def test_get_by_date_not_found(self, user, challenge_repo):
        result = challenge_repo.get_by_date(user.id, date(2020, 1, 1))
        assert result is None

    def test_get_consecutive_completed_days_zero(self, user, challenge_repo):
        count = challenge_repo.get_consecutive_completed_days(user.id)
        assert count == 0

    def test_get_consecutive_completed_days_multiple(self, user, challenge_repo):
        today = date.today()
        for i in range(3):
            d = today - timedelta(days=i)
            DailyChallenge.objects.create(
                user=user,
                date=d,
                all_completed=True,
                challenges=[{"type": "x"}],
            )
        count = challenge_repo.get_consecutive_completed_days(user.id)
        assert count == 3

    def test_get_consecutive_days_breaks_on_gap(self, user, challenge_repo):
        today = date.today()
        DailyChallenge.objects.create(
            user=user, date=today, all_completed=True, challenges=[{"type": "x"}]
        )
        # Skip yesterday, add day before
        DailyChallenge.objects.create(
            user=user,
            date=today - timedelta(days=2),
            all_completed=True,
            challenges=[{"type": "x"}],
        )
        count = challenge_repo.get_consecutive_completed_days(user.id)
        assert count == 1  # Only today counts, yesterday missing
