"""
Tests for XP and Level domain services.
"""

import pytest

from apps.users.domain.services import (
    LEVEL_THRESHOLDS,
    XP_REWARDS,
    XPService,
    get_level_for_xp,
    get_xp_for_level,
    get_xp_for_next_level,
)
from apps.users.infrastructure.models import UserProgress, XPTransaction
from apps.users.infrastructure.repositories import (
    DjangoProgressRepository,
    DjangoXPTransactionRepository,
    DjangoNotificationRepository,
)
from apps.users.domain.services import NotificationService


# =============================================================================
# PURE FUNCTION TESTS (no DB)
# =============================================================================


class TestGetLevelForXP:
    def test_zero_xp_is_level_1(self):
        assert get_level_for_xp(0) == 1

    def test_exact_threshold_values(self):
        assert get_level_for_xp(100) == 2
        assert get_level_for_xp(250) == 3
        assert get_level_for_xp(500) == 4
        assert get_level_for_xp(7500) == 10

    def test_between_thresholds(self):
        assert get_level_for_xp(50) == 1
        assert get_level_for_xp(199) == 2
        assert get_level_for_xp(999) == 4

    def test_beyond_level_10(self):
        assert get_level_for_xp(10000) == 11
        assert get_level_for_xp(12500) == 12

    def test_negative_xp_returns_level_1(self):
        assert get_level_for_xp(-10) == 1


class TestGetXPForLevel:
    def test_level_1(self):
        assert get_xp_for_level(1) == 0

    def test_level_10(self):
        assert get_xp_for_level(10) == 7500

    def test_level_beyond_10(self):
        assert get_xp_for_level(11) == 10000
        assert get_xp_for_level(12) == 12500

    def test_level_zero_or_negative(self):
        assert get_xp_for_level(0) == 0
        assert get_xp_for_level(-1) == 0


class TestGetXPForNextLevel:
    def test_returns_dict_with_required_keys(self):
        result = get_xp_for_next_level(0)
        assert "current_level" in result
        assert "next_level" in result
        assert "xp_needed" in result
        assert "xp_progress" in result
        assert "progress_percentage" in result

    def test_zero_xp(self):
        result = get_xp_for_next_level(0)
        assert result["current_level"] == 1
        assert result["next_level"] == 2
        assert result["xp_progress"] == 0

    def test_mid_level(self):
        result = get_xp_for_next_level(150)
        assert result["current_level"] == 2
        assert result["xp_progress"] == 50  # 150 - 100

    def test_progress_percentage(self):
        result = get_xp_for_next_level(175)
        assert result["current_level"] == 2
        # 175 - 100 = 75 progress, 250 - 100 = 150 needed => 50%
        assert result["progress_percentage"] == 50.0


# =============================================================================
# XP SERVICE INTEGRATION TESTS (with DB)
# =============================================================================


@pytest.mark.django_db
class TestXPService:
    @pytest.fixture
    def xp_service(self):
        return XPService(
            progress_repo=DjangoProgressRepository(),
            xp_transaction_repo=DjangoXPTransactionRepository(),
            notification_service=NotificationService(
                notification_repo=DjangoNotificationRepository(),
            ),
        )

    def test_award_xp_creates_transaction(self, user, xp_service):
        xp_service.award_xp(user.id, 50, "word_added", "Added a word")
        assert XPTransaction.objects.filter(user=user).count() == 1
        t = XPTransaction.objects.get(user=user)
        assert t.amount == 50
        assert t.reason == "word_added"

    def test_award_xp_updates_progress(self, user, xp_service):
        result = xp_service.award_xp(user.id, 50, "word_added")
        assert result["new_total"] == 50
        assert result["xp_gained"] == 50
        progress = UserProgress.objects.get(user=user)
        assert progress.total_xp == 50

    def test_award_xp_accumulates(self, user, xp_service):
        xp_service.award_xp(user.id, 50, "word_added")
        result = xp_service.award_xp(user.id, 60, "review_correct")
        assert result["new_total"] == 110
        assert result["new_level"] == 2

    def test_level_up_detection(self, user, xp_service):
        result = xp_service.award_xp(user.id, 100, "test_complete")
        assert result["level_up"] is True
        assert result["new_level"] == 2

    def test_level_up_creates_notification(self, user, xp_service):
        from apps.users.infrastructure.models import Notification
        xp_service.award_xp(user.id, 100, "test_complete")
        notifs = Notification.objects.filter(user=user, type="level_up")
        assert notifs.count() == 1
        assert "Level 2" in notifs.first().message

    def test_award_zero_xp_noop(self, user, xp_service):
        result = xp_service.award_xp(user.id, 0, "word_added")
        assert result["xp_gained"] == 0
        assert XPTransaction.objects.filter(user=user).count() == 0

    def test_get_level_info(self, user, xp_service):
        xp_service.award_xp(user.id, 150, "test_complete")
        info = xp_service.get_level_info(user.id)
        assert info["level"] == 2
        assert info["total_xp"] == 150

    def test_get_xp_history(self, user, xp_service):
        xp_service.award_xp(user.id, 50, "word_added")
        xp_service.award_xp(user.id, 30, "review_correct")
        history = xp_service.get_xp_history(user.id, days=7)
        assert len(history) == 7
        # Today's total should be 80
        today_entry = history[-1]
        assert today_entry["xp"] == 80


class TestXPRewards:
    """Test that XP reward constants are all positive integers."""

    def test_all_rewards_positive(self):
        for reason, amount in XP_REWARDS.items():
            assert amount > 0, f"{reason} has non-positive reward: {amount}"

    def test_review_correct_more_than_incorrect(self):
        assert XP_REWARDS["review_correct"] > XP_REWARDS["review_incorrect"]

    def test_perfect_more_than_regular(self):
        assert XP_REWARDS["test_perfect"] > XP_REWARDS["test_complete"]
        assert XP_REWARDS["review_perfect"] > XP_REWARDS["review_complete"]
