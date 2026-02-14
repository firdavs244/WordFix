"""
Word Recommendation use cases – generate, accept recommendations.
"""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class GetWordRecommendationsUseCase:
    """Return current recommendations, generating new ones if needed."""

    FALLBACK_WORDS = [
        {"word": "analyze", "translation": "tahlil qilmoq", "reason": "Academic vocabulary", "reason_type": "high_frequency"},
        {"word": "approach", "translation": "yondashuv", "reason": "Common academic word", "reason_type": "high_frequency"},
        {"word": "benefit", "translation": "foyda", "reason": "Versatile word", "reason_type": "high_frequency"},
        {"word": "concept", "translation": "tushuncha", "reason": "Academic core word", "reason_type": "high_frequency"},
        {"word": "demonstrate", "translation": "namoyish qilmoq", "reason": "Formal vocabulary", "reason_type": "level_appropriate"},
        {"word": "establish", "translation": "tashkil etmoq", "reason": "Professional vocabulary", "reason_type": "level_appropriate"},
        {"word": "evident", "translation": "aniq", "reason": "Formal adjective", "reason_type": "level_appropriate"},
        {"word": "factor", "translation": "omil", "reason": "Commonly used", "reason_type": "high_frequency"},
        {"word": "generate", "translation": "yaratmoq", "reason": "Academic verb", "reason_type": "high_frequency"},
        {"word": "indicate", "translation": "ko'rsatmoq", "reason": "Academic verb", "reason_type": "high_frequency"},
    ]

    def __init__(self, recommendation_repo, ai_provider=None, word_repo=None):
        self.recommendation_repo = recommendation_repo
        self.ai_provider = ai_provider
        self.word_repo = word_repo

    def _get_excluded_words(self, user_id: UUID) -> set[str]:
        """Get words that should NOT be recommended (already in word bank or active recs)."""
        excluded: set[str] = set()
        # Words already in user's word bank
        if self.word_repo:
            try:
                words, _ = self.word_repo.get_all_by_user(user_id, page=1, page_size=500)
                excluded.update(w.original_word.lower() for w in words if w.original_word)
            except Exception:
                logger.warning("Failed to get user words for exclusion")
        # Words already in active recommendations
        try:
            active_words = self.recommendation_repo.get_active_words(user_id)
            excluded.update(w.lower() for w in active_words if w)
        except Exception:
            logger.warning("Failed to get active recommendation words")
        return excluded

    def execute(self, user_id: UUID, count: int = 10) -> list[dict]:
        existing = self.recommendation_repo.get_active(user_id, limit=count)
        if len(existing) >= count:
            return self._to_dicts(existing)

        needed = count - len(existing)
        new_recs = self._generate_recommendations(user_id, needed)
        all_recs = existing + new_recs
        return self._to_dicts(all_recs)

    def _generate_recommendations(self, user_id: UUID, count: int) -> list:
        """Try AI generation, fall back to hardcoded list."""
        excluded = self._get_excluded_words(user_id)

        if self.ai_provider and self.ai_provider.is_available():
            try:
                exclude_str = ", ".join(sorted(excluded)[:50]) if excluded else "none"
                prompt = (
                    f"Suggest {count} English words for an Uzbek learner at intermediate level. "
                    f"Do NOT recommend these words: [{exclude_str}]. "
                    f"Return JSON: {{\"words\": [{{\"word\": ..., \"translation\": ..., \"reason\": ...}}]}}"
                )
                result = self.ai_provider.generate_json(prompt)
                words = result.get("words", [])[:count]
                recs = []
                for w in words:
                    word_text = w.get("word", "").strip().lower()
                    if not word_text or word_text in excluded:
                        continue
                    if self.recommendation_repo.exists_for_word(user_id, word_text):
                        continue
                    try:
                        rec = self.recommendation_repo.create(
                            user_id=user_id,
                            recommended_word=word_text,
                            translation=w.get("translation", ""),
                            reason=w.get("reason", ""),
                            reason_type="level_appropriate",
                            priority_score=0.7,
                            ai_confidence=0.8,
                        )
                        recs.append(rec)
                        excluded.add(word_text)
                    except Exception:
                        logger.warning("Failed to create recommendation for word: %s", word_text)
                return recs
            except Exception:
                logger.warning("AI recommendation failed, using fallback")

        return self._get_fallback_recommendations(user_id, count, excluded)

    def _get_fallback_recommendations(self, user_id: UUID, count: int, excluded: set[str] | None = None) -> list:
        if excluded is None:
            excluded = self._get_excluded_words(user_id)
        recs = []
        for item in self.FALLBACK_WORDS:
            if len(recs) >= count:
                break
            word_text = item["word"].strip().lower()
            if word_text in excluded:
                continue
            if self.recommendation_repo.exists_for_word(user_id, word_text):
                continue
            try:
                rec = self.recommendation_repo.create(
                    user_id=user_id,
                    recommended_word=word_text,
                    translation=item["translation"],
                    reason=item["reason"],
                    reason_type=item["reason_type"],
                    priority_score=0.5,
                    ai_confidence=0.0,
                    source_data={"source": "fallback"},
                )
                recs.append(rec)
                excluded.add(word_text)
            except Exception:
                logger.warning("Failed to create fallback recommendation for: %s", word_text)
        return recs

    @staticmethod
    def _to_dicts(recs) -> list[dict]:
        return [
            {
                "id": str(r.id),
                "recommended_word": r.recommended_word,
                "translation": r.translation,
                "reason": r.reason,
                "reason_type": r.reason_type,
                "priority_score": r.priority_score,
                "is_accepted": r.is_accepted,
                "ai_confidence": r.ai_confidence,
            }
            for r in recs
        ]


class AcceptRecommendationUseCase:
    """Accept a word recommendation and add it to the user's word bank."""

    def __init__(self, recommendation_repo, word_repo=None):
        self.recommendation_repo = recommendation_repo
        self.word_repo = word_repo

    def execute(self, user_id: UUID, recommendation_id: UUID) -> dict:
        from apps.common.exceptions import EntityNotFoundError

        # 1. Get recommendation first to extract word data
        recommendation = self.recommendation_repo.get_by_id(recommendation_id, user_id)
        if not recommendation:
            raise EntityNotFoundError("Recommendation not found.")

        if recommendation.is_accepted:
            return {
                "success": True,
                "word_id": None,
                "message": "Recommendation already accepted.",
            }

        # 2. Accept the recommendation
        accepted = self.recommendation_repo.accept(recommendation_id, user_id)
        if not accepted:
            raise EntityNotFoundError("Failed to accept recommendation.")

        # 3. Create word in user's word bank
        word_id = None
        if self.word_repo:
            try:
                word = self.word_repo.create(
                    user_id=user_id,
                    original_word=recommendation.recommended_word,
                    translation=recommendation.translation,
                )
                word_id = str(word.id) if word else None
            except Exception as e:
                logger.warning(
                    "Failed to create word from recommendation: %s (word='%s')",
                    e,
                    recommendation.recommended_word,
                )

        return {"success": True, "word_id": word_id}
