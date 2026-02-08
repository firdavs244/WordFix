"""
User domain services.

Business logic that doesn't naturally belong to a single entity.
"""

import logging
from datetime import date, timedelta

logger = logging.getLogger(__name__)

# =============================================================================
# LEVEL THRESHOLDS
# =============================================================================

LEVEL_THRESHOLDS = [
    0,      # Level 1
    100,    # Level 2
    250,    # Level 3
    500,    # Level 4
    1000,   # Level 5
    1750,   # Level 6
    2750,   # Level 7
    4000,   # Level 8
    5500,   # Level 9
    7500,   # Level 10
]


def get_level_for_xp(xp: int) -> int:
    """Calculate level from total XP."""
    for i in range(len(LEVEL_THRESHOLDS) - 1, -1, -1):
        if xp >= LEVEL_THRESHOLDS[i]:
            level = i + 1
            # Beyond level 10, each 2500 XP adds a level
            if level == 10:
                extra = (xp - LEVEL_THRESHOLDS[9]) // 2500
                level += extra
            return level
    return 1


def get_xp_for_level(level: int) -> int:
    """Get the XP threshold for a given level."""
    if level <= 0:
        return 0
    if level <= len(LEVEL_THRESHOLDS):
        return LEVEL_THRESHOLDS[level - 1]
    # Level 11+: 7500 + (level - 10) * 2500
    return LEVEL_THRESHOLDS[9] + (level - 10) * 2500


def get_xp_for_next_level(current_xp: int) -> dict:
    """Get detailed level progress information."""
    current_level = get_level_for_xp(current_xp)
    next_level = current_level + 1
    current_threshold = get_xp_for_level(current_level)
    next_threshold = get_xp_for_level(next_level)
    xp_in_level = current_xp - current_threshold
    xp_needed = next_threshold - current_threshold
    progress_pct = round((xp_in_level / xp_needed * 100) if xp_needed > 0 else 100, 1)

    return {
        "current_level": current_level,
        "next_level": next_level,
        "xp_needed": xp_needed,
        "xp_progress": xp_in_level,
        "progress_percentage": min(progress_pct, 100.0),
        "current_threshold": current_threshold,
        "next_threshold": next_threshold,
    }


# =============================================================================
# XP AWARD AMOUNTS
# =============================================================================

XP_REWARDS = {
    "word_added": 5,
    "review_correct": 10,
    "review_incorrect": 3,
    "review_complete": 20,
    "review_perfect": 30,
    "test_complete": 25,
    "test_good": 15,
    "test_perfect": 40,
    "game_complete": 15,
    "game_good": 10,
    "word_mastered": 25,
    "streak_7": 50,
    "streak_30": 200,
    "daily_goal": 20,
}

XP_DESCRIPTIONS = {
    "word_added": "Added a new word",
    "review_correct": "Correct review answer",
    "review_incorrect": "Review attempt",
    "review_complete": "Completed review session",
    "review_perfect": "Perfect review session",
    "test_complete": "Completed a test",
    "test_good": "Good test score (80%+)",
    "test_perfect": "Perfect test score",
    "game_complete": "Completed a game",
    "game_good": "Good game score (80%+)",
    "word_mastered": "Mastered a word",
    "streak_7": "7-day streak milestone",
    "streak_30": "30-day streak milestone",
    "daily_goal": "Daily goal completed",
    "badge_reward": "Badge earned",
    "level_up": "Level up bonus",
}


class UserDomainService:
    """
    Domain service for user-related business logic.
    """

    @staticmethod
    def can_user_access_premium_features(user) -> bool:
        return user.is_active


class XPService:
    """Domain service for XP and level calculations."""

    def __init__(self, progress_repo, xp_transaction_repo, notification_service=None):
        self.progress_repo = progress_repo
        self.xp_transaction_repo = xp_transaction_repo
        self.notification_service = notification_service

    def award_xp(self, user_id, amount: int, reason: str, description: str = "") -> dict:
        """Award XP to a user and handle level ups."""
        if amount <= 0:
            return {"new_total": 0, "level_up": False, "new_level": 1, "xp_gained": 0}

        progress = self.progress_repo.get_or_create(user_id)
        old_level = progress.level

        # Create transaction
        desc = description or XP_DESCRIPTIONS.get(reason, reason)
        self.xp_transaction_repo.create(
            user_id=user_id, amount=amount, reason=reason, description=desc,
        )

        # Update total XP
        new_total = progress.total_xp + amount
        new_level = get_level_for_xp(new_total)

        self.progress_repo.update(
            progress_id=progress.id,
            total_xp=new_total,
            level=new_level,
        )

        level_up = new_level > old_level

        if level_up and self.notification_service:
            self.notification_service.create_notification(
                user_id=user_id,
                notification_type="level_up",
                title="Level Up! 🎉",
                message=f"Congratulations! You reached Level {new_level}!",
                data={"level": new_level, "total_xp": new_total},
            )

        return {
            "new_total": new_total,
            "level_up": level_up,
            "new_level": new_level,
            "xp_gained": amount,
        }

    def get_level_info(self, user_id) -> dict:
        """Get level progress info for a user."""
        progress = self.progress_repo.get_or_create(user_id)
        level_info = get_xp_for_next_level(progress.total_xp)
        return {
            "level": progress.level,
            "total_xp": progress.total_xp,
            "xp_for_current": level_info["current_threshold"],
            "xp_for_next": level_info["next_threshold"],
            "progress_pct": level_info["progress_percentage"],
            "xp_progress": level_info["xp_progress"],
            "xp_needed": level_info["xp_needed"],
            "words_learned_total": progress.words_learned_total,
            "words_mastered_total": progress.words_mastered_total,
            "tests_completed": progress.tests_completed,
            "games_played": progress.games_played,
            "reviews_completed": progress.reviews_completed,
            "perfect_scores": progress.perfect_scores,
            "total_study_time_seconds": progress.total_study_time_seconds,
        }

    def get_xp_history(self, user_id, days: int = 7) -> list:
        """Get daily XP totals for the last N days."""
        return self.xp_transaction_repo.get_daily_totals(user_id, days=days)


# =============================================================================
# BADGE DEFINITIONS
# =============================================================================

BADGE_DEFINITIONS = [
    {"code": "first_word", "name": "First Word", "description": "Add your first word",
     "icon": "book-open", "category": "words", "xp_reward": 10, "rarity": "common"},
    {"code": "word_10", "name": "Word Collector", "description": "Add 10 words",
     "icon": "library", "category": "words", "xp_reward": 20, "rarity": "common"},
    {"code": "word_50", "name": "Vocabulary Builder", "description": "Add 50 words",
     "icon": "book-marked", "category": "words", "xp_reward": 50, "rarity": "rare"},
    {"code": "word_100", "name": "Word Master", "description": "Add 100 words",
     "icon": "crown", "category": "words", "xp_reward": 100, "rarity": "epic"},
    {"code": "streak_3", "name": "Getting Started", "description": "Maintain a 3-day streak",
     "icon": "flame", "category": "streak", "xp_reward": 15, "rarity": "common"},
    {"code": "streak_7", "name": "Week Warrior", "description": "Maintain a 7-day streak",
     "icon": "flame", "category": "streak", "xp_reward": 30, "rarity": "rare"},
    {"code": "streak_30", "name": "Monthly Champion", "description": "Maintain a 30-day streak",
     "icon": "flame", "category": "streak", "xp_reward": 100, "rarity": "epic"},
    {"code": "streak_100", "name": "Unstoppable", "description": "Maintain a 100-day streak",
     "icon": "flame", "category": "streak", "xp_reward": 300, "rarity": "legendary"},
    {"code": "review_first", "name": "First Review", "description": "Complete your first review",
     "icon": "brain", "category": "review", "xp_reward": 10, "rarity": "common"},
    {"code": "review_50", "name": "Review Pro", "description": "Complete 50 reviews",
     "icon": "brain", "category": "review", "xp_reward": 50, "rarity": "rare"},
    {"code": "test_first", "name": "Test Taker", "description": "Complete your first test",
     "icon": "clipboard-check", "category": "test", "xp_reward": 10, "rarity": "common"},
    {"code": "test_10", "name": "Test Expert", "description": "Complete 10 tests",
     "icon": "clipboard-check", "category": "test", "xp_reward": 50, "rarity": "rare"},
    {"code": "game_first", "name": "First Game", "description": "Play your first game",
     "icon": "gamepad-2", "category": "game", "xp_reward": 10, "rarity": "common"},
    {"code": "speed_demon", "name": "Speed Demon", "description": "Get 20+ correct in Speed Round",
     "icon": "zap", "category": "game", "xp_reward": 50, "rarity": "epic"},
    {"code": "perfect_review", "name": "Perfect Review", "description": "Get 100% in a review session",
     "icon": "star", "category": "review", "xp_reward": 30, "rarity": "rare"},
    {"code": "perfect_test", "name": "Perfect Test", "description": "Get 100% in a test",
     "icon": "star", "category": "test", "xp_reward": 50, "rarity": "epic"},
    {"code": "level_5", "name": "Rising Star", "description": "Reach Level 5",
     "icon": "trending-up", "category": "level", "xp_reward": 50, "rarity": "rare"},
    {"code": "level_10", "name": "Veteran", "description": "Reach Level 10",
     "icon": "award", "category": "level", "xp_reward": 200, "rarity": "legendary"},
    {"code": "mastered_10", "name": "Word Scholar", "description": "Master 10 words",
     "icon": "graduation-cap", "category": "mastery", "xp_reward": 50, "rarity": "rare"},
    {"code": "mastered_50", "name": "Word Sage", "description": "Master 50 words",
     "icon": "graduation-cap", "category": "mastery", "xp_reward": 200, "rarity": "legendary"},
]


class BadgeService:
    """Domain service for badge checking and awarding."""

    def __init__(self, badge_repo, user_badge_repo, progress_repo, xp_service=None,
                 notification_service=None):
        self.badge_repo = badge_repo
        self.user_badge_repo = user_badge_repo
        self.progress_repo = progress_repo
        self.xp_service = xp_service
        self.notification_service = notification_service

    def check_and_award_badges(self, user_id, context: dict | None = None) -> list:
        """Check all badge conditions and award new ones."""
        context = context or {}
        progress = self.progress_repo.get_or_create(user_id)
        earned_codes = set(self.user_badge_repo.get_earned_codes(user_id))
        new_badges = []

        # Badge condition checks
        checks = {
            "first_word": progress.words_learned_total >= 1,
            "word_10": progress.words_learned_total >= 10,
            "word_50": progress.words_learned_total >= 50,
            "word_100": progress.words_learned_total >= 100,
            "streak_3": context.get("current_streak", 0) >= 3,
            "streak_7": context.get("current_streak", 0) >= 7,
            "streak_30": context.get("current_streak", 0) >= 30,
            "streak_100": context.get("current_streak", 0) >= 100,
            "review_first": progress.reviews_completed >= 1,
            "review_50": progress.reviews_completed >= 50,
            "test_first": progress.tests_completed >= 1,
            "test_10": progress.tests_completed >= 10,
            "game_first": progress.games_played >= 1,
            "speed_demon": context.get("speed_round_correct", 0) >= 20,
            "perfect_review": context.get("perfect_review", False),
            "perfect_test": context.get("perfect_test", False),
            "level_5": progress.level >= 5,
            "level_10": progress.level >= 10,
            "mastered_10": progress.words_mastered_total >= 10,
            "mastered_50": progress.words_mastered_total >= 50,
        }

        for code, condition in checks.items():
            if condition and code not in earned_codes:
                badge = self.badge_repo.get_by_code(code)
                if badge:
                    self.user_badge_repo.create(user_id=user_id, badge_id=badge.id)
                    new_badges.append(badge)

                    # Award XP for badge
                    if self.xp_service and badge.xp_reward > 0:
                        self.xp_service.award_xp(
                            user_id, badge.xp_reward, "badge_reward",
                            f"Badge earned: {badge.name}",
                        )

                    # Notification
                    if self.notification_service:
                        self.notification_service.create_notification(
                            user_id=user_id,
                            notification_type="badge_earned",
                            title=f"🏆 New Badge: {badge.name}!",
                            message=badge.description,
                            data={"badge_code": badge.code, "badge_name": badge.name,
                                  "badge_icon": badge.icon, "badge_rarity": badge.rarity},
                        )

        return new_badges

    def get_user_badges(self, user_id) -> list:
        """Get all badges earned by a user."""
        return self.user_badge_repo.get_by_user(user_id)

    def get_available_badges(self, user_id) -> list:
        """Get all badges with earned status for a user."""
        all_badges = self.badge_repo.get_all()
        earned_codes = set(self.user_badge_repo.get_earned_codes(user_id))
        earned_map = {ub.badge_code: ub.earned_at for ub in self.user_badge_repo.get_by_user(user_id)}

        result = []
        for badge in all_badges:
            is_earned = badge.code in earned_codes
            result.append({
                "id": str(badge.id),
                "code": badge.code,
                "name": badge.name,
                "description": badge.description,
                "icon": badge.icon,
                "category": badge.category,
                "xp_reward": badge.xp_reward,
                "rarity": badge.rarity,
                "is_earned": is_earned,
                "earned_at": str(earned_map.get(badge.code, "")) if is_earned else None,
            })
        return result


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
