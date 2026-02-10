"""
Smart import use cases: text analysis and word import.
"""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class AnalyzeTextUseCase:
    """Analyze text and suggest unknown words for the user."""

    def __init__(self, word_repo, ai_provider, user_repo, prompt_template: str, language_map: dict):
        self.word_repo = word_repo
        self.ai_provider = ai_provider
        self.user_repo = user_repo
        self.prompt_template = prompt_template
        self.language_map = language_map

    def execute(self, user_id, text: str, max_words: int = 20) -> list[dict]:
        user_id = UUID(str(user_id))

        if not text or not text.strip():
            from apps.common.exceptions import ValidationError
            raise ValidationError("Text is required.")

        if len(text) > 5000:
            from apps.common.exceptions import ValidationError
            raise ValidationError("Text is too long. Maximum 5000 characters allowed.")

        # 1. Get user's existing words
        existing_words, _ = self.word_repo.get_all_by_user(
            user_id=user_id, page=1, page_size=10000,
        )
        known_words = [w.original_word.lower() for w in existing_words]

        # 2. Get user language info
        lang_info = self.user_repo.get_user_language_info(user_id)
        native_lang = self.language_map.get(
            lang_info.get("native_language", "uz"), "Uzbek"
        )
        proficiency = lang_info.get("proficiency_level", "A2")

        # 3. Try AI analysis
        if self.ai_provider:
            try:
                prompt = self.prompt_template.format(
                    text=text[:5000],
                    proficiency_level=proficiency,
                    native_language=native_lang,
                    known_words=", ".join(known_words[:200]) if known_words else "none",
                    max_words=max_words,
                )
                result = self.ai_provider.generate_json(prompt, max_tokens=2000, temperature=0.3)

                if isinstance(result, list):
                    suggestions = result
                elif isinstance(result, dict) and "words" in result:
                    suggestions = result["words"]
                else:
                    suggestions = [result] if isinstance(result, dict) else []

                # Filter out known words
                filtered = []
                for s in suggestions[:max_words]:
                    word = s.get("word", "").lower().strip()
                    if word and word not in known_words and len(word) > 2:
                        s["word"] = word
                        filtered.append(s)

                return filtered[:max_words]

            except Exception as e:
                logger.warning(f"AI analysis failed, using fallback: {e}")

        # 4. Fallback: simple extraction
        return self._fallback_extract(text, known_words, max_words)

    def _fallback_extract(self, text: str, known_words: list, max_words: int) -> list:
        """Simple regex-based word extraction fallback."""
        import re
        from collections import Counter

        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        word_counts = Counter(words)

        # Common English words to skip
        stop_words = {
            "the", "and", "for", "are", "but", "not", "you", "all", "can",
            "had", "her", "was", "one", "our", "out", "has", "his", "how",
            "its", "may", "new", "now", "old", "see", "way", "who", "did",
            "get", "let", "say", "she", "too", "use", "will", "with",
            "that", "this", "have", "from", "they", "been", "said", "each",
            "which", "their", "there", "were", "what", "when", "make",
            "like", "just", "over", "such", "take", "year", "them", "some",
            "than", "then", "very", "about", "would", "these", "other",
            "into", "more", "also", "been", "could", "your", "after",
        }

        suggestions = []
        for word, count in word_counts.most_common(max_words * 3):
            if word in known_words or word in stop_words:
                continue
            if len(word) < 4:
                continue
            suggestions.append({
                "word": word,
                "translation": "",
                "part_of_speech": "",
                "context_sentence": "",
                "difficulty": "medium",
                "reason": f"Appears {count} time(s) in the text",
            })
            if len(suggestions) >= max_words:
                break

        return suggestions


class ImportWordsUseCase:
    """Bulk import selected words into user's word bank."""

    def __init__(self, word_repo, enrich_task=None, enrichment_enabled: bool = True):
        self.word_repo = word_repo
        self.enrich_task = enrich_task
        self.enrichment_enabled = enrichment_enabled

    def execute(self, user_id, selected_words: list[dict]) -> dict:
        user_id = UUID(str(user_id))
        added = 0
        skipped = 0

        for word_data in selected_words:
            original_word = word_data.get("original_word", "").strip().lower()
            if not original_word:
                skipped += 1
                continue

            if self.word_repo.exists(original_word, user_id):
                skipped += 1
                continue

            try:
                word = self.word_repo.create(
                    user_id=user_id,
                    original_word=original_word,
                    translation=word_data.get("translation", ""),
                    difficulty_level=word_data.get("difficulty_level", "medium"),
                )
                added += 1

                # Queue enrichment
                if self.enrichment_enabled and self.enrich_task:
                    try:
                        self.enrich_task(str(word.id), str(user_id))
                    except Exception as e:
                        logger.warning(f"Failed to queue enrichment for {original_word}: {e}")

            except Exception as e:
                logger.warning(f"Failed to import word '{original_word}': {e}")
                skipped += 1

        return {"added": added, "skipped": skipped}
