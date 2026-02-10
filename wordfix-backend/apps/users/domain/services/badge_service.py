"""
Badge service — badge definitions and awarding logic.
"""

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
    # Combo badges
    {"code": "combo_5", "name": "Combo Starter", "description": "Reach a 5x combo streak",
     "icon": "zap", "category": "combo", "xp_reward": 15, "rarity": "common"},
    {"code": "combo_10", "name": "Combo King", "description": "Reach a 10x combo streak",
     "icon": "zap", "category": "combo", "xp_reward": 30, "rarity": "rare"},
    {"code": "combo_20", "name": "Combo Master", "description": "Reach a 20x combo streak",
     "icon": "zap", "category": "combo", "xp_reward": 75, "rarity": "epic"},
    {"code": "combo_50", "name": "Unstoppable Combo", "description": "Reach a 50x combo streak",
     "icon": "zap", "category": "combo", "xp_reward": 200, "rarity": "legendary"},
    # Daily challenge badges
    {"code": "daily_champion_7", "name": "Weekly Challenger", "description": "Complete all daily challenges 7 days in a row",
     "icon": "calendar-check", "category": "challenge", "xp_reward": 75, "rarity": "rare"},
    {"code": "daily_champion_30", "name": "Monthly Challenger", "description": "Complete all daily challenges 30 days in a row",
     "icon": "calendar-check", "category": "challenge", "xp_reward": 300, "rarity": "legendary"},
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
            # Combo badges
            "combo_5": context.get("max_combo", 0) >= 5,
            "combo_10": context.get("max_combo", 0) >= 10,
            "combo_20": context.get("max_combo", 0) >= 20,
            "combo_50": context.get("max_combo", 0) >= 50,
            # Daily challenge badges
            "daily_champion_7": context.get("consecutive_challenge_days", 0) >= 7,
            "daily_champion_30": context.get("consecutive_challenge_days", 0) >= 30,
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
