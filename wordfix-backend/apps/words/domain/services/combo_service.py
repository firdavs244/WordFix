"""
Combo and daily challenge domain services.

CLEAN ARCHITECTURE: No Django imports. Uses stdlib only.
"""

import random


class ComboService:
    """Combo multiplier service for consecutive correct answers."""

    COMBO_THRESHOLDS = [
        (20, 5.0),
        (10, 3.0),
        (5, 2.0),
        (2, 1.5),
    ]

    @staticmethod
    def get_multiplier(combo_count: int) -> float:
        """Get XP multiplier based on current combo count."""
        for threshold, multiplier in ComboService.COMBO_THRESHOLDS:
            if combo_count >= threshold:
                return multiplier
        return 1.0

    @staticmethod
    def calculate_combo_xp(base_xp: int, combo_count: int) -> tuple[int, float]:
        """Calculate combo XP. Returns (final_xp, multiplier)."""
        multiplier = ComboService.get_multiplier(combo_count)
        return (int(base_xp * multiplier), multiplier)


class DailyChallengeService:
    """Domain service for generating and managing daily challenges."""

    CHALLENGE_TYPES_EASY = [
        {"type": "review_words", "target": 5, "xp_reward": 20,
         "title": "Review 5 words", "icon": "book"},
        {"type": "add_words", "target": 3, "xp_reward": 20,
         "title": "Add 3 new words", "icon": "plus"},
        {"type": "play_game", "target": 1, "xp_reward": 15,
         "title": "Play any game", "icon": "gamepad"},
        {"type": "complete_test", "target": 1, "xp_reward": 20,
         "title": "Complete a test", "icon": "clipboard"},
        {"type": "chat_practice", "target": 1, "xp_reward": 15,
         "title": "Practice in AI chat", "icon": "message-circle"},
        {"type": "write_story", "target": 1, "xp_reward": 20,
         "title": "Write a story", "icon": "pen-tool"},
        {"type": "listening", "target": 1, "xp_reward": 15,
         "title": "Complete listening challenge", "icon": "headphones"},
    ]

    CHALLENGE_TYPES_MEDIUM = [
        {"type": "review_words", "target": 10, "xp_reward": 30,
         "title": "Review 10 words", "icon": "book"},
        {"type": "add_words", "target": 5, "xp_reward": 30,
         "title": "Add 5 new words", "icon": "plus"},
        {"type": "perfect_review", "target": 1, "xp_reward": 30,
         "title": "Get a perfect review score", "icon": "star"},
        {"type": "play_game", "target": 2, "xp_reward": 25,
         "title": "Play 2 games", "icon": "gamepad"},
        {"type": "combo_streak", "target": 5, "xp_reward": 30,
         "title": "Reach 5x combo", "icon": "zap"},
        {"type": "complete_test", "target": 1, "xp_reward": 25,
         "title": "Complete a test", "icon": "clipboard"},
        {"type": "master_word", "target": 1, "xp_reward": 35,
         "title": "Master a word", "icon": "crown"},
        {"type": "write_story", "target": 1, "xp_reward": 30,
         "title": "Write a story", "icon": "pen-tool"},
        {"type": "listening", "target": 1, "xp_reward": 25,
         "title": "Complete listening challenge", "icon": "headphones"},
    ]

    CHALLENGE_TYPES_HARD = [
        {"type": "review_words", "target": 15, "xp_reward": 40,
         "title": "Review 15 words", "icon": "book"},
        {"type": "perfect_review", "target": 3, "xp_reward": 50,
         "title": "Get 3 perfect review scores", "icon": "star"},
        {"type": "play_game", "target": 2, "xp_reward": 30,
         "title": "Play 2 games", "icon": "gamepad"},
        {"type": "combo_streak", "target": 10, "xp_reward": 45,
         "title": "Reach 10x combo", "icon": "zap"},
        {"type": "complete_test", "target": 1, "xp_reward": 30,
         "title": "Complete a test", "icon": "clipboard"},
        {"type": "master_word", "target": 1, "xp_reward": 40,
         "title": "Master a word", "icon": "crown"},
        {"type": "add_words", "target": 5, "xp_reward": 35,
         "title": "Add 5 new words", "icon": "plus"},
        {"type": "write_story", "target": 1, "xp_reward": 40,
         "title": "Write a story", "icon": "pen-tool"},
        {"type": "listening", "target": 2, "xp_reward": 35,
         "title": "Complete 2 listening challenges", "icon": "headphones"},
    ]

    @staticmethod
    def generate_daily_challenges(user_level: int, existing_word_count: int) -> list[dict]:
        """
        Generate 3 daily challenges based on user level.
        If word count < 5, add_words is mandatory.
        """
        if user_level <= 3:
            pool = [dict(c) for c in DailyChallengeService.CHALLENGE_TYPES_EASY]
        elif user_level <= 7:
            pool = [dict(c) for c in DailyChallengeService.CHALLENGE_TYPES_MEDIUM]
        else:
            pool = [dict(c) for c in DailyChallengeService.CHALLENGE_TYPES_HARD]

        challenges = []

        # If not enough words, force add_words challenge
        if existing_word_count < 5:
            add_challenge = None
            for c in pool:
                if c["type"] == "add_words":
                    add_challenge = dict(c)
                    break
            if not add_challenge:
                add_challenge = {"type": "add_words", "target": 3, "xp_reward": 20,
                                 "title": "Add 3 new words", "icon": "plus"}
            add_challenge["current"] = 0
            add_challenge["completed"] = False
            challenges.append(add_challenge)
            pool = [c for c in pool if c["type"] != "add_words"]

        # Ensure no duplicate types
        used_types = {c["type"] for c in challenges}
        remaining_pool = [c for c in pool if c["type"] not in used_types]

        needed = 3 - len(challenges)
        if len(remaining_pool) < needed:
            remaining_pool = pool

        selected = random.sample(remaining_pool, min(needed, len(remaining_pool)))
        for c in selected:
            challenge = dict(c)
            challenge["current"] = 0
            challenge["completed"] = False
            challenges.append(challenge)

        return challenges[:3]
