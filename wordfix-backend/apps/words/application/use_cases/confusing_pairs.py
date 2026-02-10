"""
Confusing pairs detection, drill generation, and management use cases.
"""

import logging
from uuid import UUID

from apps.common.exceptions import ValidationError
from core.interfaces.ai_provider import AIProviderError

logger = logging.getLogger(__name__)


class DetectConfusionUseCase:
    """Detect if a wrong answer matches another word's translation."""

    def __init__(self, word_repo, confusing_pair_repo):
        self.word_repo = word_repo
        self.confusing_pair_repo = confusing_pair_repo

    def execute(self, user_id, word_id, wrong_answer: str):
        """
        Check if wrong_answer matches another word's translation.
        If so, create or increment a confusing pair.
        Returns ConfusingPairEntity or None.
        """
        user_id = UUID(str(user_id))
        word_id = UUID(str(word_id))

        if not wrong_answer or not wrong_answer.strip():
            return None

        wrong_answer_lower = wrong_answer.strip().lower()

        try:
            # Get user's words to check if wrong answer matches another word
            words, _ = self.word_repo.get_all_by_user(
                user_id=user_id, page=1, page_size=5000,
            )

            for w in words:
                if str(w.id) == str(word_id):
                    continue
                if not w.translation:
                    continue
                # Check if wrong answer matches this word's translation
                if w.translation.strip().lower() == wrong_answer_lower:
                    # Found confusing pair
                    pair, created = self.confusing_pair_repo.get_or_create(
                        user_id=user_id,
                        word_1_id=word_id,
                        word_2_id=w.id,
                    )
                    if not created:
                        pair = self.confusing_pair_repo.increment_confusion(pair.id)
                    return pair

        except Exception as e:
            logger.warning(f"Confusion detection failed: {e}")

        return None


class GetConfusingPairsUseCase:
    """Get all confusing pairs for a user."""

    def __init__(self, confusing_pair_repo, word_repo):
        self.confusing_pair_repo = confusing_pair_repo
        self.word_repo = word_repo

    def execute(self, user_id, include_resolved: bool = False) -> list[dict]:
        user_id = UUID(str(user_id))
        pairs = self.confusing_pair_repo.get_by_user(
            user_id=user_id, include_resolved=include_resolved
        )

        result = []
        for pair in pairs:
            try:
                word_1 = self.word_repo.get_by_id(word_id=pair.word_1_id, user_id=user_id)
                word_2 = self.word_repo.get_by_id(word_id=pair.word_2_id, user_id=user_id)
                result.append({
                    "id": str(pair.id),
                    "word_1": {
                        "id": str(word_1.id),
                        "original_word": word_1.original_word,
                        "translation": word_1.translation,
                    },
                    "word_2": {
                        "id": str(word_2.id),
                        "original_word": word_2.original_word,
                        "translation": word_2.translation,
                    },
                    "confusion_count": pair.confusion_count,
                    "last_confused_at": pair.last_confused_at.isoformat() if pair.last_confused_at else None,
                    "is_resolved": pair.is_resolved,
                })
            except Exception as e:
                logger.warning(f"Failed to get word details for pair {pair.id}: {e}")

        return result


class GetConfusingPairDetailUseCase:
    """Get details of a single confusing pair."""

    def __init__(self, confusing_pair_repo, word_repo):
        self.confusing_pair_repo = confusing_pair_repo
        self.word_repo = word_repo

    def execute(self, user_id, pair_id) -> dict:
        user_id = UUID(str(user_id))
        pair_id = UUID(str(pair_id))

        pair = self.confusing_pair_repo.get_by_id(pair_id=pair_id, user_id=user_id)
        word_1 = self.word_repo.get_by_id(word_id=pair.word_1_id, user_id=user_id)
        word_2 = self.word_repo.get_by_id(word_id=pair.word_2_id, user_id=user_id)

        return {
            "id": str(pair.id),
            "word_1": {
                "id": str(word_1.id),
                "original_word": word_1.original_word,
                "translation": word_1.translation,
                "definition": word_1.definition,
                "example_sentence": word_1.example_sentence,
            },
            "word_2": {
                "id": str(word_2.id),
                "original_word": word_2.original_word,
                "translation": word_2.translation,
                "definition": word_2.definition,
                "example_sentence": word_2.example_sentence,
            },
            "confusion_count": pair.confusion_count,
            "last_confused_at": pair.last_confused_at.isoformat() if pair.last_confused_at else None,
            "is_resolved": pair.is_resolved,
            "drill_data": pair.drill_data,
        }


class GenerateConfusionDrillUseCase:
    """Generate or retrieve an AI drill for a confusing pair."""

    def __init__(self, confusing_pair_repo, word_repo, ai_provider=None,
                 user_repo=None, prompt_template="", language_map=None):
        self.confusing_pair_repo = confusing_pair_repo
        self.word_repo = word_repo
        self.ai_provider = ai_provider
        self.user_repo = user_repo
        self.prompt_template = prompt_template
        self.language_map = language_map or {}

    def execute(self, user_id, pair_id) -> dict:
        user_id = UUID(str(user_id))
        pair_id = UUID(str(pair_id))

        pair = self.confusing_pair_repo.get_by_id(pair_id=pair_id, user_id=user_id)

        # Return cached drill if available
        if pair.drill_data and isinstance(pair.drill_data, dict) and pair.drill_data.get("explanation"):
            return pair.drill_data

        word_1 = self.word_repo.get_by_id(word_id=pair.word_1_id, user_id=user_id)
        word_2 = self.word_repo.get_by_id(word_id=pair.word_2_id, user_id=user_id)

        # Get user language info
        native_lang = "Uzbek"
        proficiency = "B1"
        if self.user_repo:
            try:
                user_info = self.user_repo.get_user_language_info(user_id)
                native_lang = self.language_map.get(
                    user_info.get("native_language", "uz"), "Uzbek"
                )
                proficiency = user_info.get("proficiency_level", "B1")
            except Exception:
                pass

        # Try AI generation
        drill_data = self._generate_ai_drill(
            word_1, word_2, pair.confusion_count, native_lang, proficiency
        )

        if not drill_data:
            drill_data = self._generate_basic_drill(word_1, word_2, native_lang)

        # Cache the drill
        self.confusing_pair_repo.update(pair_id=pair_id, drill_data=drill_data)

        return drill_data

    def _generate_ai_drill(self, word_1, word_2, confusion_count, native_lang, proficiency) -> dict:
        """Generate drill using AI."""
        if not self.ai_provider or not self.ai_provider.is_available():
            return {}

        if not self.prompt_template:
            return {}

        try:
            prompt = self.prompt_template.format(
                native_language=native_lang,
                proficiency_level=proficiency,
                word_1=word_1.original_word,
                translation_1=word_1.translation,
                word_2=word_2.original_word,
                translation_2=word_2.translation,
                confusion_count=confusion_count,
            )

            result = self.ai_provider.generate_json(prompt=prompt, max_tokens=2000)

            if isinstance(result, dict) and "explanation" in result:
                return result

        except (AIProviderError, Exception) as e:
            logger.warning(f"AI drill generation failed: {e}")

        return {}

    def _generate_basic_drill(self, word_1, word_2, native_lang) -> dict:
        """Generate a basic drill without AI."""
        return {
            "explanation": (
                f'"{word_1.original_word}" means "{word_1.translation}", '
                f'while "{word_2.original_word}" means "{word_2.translation}".'
            ),
            "word_1_examples": [
                {
                    "sentence": word_1.example_sentence or f"I use the word '{word_1.original_word}'.",
                    "translation": word_1.example_translation or word_1.translation,
                }
            ],
            "word_2_examples": [
                {
                    "sentence": word_2.example_sentence or f"I use the word '{word_2.original_word}'.",
                    "translation": word_2.example_translation or word_2.translation,
                }
            ],
            "mnemonic": f"Remember: '{word_1.original_word}' = {word_1.translation}, '{word_2.original_word}' = {word_2.translation}",
            "test_questions": [
                {
                    "sentence": f"Which word means '{word_1.translation}'?",
                    "correct_answer": word_1.original_word,
                    "wrong_answer": word_2.original_word,
                    "explanation": f"'{word_1.original_word}' means '{word_1.translation}'",
                },
                {
                    "sentence": f"Which word means '{word_2.translation}'?",
                    "correct_answer": word_2.original_word,
                    "wrong_answer": word_1.original_word,
                    "explanation": f"'{word_2.original_word}' means '{word_2.translation}'",
                },
            ],
        }


class ResolveConfusingPairUseCase:
    """Mark a confusing pair as resolved."""

    def __init__(self, confusing_pair_repo):
        self.confusing_pair_repo = confusing_pair_repo

    def execute(self, user_id, pair_id):
        user_id = UUID(str(user_id))
        pair_id = UUID(str(pair_id))

        # Verify ownership
        self.confusing_pair_repo.get_by_id(pair_id=pair_id, user_id=user_id)
        return self.confusing_pair_repo.resolve(pair_id=pair_id)


class GetConfusingPairCountUseCase:
    """Get count of unresolved confusing pairs."""

    def __init__(self, confusing_pair_repo):
        self.confusing_pair_repo = confusing_pair_repo

    def execute(self, user_id) -> int:
        user_id = UUID(str(user_id))
        return self.confusing_pair_repo.get_unresolved_count(user_id=user_id)
