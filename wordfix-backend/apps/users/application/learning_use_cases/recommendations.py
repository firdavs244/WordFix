"""
Word Recommendation use cases – generate, accept recommendations.
"""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class GetWordRecommendationsUseCase:
    """Return current recommendations, generating new ones if needed."""

    FALLBACK_WORDS = [
        # --- Academic / High-frequency ---
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
        # --- Level-appropriate / Professional ---
        {"word": "investigate", "translation": "tekshirmoq", "reason": "Academic verb", "reason_type": "high_frequency"},
        {"word": "justify", "translation": "asoslamoq", "reason": "Formal writing", "reason_type": "level_appropriate"},
        {"word": "maintain", "translation": "saqlamoq", "reason": "Common verb", "reason_type": "high_frequency"},
        {"word": "obtain", "translation": "olmoq, qo'lga kiritmoq", "reason": "Formal verb", "reason_type": "level_appropriate"},
        {"word": "participate", "translation": "ishtirok etmoq", "reason": "Active vocabulary", "reason_type": "high_frequency"},
        {"word": "perceive", "translation": "idrok qilmoq", "reason": "Advanced verb", "reason_type": "level_appropriate"},
        {"word": "pursue", "translation": "quvmoq, intilmoq", "reason": "Goal-oriented word", "reason_type": "level_appropriate"},
        {"word": "require", "translation": "talab qilmoq", "reason": "Essential verb", "reason_type": "high_frequency"},
        {"word": "significant", "translation": "muhim, sezilarli", "reason": "Academic adjective", "reason_type": "high_frequency"},
        {"word": "sufficient", "translation": "yetarli", "reason": "Formal adjective", "reason_type": "level_appropriate"},
        # --- Intermediate ---
        {"word": "acquire", "translation": "egallamoq", "reason": "Formal synonym of 'get'", "reason_type": "level_appropriate"},
        {"word": "acknowledge", "translation": "tan olmoq", "reason": "Professional word", "reason_type": "level_appropriate"},
        {"word": "accomplish", "translation": "bajarmoq", "reason": "Achievement vocabulary", "reason_type": "high_frequency"},
        {"word": "consequence", "translation": "oqibat", "reason": "Cause-effect vocabulary", "reason_type": "high_frequency"},
        {"word": "contribute", "translation": "hissa qo'shmoq", "reason": "Community vocabulary", "reason_type": "high_frequency"},
        {"word": "crucial", "translation": "juda muhim", "reason": "Emphasis word", "reason_type": "high_frequency"},
        {"word": "diminish", "translation": "kamaymoq", "reason": "Advanced verb", "reason_type": "level_appropriate"},
        {"word": "elaborate", "translation": "batafsil tushuntirmoq", "reason": "Academic discourse", "reason_type": "level_appropriate"},
        {"word": "emphasize", "translation": "ta'kidlamoq", "reason": "Communication skill", "reason_type": "high_frequency"},
        {"word": "enhance", "translation": "yaxshilamoq", "reason": "Improvement vocabulary", "reason_type": "high_frequency"},
        # --- Upper-intermediate ---
        {"word": "fluctuate", "translation": "o'zgarib turmoq", "reason": "Data/trends vocabulary", "reason_type": "level_appropriate"},
        {"word": "guarantee", "translation": "kafolatlamoq", "reason": "Business vocabulary", "reason_type": "high_frequency"},
        {"word": "hypothesis", "translation": "faraziya", "reason": "Scientific term", "reason_type": "level_appropriate"},
        {"word": "implement", "translation": "amalga oshirmoq", "reason": "Professional verb", "reason_type": "high_frequency"},
        {"word": "incorporate", "translation": "qo'shib yubormoq", "reason": "Business vocabulary", "reason_type": "level_appropriate"},
        {"word": "inevitable", "translation": "muqarrar", "reason": "Advanced adjective", "reason_type": "level_appropriate"},
        {"word": "infrastructure", "translation": "infratuzilma", "reason": "Modern vocabulary", "reason_type": "level_appropriate"},
        {"word": "negotiate", "translation": "muzokara qilmoq", "reason": "Professional skill", "reason_type": "high_frequency"},
        {"word": "phenomenon", "translation": "hodisa", "reason": "Scientific/academic", "reason_type": "level_appropriate"},
        {"word": "preliminary", "translation": "dastlabki", "reason": "Formal adjective", "reason_type": "level_appropriate"},
        # --- Advanced / Idiomatic ---
        {"word": "comprehensive", "translation": "har tomonlama", "reason": "Academic adjective", "reason_type": "level_appropriate"},
        {"word": "controversy", "translation": "munozara, tortishuv", "reason": "Discussion vocabulary", "reason_type": "level_appropriate"},
        {"word": "deteriorate", "translation": "yomonlashmoq", "reason": "Advanced verb", "reason_type": "level_appropriate"},
        {"word": "distinguish", "translation": "farqlamoq", "reason": "Critical thinking", "reason_type": "high_frequency"},
        {"word": "enormous", "translation": "ulkan", "reason": "Descriptive vocabulary", "reason_type": "high_frequency"},
        {"word": "prosperity", "translation": "farovonlik", "reason": "Economic vocabulary", "reason_type": "level_appropriate"},
        {"word": "reluctant", "translation": "istamaydigan", "reason": "Emotional vocabulary", "reason_type": "level_appropriate"},
        {"word": "simultaneously", "translation": "bir vaqtda", "reason": "Advanced adverb", "reason_type": "level_appropriate"},
        {"word": "straightforward", "translation": "oddiy, tushunarli", "reason": "Communication word", "reason_type": "high_frequency"},
        {"word": "substantial", "translation": "sezilarli, katta", "reason": "Formal adjective", "reason_type": "level_appropriate"},
        # --- Additional useful words ---
        {"word": "accommodate", "translation": "joylashtirmoq", "reason": "Hospitality vocabulary", "reason_type": "level_appropriate"},
        {"word": "ambiguous", "translation": "noaniq", "reason": "Critical thinking", "reason_type": "level_appropriate"},
        {"word": "anticipate", "translation": "kutmoq, oldindan bilmoq", "reason": "Planning vocabulary", "reason_type": "high_frequency"},
        {"word": "compatible", "translation": "mos keladigan", "reason": "Tech/relationship vocabulary", "reason_type": "high_frequency"},
        {"word": "contemplate", "translation": "o'ylab ko'rmoq", "reason": "Thoughtful vocabulary", "reason_type": "level_appropriate"},
        {"word": "deceptive", "translation": "aldamchi", "reason": "Advanced adjective", "reason_type": "level_appropriate"},
        {"word": "diligent", "translation": "tirishqoq", "reason": "Character vocabulary", "reason_type": "level_appropriate"},
        {"word": "endeavor", "translation": "harakat qilmoq", "reason": "Formal verb", "reason_type": "level_appropriate"},
        {"word": "legitimate", "translation": "qonuniy, to'g'ri", "reason": "Legal/formal vocabulary", "reason_type": "level_appropriate"},
        {"word": "magnificent", "translation": "ajoyib, ulug'vor", "reason": "Descriptive vocabulary", "reason_type": "level_appropriate"},
    ]

    def __init__(self, recommendation_repo, ai_provider=None, word_repo=None):
        self.recommendation_repo = recommendation_repo
        self.ai_provider = ai_provider
        self.word_repo = word_repo

    def _get_excluded_words(self, user_id: UUID) -> set[str]:
        """Get words that should NOT be recommended (already in word bank, active recs, or previously accepted)."""
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
        # Words previously accepted (prevent re-recommendation of same word)
        try:
            accepted_words = self.recommendation_repo.get_accepted_words(user_id)
            excluded.update(w.lower() for w in accepted_words if w)
        except Exception:
            logger.warning("Failed to get accepted recommendation words")
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
        seen: set[str] = set()
        result: list[dict] = []
        for r in recs:
            key = r.recommended_word.strip().lower()
            if key in seen:
                continue
            seen.add(key)
            result.append({
                "id": str(r.id),
                "word": r.recommended_word,
                "translation": r.translation,
                "reason": r.reason,
                "reason_type": r.reason_type,
                "priority": r.priority_score,
                "is_accepted": r.is_accepted,
                "ai_confidence": r.ai_confidence,
            })
        return result


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
