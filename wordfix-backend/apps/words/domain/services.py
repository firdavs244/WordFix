"""
Word domain services.

Business logic that doesn't naturally belong to a single entity.
Includes SM-2 spaced repetition and word enrichment domain logic.

CLEAN ARCHITECTURE: No Django imports. Uses stdlib only.
"""

import random
from datetime import datetime, timedelta, timezone


class WordDomainService:
    """Legacy domain service for word-related business logic."""

    @staticmethod
    def calculate_next_review_interval(times_correct: int, times_reviewed: int) -> int:
        if times_reviewed == 0:
            return 1
        accuracy = times_correct / times_reviewed
        if accuracy >= 0.9:
            return min(720, 24 * (2 ** min(times_correct, 8)))
        elif accuracy >= 0.7:
            return min(168, 12 * (2 ** min(times_correct, 5)))
        elif accuracy >= 0.5:
            return 4
        else:
            return 1


class SpacedRepetitionService:
    """
    SM-2 Spaced Repetition algorithm implementation.

    Quality scale: 0-5
        0 = Complete blackout
        1 = Incorrect, but remembered upon seeing answer
        2 = Incorrect, but answer seemed easy to recall
        3 = Correct with serious difficulty
        4 = Correct with some hesitation
        5 = Perfect response
    """

    def calculate_next_review(self, word_entity, quality: int, now: datetime | None = None):
        """
        Apply SM-2 algorithm to update word's spaced repetition parameters.

        Args:
            word_entity: WordEntity to update (mutated in place)
            quality: 0-5 quality rating
            now: Current datetime (injected for testability, defaults to UTC now)

        Returns:
            Updated word_entity
        """
        if quality < 0 or quality > 5:
            raise ValueError(f"Quality must be 0-5, got {quality}")

        if now is None:
            now = datetime.now(timezone.utc)

        ef = word_entity.easiness_factor
        rep = word_entity.repetition_number
        interval = word_entity.interval_days

        if quality >= 3:
            if rep == 0:
                interval = 1
            elif rep == 1:
                interval = 6
            else:
                interval = round(interval * ef)
            rep += 1
        else:
            rep = 0
            interval = 1

        # Update easiness factor
        ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        if ef < 1.3:
            ef = 1.3

        word_entity.easiness_factor = ef
        word_entity.repetition_number = rep
        word_entity.interval_days = interval
        word_entity.next_review_at = now + timedelta(days=interval)

        # Calculate confidence & mastered status
        word_entity.confidence_score = self.calculate_confidence(word_entity, now=now)
        if word_entity.confidence_score >= 95 and rep >= 5:
            word_entity.is_mastered = True

        return word_entity

    def calculate_confidence(self, word_entity, now: datetime | None = None) -> float:
        """
        Calculate confidence score based on review history.

        Args:
            word_entity: WordEntity with review stats
            now: Current datetime (injected for testability)

        Returns:
            Confidence score 0-100
        """
        if word_entity.review_count == 0:
            return 0.0

        if now is None:
            now = datetime.now(timezone.utc)

        base = (word_entity.correct_count / word_entity.review_count) * 100

        # Recency bonus
        recency_bonus = 0
        if word_entity.last_reviewed_at:
            last_reviewed = word_entity.last_reviewed_at
            # Ensure timezone-aware comparison
            if hasattr(last_reviewed, 'tzinfo') and last_reviewed.tzinfo is None:
                last_reviewed = last_reviewed.replace(tzinfo=timezone.utc)
            if hasattr(now, 'tzinfo') and now.tzinfo is None:
                now = now.replace(tzinfo=timezone.utc)
            days_since = (now - last_reviewed).days
            if days_since <= 1:
                recency_bonus = 10
            elif days_since <= 3:
                recency_bonus = 5
            elif days_since <= 7:
                recency_bonus = 2

        # Streak bonus (capped at 20)
        streak_bonus = min(word_entity.repetition_number * 5, 20)

        return min(base + recency_bonus + streak_bonus, 100.0)

    def get_predicted_intervals(self, word_entity) -> dict:
        """
        For each quality (0-5), predict what the next interval would be.

        Returns:
            Dict mapping quality to human-readable interval string
        """
        predictions = {}
        for q in range(6):
            ef = word_entity.easiness_factor
            rep = word_entity.repetition_number
            interval = word_entity.interval_days

            if q >= 3:
                if rep == 0:
                    interval = 1
                elif rep == 1:
                    interval = 6
                else:
                    new_ef = ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
                    if new_ef < 1.3:
                        new_ef = 1.3
                    interval = round(interval * new_ef)
            else:
                interval = 1

            predictions[q] = self._format_interval(interval)

        return predictions

    @staticmethod
    def _format_interval(days: int) -> str:
        if days < 1:
            return "< 1 day"
        elif days == 1:
            return "1 day"
        elif days < 30:
            return f"{days} days"
        elif days < 365:
            months = days // 30
            return f"{months} month{'s' if months > 1 else ''}"
        else:
            years = days // 365
            return f"{years} year{'s' if years > 1 else ''}"


class WordEnrichmentDomainService:
    """Domain service for handling word enrichment data mapping."""

    @staticmethod
    def enrich_word(word_entity, enrichment_data: dict, now: datetime | None = None):
        """
        Map enrichment data dict onto word entity fields.

        Args:
            word_entity: WordEntity to update
            enrichment_data: Dict with enrichment fields from AI
            now: Current datetime (injected, defaults to UTC now)

        Returns:
            Updated word_entity
        """
        if now is None:
            now = datetime.now(timezone.utc)

        field_mapping = {
            "translation": "translation",
            "pronunciation": "pronunciation",
            "part_of_speech": "part_of_speech",
            "definition": "definition",
            "example_sentence": "example_sentence",
            "example_translation": "example_translation",
            "synonyms": "synonyms",
            "antonyms": "antonyms",
            "collocations": "collocations",
            "word_family": "word_family",
            "difficulty_level": "difficulty_level",
            "mnemonic": "mnemonic",
            "usage_notes": "usage_notes",
        }

        for source_key, entity_attr in field_mapping.items():
            if source_key in enrichment_data and enrichment_data[source_key]:
                setattr(word_entity, entity_attr, enrichment_data[source_key])

        word_entity.is_enriched = True
        word_entity.enrichment_status = "enriched"
        word_entity.enriched_at = now

        return word_entity


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
