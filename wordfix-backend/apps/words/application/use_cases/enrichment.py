"""
Word enrichment use cases.
"""

import logging
import os
import time
from datetime import datetime, timezone
from uuid import UUID

from apps.words.domain.services import WordEnrichmentDomainService
from core.interfaces.ai_provider import AIProviderError

logger = logging.getLogger(__name__)


class EnrichWordUseCase:
    """Enrich a single word with AI-generated data."""

    def __init__(
        self,
        word_repo,
        ai_provider,
        tts_provider=None,
        user_repo=None,
        media_root: str = "",
        media_url: str = "media/",
        prompt_template: str = "",
        language_map: dict | None = None,
        distractor_task: callable = None,
    ):
        self.word_repo = word_repo
        self.ai_provider = ai_provider
        self.tts_provider = tts_provider
        self.user_repo = user_repo
        self.media_root = media_root
        self.media_url = media_url
        self.prompt_template = prompt_template
        self.language_map = language_map or {}
        self.distractor_task = distractor_task

    def execute(self, word_id, user_id):
        word_id = UUID(str(word_id))
        user_id = UUID(str(user_id))

        word = self.word_repo.get_by_id(word_id=word_id, user_id=user_id)

        # Get user info for prompt customization via repository
        native_lang = "Uzbek"
        proficiency = "B1"
        if self.user_repo:
            try:
                user_info = self.user_repo.get_user_language_info(user_id)
                native_lang = self.language_map.get(
                    user_info["native_language"],
                    user_info.get("native_language", "Uzbek"),
                )
                proficiency = user_info.get("proficiency_level", "B1")
            except Exception:
                pass

        # Check AI availability
        if not self.ai_provider.is_available():
            logger.warning(
                f"AI provider not available, skipping enrichment for word {word_id}"
            )
            return word

        # Set enrichment status
        self.word_repo.update(
            word_id=word_id, user_id=user_id, enrichment_status="enriching"
        )

        try:
            prompt = self.prompt_template.format(
                native_language=native_lang,
                learning_language="English",
                proficiency_level=proficiency,
                word=word.original_word,
            )

            enrichment_data = self.ai_provider.generate_json(prompt=prompt)

            enrichment_service = WordEnrichmentDomainService()
            now = datetime.now(timezone.utc)
            enrichment_service.enrich_word(word, enrichment_data, now=now)

            # Save enriched data
            update_fields = {
                "translation": word.translation,
                "pronunciation": word.pronunciation,
                "part_of_speech": word.part_of_speech,
                "definition": word.definition,
                "example_sentence": word.example_sentence,
                "example_translation": word.example_translation,
                "synonyms": word.synonyms,
                "antonyms": word.antonyms,
                "collocations": word.collocations,
                "word_family": word.word_family,
                "difficulty_level": word.difficulty_level,
                "mnemonic": word.mnemonic,
                "usage_notes": word.usage_notes,
                "is_enriched": True,
                "enrichment_status": "enriched",
                "enriched_at": now,
            }

            # Generate TTS audio if provider available
            if self.tts_provider:
                try:
                    audio_bytes = self.tts_provider.generate_audio(word.original_word)
                    # Save audio file
                    audio_dir = os.path.join(
                        self.media_root, "audio", "words",
                        str(user_id), str(word_id)
                    )
                    os.makedirs(audio_dir, exist_ok=True)
                    audio_path = os.path.join(audio_dir, "pronunciation.mp3")
                    with open(audio_path, "wb") as f:
                        f.write(audio_bytes)
                    update_fields["audio_url"] = (
                        f"{self.media_url}audio/words/{user_id}/{word_id}/pronunciation.mp3"
                    )
                except Exception as e:
                    logger.warning(f"TTS generation failed for {word_id}: {e}")

            updated_word = self.word_repo.update(
                word_id=word_id, user_id=user_id, **update_fields
            )

            # Trigger smart distractor generation
            if self.distractor_task:
                try:
                    self.distractor_task(str(word_id), str(user_id))
                except Exception as e:
                    logger.warning(f"Failed to queue distractor generation: {e}")

            return updated_word

        except AIProviderError as e:
            logger.error(f"AI enrichment failed for word {word_id}: {e}")
            self.word_repo.update(
                word_id=word_id, user_id=user_id,
                enrichment_status="failed", enrichment_error=str(e),
            )
            raise
        except Exception as e:
            logger.error(f"Enrichment error for word {word_id}: {e}")
            self.word_repo.update(
                word_id=word_id, user_id=user_id,
                enrichment_status="failed", enrichment_error=str(e),
            )
            raise


class BatchEnrichUseCase:
    """Enrich multiple words at once."""

    def __init__(self, word_repo, ai_provider, tts_provider=None):
        self.word_repo = word_repo
        self.ai_provider = ai_provider
        self.tts_provider = tts_provider

    def execute(self, user_id, word_ids: list):
        enriched = 0
        failed = 0
        errors = []
        enrich_uc = EnrichWordUseCase(
            self.word_repo, self.ai_provider, self.tts_provider
        )

        for word_id in word_ids:
            try:
                enrich_uc.execute(word_id, user_id)
                enriched += 1
            except Exception as e:
                failed += 1
                errors.append({"word_id": str(word_id), "error": str(e)})

            # Rate limiting: 1s between requests
            if word_ids.index(word_id) < len(word_ids) - 1:
                time.sleep(1)

        return {"enriched": enriched, "failed": failed, "errors": errors}
