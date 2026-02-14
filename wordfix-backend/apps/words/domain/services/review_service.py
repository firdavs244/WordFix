"""
Review and enrichment domain services.

Business logic for spaced repetition (SM-2) and word enrichment.

CLEAN ARCHITECTURE: No Django imports. Uses stdlib only.
"""

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
