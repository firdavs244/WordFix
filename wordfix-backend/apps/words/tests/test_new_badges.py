"""
Tests for new badges: combo badges and daily champion badges.
"""

import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from apps.users.domain.services.badge_service import BadgeService, BADGE_DEFINITIONS


class TestNewBadgeDefinitions:
    """Test that new badge definitions exist."""

    def test_combo_badges_defined(self):
        codes = {b["code"] for b in BADGE_DEFINITIONS}
        assert "combo_5" in codes
        assert "combo_10" in codes
        assert "combo_20" in codes
        assert "combo_50" in codes

    def test_daily_champion_badges_defined(self):
        codes = {b["code"] for b in BADGE_DEFINITIONS}
        assert "daily_champion_7" in codes
        assert "daily_champion_30" in codes

    def test_combo_badge_details(self):
        combo_5 = next(b for b in BADGE_DEFINITIONS if b["code"] == "combo_5")
        assert combo_5["category"] == "combo"
        assert combo_5["xp_reward"] > 0

    def test_daily_champion_badge_details(self):
        dc7 = next(b for b in BADGE_DEFINITIONS if b["code"] == "daily_champion_7")
        assert dc7["category"] == "challenge"
        assert dc7["xp_reward"] > 0


class TestComboBadgeAwarding:
    """Test that combo badges are awarded correctly."""

    def _make_service(self):
        badge_repo = MagicMock()
        badge_repo.get_by_code.return_value = MagicMock(
            id=uuid4(), code="combo_5", name="Combo Starter",
            icon="zap", rarity="common", xp_reward=15,
        )

        user_badge_repo = MagicMock()
        user_badge_repo.get_earned_codes.return_value = []

        progress = MagicMock()
        progress.words_learned_total = 0
        progress.reviews_completed = 0
        progress.tests_completed = 0
        progress.games_played = 0
        progress.level = 1
        progress.words_mastered_total = 0

        progress_repo = MagicMock()
        progress_repo.get_or_create.return_value = progress

        return BadgeService(badge_repo, user_badge_repo, progress_repo)

    def test_awards_combo_5_badge(self):
        service = self._make_service()
        new = service.check_and_award_badges(
            uuid4(), context={"max_combo": 5}
        )
        assert any(b.code == "combo_5" for b in new)

    def test_does_not_award_if_already_earned(self):
        service = self._make_service()
        service.user_badge_repo.get_earned_codes.return_value = ["combo_5"]
        new = service.check_and_award_badges(
            uuid4(), context={"max_combo": 5}
        )
        assert not any(getattr(b, 'code', None) == "combo_5" for b in new)

    def test_awards_daily_champion_badge(self):
        service = self._make_service()
        service.badge_repo.get_by_code.return_value = MagicMock(
            id=uuid4(), code="daily_champion_7", name="Weekly Challenger",
            icon="calendar-check", rarity="rare", xp_reward=75,
        )
        new = service.check_and_award_badges(
            uuid4(), context={"consecutive_challenge_days": 7}
        )
        awarded_codes = [b.code for b in new]
        assert "daily_champion_7" in awarded_codes
