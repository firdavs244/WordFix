"""
AI Smart Distractor Generator Service.

Generates intelligent wrong-answer options for tests and games
that are plausible but not synonyms of the target word.
"""

import logging
import random

from core.interfaces.ai_provider import AIProviderError

logger = logging.getLogger(__name__)


class DistractorGeneratorService:
    """Generate smart distractors for vocabulary tests and games."""

    def __init__(self, ai_provider, word_repo, distractor_repo):
        self.ai_provider = ai_provider
        self.word_repo = word_repo
        self.distractor_repo = distractor_repo

    def generate_distractors(
        self,
        word_id,
        word: str,
        translation: str,
        part_of_speech: str,
        synonyms: list,
        difficulty: str,
        user_id,
        user_level: str = "B1",
        native_language: str = "Uzbek",
        count: int = 3,
    ) -> list[str]:
        """
        Generate smart distractors for a word.

        1. Check cache (WordDistractor model)
        2. Cache hit → return cached
        3. Cache miss → try AI
        4. AI fail → fallback: random translations from user's other words
        5. Cache the result
        """
        # 1. Check cache
        cached = self.distractor_repo.get_by_word(word_id=word_id)
        if cached and len(cached.distractors) >= count:
            return cached.distractors[:count]

        # 2. Try AI
        distractors = self._generate_with_ai(
            word, translation, part_of_speech, synonyms,
            difficulty, user_level, native_language, count
        )

        if distractors and len(distractors) >= count:
            # Cache AI result
            self.distractor_repo.update_or_create(
                word_id=word_id,
                distractors=distractors[:count],
                generated_by="ai",
            )
            return distractors[:count]

        # 3. Fallback
        distractors = self._get_fallback_distractors(
            user_id, word_id, translation, synonyms, part_of_speech, count
        )

        if distractors:
            self.distractor_repo.update_or_create(
                word_id=word_id,
                distractors=distractors[:count],
                generated_by="fallback",
            )

        return distractors[:count]

    def _generate_with_ai(
        self, word, translation, part_of_speech, synonyms,
        difficulty, user_level, native_language, count
    ) -> list[str]:
        """Try AI-powered distractor generation."""
        if not self.ai_provider or not self.ai_provider.is_available():
            return []

        try:
            from core.services.ai.prompts import SMART_DISTRACTOR_PROMPT

            synonyms_str = ", ".join(synonyms) if synonyms else "none"

            prompt = SMART_DISTRACTOR_PROMPT.format(
                word=word,
                translation=translation,
                part_of_speech=part_of_speech or "word",
                user_level=user_level,
                synonyms=synonyms_str,
                count=count,
                native_language=native_language,
            )

            result = self.ai_provider.generate_json(prompt=prompt, max_tokens=500)

            if isinstance(result, dict) and "distractors" in result:
                distractors = result["distractors"]
                if isinstance(distractors, list) and len(distractors) > 0:
                    # Filter out synonyms
                    synonyms_lower = {s.lower() for s in synonyms} if synonyms else set()
                    synonyms_lower.add(translation.lower())
                    filtered = [
                        d for d in distractors
                        if isinstance(d, str) and d.lower() not in synonyms_lower
                    ]
                    return filtered

        except (AIProviderError, Exception) as e:
            logger.warning(f"AI distractor generation failed for '{word}': {e}")

        return []

    def _get_fallback_distractors(
        self, user_id, word_id, translation, synonyms, part_of_speech, count
    ) -> list[str]:
        """
        Fallback: get random translations from user's other words.
        Excludes synonyms and the correct translation.
        """
        try:
            words, _ = self.word_repo.get_all_by_user(
                user_id=user_id, page=1, page_size=200
            )

            synonyms_lower = {s.lower() for s in synonyms} if synonyms else set()
            synonyms_lower.add(translation.lower())

            candidates = []
            for w in words:
                if str(w.id) == str(word_id):
                    continue
                if not w.translation:
                    continue
                if w.translation.lower() in synonyms_lower:
                    continue
                # Prefer same part of speech
                candidates.append((w.translation, w.part_of_speech))

            # Sort: same POS first
            same_pos = [t for t, pos in candidates if pos == part_of_speech]
            diff_pos = [t for t, pos in candidates if pos != part_of_speech]

            random.shuffle(same_pos)
            random.shuffle(diff_pos)

            result = same_pos[:count]
            if len(result) < count:
                result.extend(diff_pos[:count - len(result)])

            return result[:count]

        except Exception as e:
            logger.warning(f"Fallback distractor generation failed: {e}")
            return []
