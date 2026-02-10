"""
XP service — level thresholds, XP rewards, and XP/level domain logic.
"""

import logging

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
    "combo_bonus": 0,  # Dynamic, computed by ComboService
    "daily_challenge": 0,  # Dynamic, computed per challenge
    "daily_all_complete": 50,
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
