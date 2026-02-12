"""
Tests for Badge domain service.
"""

import pytest

from apps.users.domain.services import BADGE_DEFINITIONS, BadgeService
from apps.users.infrastructure.models import Badge, UserBadge, UserProgress
from apps.users.infrastructure.repositories import (
    DjangoBadgeRepository,
    DjangoNotificationRepository,
    DjangoProgressRepository,
    DjangoUserBadgeRepository,
    DjangoXPTransactionRepository,
)
from apps.users.domain.services import NotificationService, XPService


@pytest.fixture
def _create_badges(db):
    """Create all badge definitions in the DB."""
    for defn in BADGE_DEFINITIONS:
        Badge.objects.get_or_create(
            code=defn["code"],
            defaults={
                "name": defn["name"],
                "description": defn["description"],
                "icon": defn["icon"],
                "category": defn["category"],
                "xp_reward": defn["xp_reward"],
                "rarity": defn["rarity"],
            },
        )


@pytest.fixture
def badge_service(_create_badges):
    progress_repo = DjangoProgressRepository()
    return BadgeService(
        badge_repo=DjangoBadgeRepository(),
        user_badge_repo=DjangoUserBadgeRepository(),
        progress_repo=progress_repo,
        xp_service=XPService(
            progress_repo=progress_repo,
            xp_transaction_repo=DjangoXPTransactionRepository(),
        ),
        notification_service=NotificationService(
            notification_repo=DjangoNotificationRepository(),
        ),
    )


# =============================================================================
# BADGE DEFINITIONS TESTS
# =============================================================================


class TestBadgeDefinitions:
    def test_all_codes_unique(self):
        codes = [b["code"] for b in BADGE_DEFINITIONS]
        assert len(codes) == len(set(codes))

    def test_all_have_required_fields(self):
        required = {"code", "name", "description", "icon", "category", "xp_reward", "rarity"}
        for defn in BADGE_DEFINITIONS:
            assert required.issubset(defn.keys()), f"Badge {defn.get('code')} missing fields"

    def test_minimum_badge_count(self):
        assert len(BADGE_DEFINITIONS) >= 15


# =============================================================================
# BADGE SERVICE TESTS
# =============================================================================


@pytest.mark.django_db
class TestBadgeService:
    def test_first_word_badge(self, user, badge_service):
        # Manually set progress
        p, _ = UserProgress.objects.get_or_create(user=user)
        p.words_learned_total = 1
        p.save()

        new_badges = badge_service.check_and_award_badges(user.id)
        badge_codes = [b.code for b in new_badges]
        assert "first_word" in badge_codes

    def test_no_duplicate_badges(self, user, badge_service):
        p, _ = UserProgress.objects.get_or_create(user=user)
        p.words_learned_total = 1
        p.save()

        first = badge_service.check_and_award_badges(user.id)
        second = badge_service.check_and_award_badges(user.id)
        assert len(first) > 0
        assert len(second) == 0  # Already earned

    def test_streak_badge_requires_context(self, user, badge_service):
        p, _ = UserProgress.objects.get_or_create(user=user)
        p.save()

        # Without context, no streak badge
        new_badges = badge_service.check_and_award_badges(user.id)
        streak_codes = [b.code for b in new_badges if b.code.startswith("streak_")]
        assert len(streak_codes) == 0

        # With context
        new_badges = badge_service.check_and_award_badges(
            user.id, context={"current_streak": 7}
        )
        streak_codes = [b.code for b in new_badges if b.code.startswith("streak_")]
        assert "streak_7" in streak_codes
        assert "streak_3" in streak_codes

    def test_multiple_badges_at_once(self, user, badge_service):
        p, _ = UserProgress.objects.get_or_create(user=user)
        p.words_learned_total = 10
        p.reviews_completed = 1
        p.save()

        new_badges = badge_service.check_and_award_badges(user.id)
        codes = [b.code for b in new_badges]
        assert "first_word" in codes
        assert "word_10" in codes
        assert "review_first" in codes

    def test_badge_awards_xp(self, user, badge_service):
        from apps.users.infrastructure.models import XPTransaction
        p, _ = UserProgress.objects.get_or_create(user=user)
        p.words_learned_total = 1
        p.save()

        badge_service.check_and_award_badges(user.id)
        # Should have at least one badge_reward transaction
        assert XPTransaction.objects.filter(
            user=user, reason="badge_reward"
        ).exists()

    def test_badge_creates_notification(self, user, badge_service):
        from apps.users.infrastructure.models import Notification
        p, _ = UserProgress.objects.get_or_create(user=user)
        p.words_learned_total = 1
        p.save()

        badge_service.check_and_award_badges(user.id)
        assert Notification.objects.filter(
            user=user, type="badge_earned"
        ).exists()

    def test_perfect_review_badge(self, user, badge_service):
        p, _ = UserProgress.objects.get_or_create(user=user)
        p.save()

        new_badges = badge_service.check_and_award_badges(
            user.id, context={"perfect_review": True}
        )
        codes = [b.code for b in new_badges]
        assert "perfect_review" in codes

    def test_speed_demon_badge(self, user, badge_service):
        p, _ = UserProgress.objects.get_or_create(user=user)
        p.games_played = 1
        p.save()

        new_badges = badge_service.check_and_award_badges(
            user.id, context={"speed_round_correct": 20}
        )
        codes = [b.code for b in new_badges]
        assert "speed_demon" in codes
        assert "game_first" in codes

    def test_get_user_badges(self, user, badge_service):
        p, _ = UserProgress.objects.get_or_create(user=user)
        p.words_learned_total = 1
        p.save()
        badge_service.check_and_award_badges(user.id)

        earned = badge_service.get_user_badges(user.id)
        assert len(earned) >= 1
        assert earned[0].badge_code == "first_word"

    def test_get_available_badges(self, user, badge_service):
        badges = badge_service.get_available_badges(user.id)
        assert len(badges) == len(BADGE_DEFINITIONS)
        # All should be unearned
        assert all(not b["is_earned"] for b in badges)

        # Earn one
        p, _ = UserProgress.objects.get_or_create(user=user)
        p.words_learned_total = 1
        p.save()
        badge_service.check_and_award_badges(user.id)

        badges = badge_service.get_available_badges(user.id)
        earned = [b for b in badges if b["is_earned"]]
        assert len(earned) >= 1


# =============================================================================
# MANAGEMENT COMMAND TEST
# =============================================================================


@pytest.mark.django_db
class TestCreateBadgesCommand:
    def test_create_badges(self):
        from django.core.management import call_command
        call_command("create_badges")
        assert Badge.objects.count() == len(BADGE_DEFINITIONS)

    def test_idempotent(self):
        from django.core.management import call_command
        call_command("create_badges")
        call_command("create_badges")
        assert Badge.objects.count() == len(BADGE_DEFINITIONS)


# =============================================================================
# NEW GAME BADGE TESTS
# =============================================================================


@pytest.mark.django_db
class TestNewGameBadges:
    """Tests for Story Builder, Listening Challenge, and Game Variety badges."""

    def test_storyteller_badge(self, user, badge_service):
        """Storyteller badge awarded for 5+ story builder games."""
        p, _ = UserProgress.objects.get_or_create(user=user)
        p.save()

        new_badges = badge_service.check_and_award_badges(
            user.id, context={"story_builder_count": 5}
        )
        codes = [b.code for b in new_badges]
        assert "storyteller" in codes

    def test_story_master_badge(self, user, badge_service):
        """Story master badge awarded for 90+ score."""
        p, _ = UserProgress.objects.get_or_create(user=user)
        p.save()

        new_badges = badge_service.check_and_award_badges(
            user.id, context={"story_builder_score": 95}
        )
        codes = [b.code for b in new_badges]
        assert "story_master" in codes

    def test_sharp_ears_badge(self, user, badge_service):
        """Sharp ears badge for 10+ listening challenges."""
        p, _ = UserProgress.objects.get_or_create(user=user)
        p.save()

        new_badges = badge_service.check_and_award_badges(
            user.id, context={"listening_challenge_count": 10}
        )
        codes = [b.code for b in new_badges]
        assert "sharp_ears" in codes

    def test_perfect_hearing_badge(self, user, badge_service):
        """Perfect hearing badge for 100% listening accuracy."""
        p, _ = UserProgress.objects.get_or_create(user=user)
        p.save()

        new_badges = badge_service.check_and_award_badges(
            user.id, context={"listening_accuracy": 100}
        )
        codes = [b.code for b in new_badges]
        assert "perfect_hearing" in codes

    def test_five_games_badge(self, user, badge_service):
        """Five games badge for playing all 5 game types."""
        p, _ = UserProgress.objects.get_or_create(user=user)
        p.save()

        new_badges = badge_service.check_and_award_badges(
            user.id, context={"unique_game_types": 5}
        )
        codes = [b.code for b in new_badges]
        assert "five_games" in codes

    def test_new_badges_in_definitions(self):
        """All new badges are present in BADGE_DEFINITIONS."""
        codes = {b["code"] for b in BADGE_DEFINITIONS}
        assert "storyteller" in codes
        assert "story_master" in codes
        assert "sharp_ears" in codes
        assert "perfect_hearing" in codes
        assert "five_games" in codes
