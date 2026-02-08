"""
Word application use cases.

Includes CRUD, enrichment, review, streak, daily progress,
test generation, and game use cases.

CLEAN ARCHITECTURE: No Django/infrastructure imports.
All external dependencies injected via constructor.
"""

import json
import logging
import os
import random
import time
from datetime import date, datetime, timedelta, timezone
from typing import Callable
from uuid import UUID

from apps.common.exceptions import EntityAlreadyExistsError, ValidationError
from apps.words.domain.repositories import AbstractWordCategoryRepository, AbstractWordRepository
from apps.words.domain.services import SpacedRepetitionService, WordEnrichmentDomainService
from core.interfaces.ai_provider import AIProviderError

logger = logging.getLogger(__name__)


# =============================================================================
# CRUD USE CASES (existing)
# =============================================================================


class AddWordUseCase:
    """Add a new word to user's word bank."""

    def __init__(
        self,
        repository: AbstractWordRepository,
        enrich_task: Callable | None = None,
        enrichment_enabled: bool = True,
    ):
        self.repository = repository
        self.enrich_task = enrich_task
        self.enrichment_enabled = enrichment_enabled

    def execute(self, user_id: UUID, data: dict):
        """Validate and create a word. Triggers auto-enrichment if enabled."""
        original_word = data.get("original_word", "").strip().lower()
        if not original_word:
            raise ValidationError("Word is required.")

        word = self.repository.create(user_id=user_id, **data)

        # Trigger auto-enrichment
        if self.enrichment_enabled and self.enrich_task:
            try:
                self.enrich_task(str(word.id), str(user_id))
            except Exception as e:
                logger.warning(f"Failed to queue enrichment task: {e}")

        return word


class GetWordsUseCase:
    """Get paginated words list with filters."""

    def __init__(self, repository: AbstractWordRepository):
        self.repository = repository

    def execute(self, user_id: UUID, filters=None, ordering="-created_at", page=1, page_size=20):
        return self.repository.get_all_by_user(
            user_id=user_id, filters=filters, ordering=ordering,
            page=page, page_size=page_size,
        )


class GetWordDetailUseCase:
    """Get a single word detail."""

    def __init__(self, repository: AbstractWordRepository):
        self.repository = repository

    def execute(self, word_id: UUID, user_id: UUID):
        return self.repository.get_by_id(word_id=word_id, user_id=user_id)


class UpdateWordUseCase:
    """Update a word (partial)."""

    def __init__(self, repository: AbstractWordRepository):
        self.repository = repository

    def execute(self, word_id: UUID, user_id: UUID, data: dict):
        data.pop("original_word", None)
        return self.repository.update(word_id=word_id, user_id=user_id, **data)


class DeleteWordUseCase:
    """Delete a word permanently."""

    def __init__(self, repository: AbstractWordRepository):
        self.repository = repository

    def execute(self, word_id: UUID, user_id: UUID) -> None:
        self.repository.delete(word_id=word_id, user_id=user_id)


class BulkAddWordsUseCase:
    """Bulk add words."""

    def __init__(self, repository: AbstractWordRepository):
        self.repository = repository

    def execute(self, user_id: UUID, words_data: list[dict]) -> dict:
        return self.repository.bulk_create(user_id=user_id, words_data=words_data)


class GetWordStatsUseCase:
    """Get word stats for a user."""

    def __init__(self, repository: AbstractWordRepository):
        self.repository = repository

    def execute(self, user_id: UUID) -> dict:
        return self.repository.get_stats(user_id=user_id)


class SearchWordsUseCase:
    """Search words."""

    def __init__(self, repository: AbstractWordRepository):
        self.repository = repository

    def execute(self, user_id: UUID, query: str, page: int = 1, page_size: int = 20):
        return self.repository.search(
            user_id=user_id, query=query, page=page, page_size=page_size,
        )


# =============================================================================
# ENRICHMENT USE CASES
# =============================================================================


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
    ):
        self.word_repo = word_repo
        self.ai_provider = ai_provider
        self.tts_provider = tts_provider
        self.user_repo = user_repo
        self.media_root = media_root
        self.media_url = media_url
        self.prompt_template = prompt_template
        self.language_map = language_map or {}

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


# =============================================================================
# REVIEW USE CASES
# =============================================================================


class GetReviewWordsUseCase:
    """Get words due for review."""

    def __init__(self, word_repo):
        self.word_repo = word_repo

    def execute(self, user_id: UUID, limit: int = 20, session_type: str = "review"):
        return self.word_repo.get_review_words(
            user_id=user_id, limit=limit, session_type=session_type,
        )


class StartReviewSessionUseCase:
    """Start a new review session."""

    def __init__(self, session_repo):
        self.session_repo = session_repo

    def execute(self, user_id: UUID, session_type: str = "review", word_count: int = 0):
        return self.session_repo.create(
            user_id=user_id,
            session_type=session_type,
            total_words=word_count,
        )


class SubmitReviewAnswerUseCase:
    """Submit a review answer and update all related data."""

    def __init__(self, word_repo, session_repo, log_repo, sr_service, streak_repo, activity_repo):
        self.word_repo = word_repo
        self.session_repo = session_repo
        self.log_repo = log_repo
        self.sr_service = sr_service
        self.streak_repo = streak_repo
        self.activity_repo = activity_repo

    def execute(self, session_id, word_id, user_id, quality: int, response_time_ms: int = 0):
        if quality < 0 or quality > 5:
            raise ValidationError("Quality must be between 0 and 5.")

        session_id = UUID(str(session_id))
        word_id = UUID(str(word_id))
        user_id = UUID(str(user_id))

        # Get word
        word = self.word_repo.get_by_id(word_id=word_id, user_id=user_id)

        # Save previous state
        prev_confidence = word.confidence_score
        prev_interval = word.interval_days

        # Apply SM-2
        now = datetime.now(timezone.utc)
        self.sr_service.calculate_next_review(word, quality, now=now)

        # Update review counts
        word.review_count += 1
        is_correct = quality >= 3
        if is_correct:
            word.correct_count += 1
        else:
            word.incorrect_count += 1
        word.last_reviewed_at = now

        # Save word
        self.word_repo.update(
            word_id=word_id,
            user_id=user_id,
            confidence_score=word.confidence_score,
            next_review_at=word.next_review_at,
            review_count=word.review_count,
            correct_count=word.correct_count,
            incorrect_count=word.incorrect_count,
            last_reviewed_at=word.last_reviewed_at,
            is_mastered=word.is_mastered,
            easiness_factor=word.easiness_factor,
            repetition_number=word.repetition_number,
            interval_days=word.interval_days,
        )

        # Create review log
        self.log_repo.create(
            session_id=session_id,
            user_id=user_id,
            word_id=word_id,
            quality=quality,
            response_time_ms=response_time_ms,
            is_correct=is_correct,
            previous_confidence=prev_confidence,
            new_confidence=word.confidence_score,
            previous_interval=prev_interval,
            new_interval=word.interval_days,
        )

        # Update session stats
        session = self.session_repo.get_by_id(session_id=session_id, user_id=user_id)
        update_data = {
            "total_words": session.total_words + 1,
        }
        if is_correct:
            update_data["correct_count"] = session.correct_count + 1
        else:
            update_data["incorrect_count"] = session.incorrect_count + 1
        session = self.session_repo.update(session_id=session_id, **update_data)

        # Update daily activity
        activity = self.activity_repo.get_or_create_today(user_id=user_id)
        act_update = {
            "words_reviewed": activity.words_reviewed + 1,
        }
        if is_correct:
            act_update["correct_answers"] = activity.correct_answers + 1
        else:
            act_update["incorrect_answers"] = activity.incorrect_answers + 1
        if word.is_mastered:
            act_update["words_mastered"] = activity.words_mastered + 1
        act_update["xp_earned"] = activity.xp_earned + (quality * 3)
        self.activity_repo.update(activity_id=activity.id, **act_update)

        # Update streak
        streak_uc = UpdateStreakUseCase(self.streak_repo)
        streak = streak_uc.execute(user_id=user_id)

        return {
            "word": word,
            "session": session,
            "streak": streak,
            "is_correct": is_correct,
        }


class CompleteReviewSessionUseCase:
    """Complete a review session."""

    def __init__(self, session_repo, log_repo):
        self.session_repo = session_repo
        self.log_repo = log_repo

    def execute(self, session_id, user_id):
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        session = self.session_repo.get_by_id(session_id=session_id, user_id=user_id)
        now = datetime.now(timezone.utc)

        duration = 0
        if session.started_at:
            duration = int((now - session.started_at).total_seconds())

        # Calculate average quality
        logs = self.log_repo.get_by_session(session_id=session_id)
        avg_quality = 0.0
        if logs:
            avg_quality = sum(log.quality for log in logs) / len(logs)

        return self.session_repo.update(
            session_id=session_id,
            is_completed=True,
            completed_at=now,
            duration_seconds=duration,
            average_quality=round(avg_quality, 2),
        )


class GetReviewSummaryUseCase:
    """Get review summary for dashboard display."""

    def __init__(self, word_repo, streak_repo, activity_repo, user_repo=None):
        self.word_repo = word_repo
        self.streak_repo = streak_repo
        self.activity_repo = activity_repo
        self.user_repo = user_repo

    def execute(self, user_id: UUID) -> dict:
        user_id = UUID(str(user_id))

        # Get stats from repository
        stats = self.word_repo.get_review_summary_stats(user_id=user_id)

        # Daily goal
        daily_goal = 10
        if self.user_repo:
            try:
                user_info = self.user_repo.get_user_language_info(user_id)
                daily_goal = user_info.get("daily_goal", 10)
            except Exception:
                pass

        # Today's activity
        activity = self.activity_repo.get_or_create_today(user_id=user_id)
        daily_progress_pct = min(
            round((activity.words_reviewed / daily_goal * 100) if daily_goal > 0 else 0, 1),
            100.0,
        )

        # Streak
        streak = self.streak_repo.get_or_create(user_id=user_id)

        return {
            **stats,
            "daily_goal": daily_goal,
            "daily_progress_pct": daily_progress_pct,
            "streak": {
                "current": streak.current_streak,
                "longest": streak.longest_streak,
                "last_activity": str(streak.last_activity_date) if streak.last_activity_date else None,
            },
        }


class UpdateStreakUseCase:
    """Update user's daily streak."""

    def __init__(self, streak_repo):
        self.streak_repo = streak_repo

    def execute(self, user_id: UUID):
        user_id = UUID(str(user_id))
        streak = self.streak_repo.get_or_create(user_id=user_id)
        today = date.today()

        if streak.last_activity_date == today:
            return streak  # Already counted today

        yesterday = today - timedelta(days=1)

        if streak.last_activity_date == yesterday:
            new_streak = streak.current_streak + 1
        elif streak.last_activity_date is None:
            new_streak = 1
        elif (
            streak.streak_frozen_until
            and streak.streak_frozen_until >= today
        ):
            new_streak = streak.current_streak  # Frozen
        else:
            new_streak = 1  # Reset

        longest = max(new_streak, streak.longest_streak)

        return self.streak_repo.update(
            streak_id=streak.id,
            current_streak=new_streak,
            longest_streak=longest,
            last_activity_date=today,
            total_review_days=streak.total_review_days + 1,
        )


# =============================================================================
# TEST GENERATION USE CASES
# =============================================================================


class GenerateTestUseCase:
    """Generate an AI-powered test from user's words."""

    def __init__(
        self,
        word_repo,
        test_session_repo,
        test_question_repo,
        ai_provider=None,
        user_repo=None,
        prompt_templates: dict | None = None,
        language_map: dict | None = None,
    ):
        self.word_repo = word_repo
        self.test_session_repo = test_session_repo
        self.test_question_repo = test_question_repo
        self.ai_provider = ai_provider
        self.user_repo = user_repo
        self.prompt_templates = prompt_templates or {}
        self.language_map = language_map or {}

    def execute(
        self,
        user_id: UUID,
        test_type: str = "mixed",
        question_count: int = 10,
        difficulty: str = "adaptive",
    ):
        user_id = UUID(str(user_id))

        # Get user's words based on difficulty
        words, total = self.word_repo.get_all_by_user(
            user_id=user_id, page=1, page_size=200
        )
        if len(words) < 5:
            raise ValidationError("You need at least 5 words to generate a test.")

        # Filter words by difficulty preference
        selected = self._select_words(words, difficulty, question_count)

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

        # Try AI generation, fallback if unavailable
        questions_data = self._generate_with_ai(
            selected, test_type, question_count, native_lang, proficiency
        )

        if not questions_data:
            questions_data = self._generate_fallback(
                selected, test_type, question_count, words
            )

        # Create session
        session = self.test_session_repo.create(
            user_id=user_id,
            test_type=test_type,
            difficulty=difficulty,
            total_questions=len(questions_data),
        )

        # Create questions
        question_objects = []
        for i, q_data in enumerate(questions_data):
            question_objects.append({
                "session_id": session.id,
                "word_id": q_data["word_id"],
                "question_type": q_data.get("question_type", "multiple_choice"),
                "question_text": q_data["question_text"],
                "correct_answer": q_data["correct_answer"],
                "options": q_data.get("options", []),
                "explanation": q_data.get("explanation", ""),
                "order": i + 1,
            })
        questions = self.test_question_repo.bulk_create(question_objects)

        return {
            "session": session,
            "questions": questions,
        }

    def _select_words(self, words, difficulty, count):
        """Select words based on difficulty preference."""
        if difficulty == "easy":
            pool = [w for w in words if w.confidence_score > 50]
        elif difficulty == "hard":
            pool = [w for w in words if w.confidence_score < 30]
        elif difficulty == "medium":
            pool = [w for w in words if 30 <= w.confidence_score <= 70]
        else:  # adaptive
            pool = list(words)

        if len(pool) < 5:
            pool = list(words)

        random.shuffle(pool)
        return pool[:count]

    def _generate_with_ai(self, words, test_type, count, native_lang, proficiency):
        """Try AI-powered question generation."""
        if not self.ai_provider or not self.ai_provider.is_available():
            return []

        words_list = ", ".join(
            f"{w.original_word} ({w.translation})" for w in words if w.translation
        )
        if not words_list:
            words_list = ", ".join(w.original_word for w in words)

        word_map = {w.original_word.lower(): w for w in words}

        # Determine which prompt to use
        if test_type == "multiple_choice":
            template = self.prompt_templates.get("multiple_choice", "")
        elif test_type == "fill_blank":
            template = self.prompt_templates.get("fill_blank", "")
        elif test_type == "context_guess":
            template = self.prompt_templates.get("context_guess", "")
        else:  # mixed
            template = self.prompt_templates.get("multiple_choice", "")

        if not template:
            return []

        try:
            prompt = template.format(
                native_language=native_lang,
                proficiency_level=proficiency,
                count=count,
                words_list=words_list,
            )
            result = self.ai_provider.generate_json(prompt=prompt, max_tokens=3000)

            if isinstance(result, dict) and "questions" in result:
                result = result["questions"]
            if not isinstance(result, list):
                return []

            questions_data = []
            for item in result[:count]:
                word_key = item.get("word", "").lower()
                word_entity = word_map.get(word_key)
                if not word_entity:
                    # Try to match any word
                    for w in words:
                        if w.original_word.lower() in str(item).lower():
                            word_entity = w
                            break
                if not word_entity:
                    word_entity = random.choice(words)

                q_type = item.get("question_type", "multiple_choice")

                if test_type == "fill_blank" or q_type == "fill_blank":
                    q_text = item.get("sentence_with_blank", item.get("question", ""))
                    hint = item.get("hint", "")
                    if hint:
                        q_text += f"\n💡 Hint: {hint}"
                else:
                    q_text = item.get("question", item.get("context_paragraph", ""))

                questions_data.append({
                    "word_id": word_entity.id,
                    "question_type": q_type,
                    "question_text": q_text,
                    "correct_answer": item.get("correct_answer", word_entity.translation),
                    "options": item.get("options", []),
                    "explanation": item.get("explanation", ""),
                })

            return questions_data

        except (AIProviderError, Exception) as e:
            logger.warning(f"AI test generation failed: {e}")
            return []

    def _generate_fallback(self, selected_words, test_type, count, all_words):
        """Generate simple tests without AI."""
        questions = []
        all_translations = [
            w.translation for w in all_words if w.translation
        ]

        for i, word in enumerate(selected_words[:count]):
            if test_type in ("multiple_choice", "mixed"):
                q_data = self._fallback_multiple_choice(word, all_translations)
            elif test_type == "fill_blank":
                q_data = self._fallback_fill_blank(word)
            elif test_type == "context_guess":
                q_data = self._fallback_context(word, all_translations)
            else:
                q_data = self._fallback_multiple_choice(word, all_translations)

            q_data["word_id"] = word.id
            questions.append(q_data)

        return questions

    def _fallback_multiple_choice(self, word, all_translations):
        """Generate a simple word→translation multiple choice question."""
        correct = word.translation or word.original_word
        distractors = [t for t in all_translations if t and t != correct]
        random.shuffle(distractors)
        options = [correct] + distractors[:3]
        while len(options) < 4:
            options.append(f"option_{len(options)}")
        random.shuffle(options)
        return {
            "question_type": "word_to_translation",
            "question_text": f'What does "{word.original_word}" mean?',
            "correct_answer": correct,
            "options": options,
            "explanation": word.definition or f'"{word.original_word}" means "{correct}"',
        }

    def _fallback_fill_blank(self, word):
        """Generate a simple fill-blank question."""
        if word.example_sentence and word.original_word.lower() in word.example_sentence.lower():
            sentence = word.example_sentence.replace(
                word.original_word, "___"
            ).replace(
                word.original_word.capitalize(), "___"
            )
        else:
            sentence = f'The word "___ " means "{word.translation or "..."}"'
        return {
            "question_type": "fill_blank",
            "question_text": sentence,
            "correct_answer": word.original_word,
            "options": [],
            "explanation": word.definition or f'The answer is "{word.original_word}"',
        }

    def _fallback_context(self, word, all_translations):
        """Generate a simple context question using example sentence."""
        if word.example_sentence:
            context = word.example_sentence.replace(
                word.original_word, "___"
            ).replace(
                word.original_word.capitalize(), "___"
            )
        else:
            context = f'"___" means "{word.translation or "..."}"'

        correct = word.original_word
        distractors = [
            w_t for w_t in all_translations if w_t and w_t != correct
        ][:3]
        options = [correct] + distractors
        while len(options) < 4:
            options.append(f"word_{len(options)}")
        random.shuffle(options)

        return {
            "question_type": "context_guess",
            "question_text": context,
            "correct_answer": correct,
            "options": options,
            "explanation": word.definition or f'The answer is "{correct}"',
        }


class SubmitTestAnswerUseCase:
    """Submit an answer to a test question."""

    def __init__(self, question_repo, word_repo, sr_service, activity_repo):
        self.question_repo = question_repo
        self.word_repo = word_repo
        self.sr_service = sr_service
        self.activity_repo = activity_repo

    def execute(self, question_id, user_id, answer: str, response_time_ms: int = 0):
        question_id = UUID(str(question_id))
        user_id = UUID(str(user_id))

        question = self.question_repo.get_by_id(question_id=question_id)

        # Check correctness (case-insensitive)
        is_correct = answer.strip().lower() == question.correct_answer.strip().lower()

        # Update question
        self.question_repo.update(
            question_id=question_id,
            user_answer=answer,
            is_correct=is_correct,
            response_time_ms=response_time_ms,
        )

        # Update word SR
        word = self.word_repo.get_by_id(word_id=question.word_id, user_id=user_id)
        quality = 4 if is_correct else 1
        now = datetime.now(timezone.utc)
        self.sr_service.calculate_next_review(word, quality, now=now)

        word.review_count += 1
        if is_correct:
            word.correct_count += 1
        else:
            word.incorrect_count += 1
        word.last_reviewed_at = now

        self.word_repo.update(
            word_id=word.id,
            user_id=user_id,
            confidence_score=word.confidence_score,
            next_review_at=word.next_review_at,
            review_count=word.review_count,
            correct_count=word.correct_count,
            incorrect_count=word.incorrect_count,
            last_reviewed_at=word.last_reviewed_at,
            is_mastered=word.is_mastered,
            easiness_factor=word.easiness_factor,
            repetition_number=word.repetition_number,
            interval_days=word.interval_days,
        )

        return {
            "is_correct": is_correct,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation,
        }


class CompleteTestSessionUseCase:
    """Complete a test session and calculate results."""

    def __init__(self, test_session_repo, test_question_repo, activity_repo):
        self.test_session_repo = test_session_repo
        self.test_question_repo = test_question_repo
        self.activity_repo = activity_repo

    def execute(self, session_id, user_id):
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        session = self.test_session_repo.get_by_id(
            session_id=session_id, user_id=user_id
        )
        questions = self.test_question_repo.get_by_session(session_id=session_id)

        correct = sum(1 for q in questions if q.is_correct is True)
        incorrect = sum(1 for q in questions if q.is_correct is False)
        total = len(questions)
        score_pct = round((correct / total * 100) if total > 0 else 0, 1)

        now = datetime.now(timezone.utc)
        duration = 0
        if session.started_at:
            duration = int((now - session.started_at).total_seconds())

        updated = self.test_session_repo.update(
            session_id=session_id,
            is_completed=True,
            completed_at=now,
            correct_answers=correct,
            incorrect_answers=incorrect,
            score_percentage=score_pct,
            duration_seconds=duration,
        )

        # Update daily activity
        try:
            activity = self.activity_repo.get_or_create_today(user_id=user_id)
            xp = correct * 5
            self.activity_repo.update(
                activity_id=activity.id,
                words_reviewed=activity.words_reviewed + total,
                correct_answers=activity.correct_answers + correct,
                incorrect_answers=activity.incorrect_answers + incorrect,
                xp_earned=activity.xp_earned + xp,
            )
        except Exception:
            pass

        return updated


class GetTestHistoryUseCase:
    """Get test history for a user."""

    def __init__(self, test_session_repo):
        self.test_session_repo = test_session_repo

    def execute(self, user_id, page=1, page_size=20):
        user_id = UUID(str(user_id))
        return self.test_session_repo.get_by_user(
            user_id=user_id, page=page, page_size=page_size
        )


class GetTestDetailUseCase:
    """Get test session detail with all questions."""

    def __init__(self, test_session_repo, test_question_repo):
        self.test_session_repo = test_session_repo
        self.test_question_repo = test_question_repo

    def execute(self, session_id, user_id):
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))
        session = self.test_session_repo.get_by_id(
            session_id=session_id, user_id=user_id
        )
        questions = self.test_question_repo.get_by_session(session_id=session_id)
        return {"session": session, "questions": questions}


# =============================================================================
# GAME USE CASES
# =============================================================================


class StartSpeedRoundUseCase:
    """Start a speed round game."""

    def __init__(self, word_repo, game_session_repo):
        self.word_repo = word_repo
        self.game_session_repo = game_session_repo

    def execute(self, user_id):
        user_id = UUID(str(user_id))

        words, _ = self.word_repo.get_all_by_user(
            user_id=user_id, page=1, page_size=200
        )
        eligible = [w for w in words if w.confidence_score < 90 and w.translation]
        if len(eligible) < 5:
            if len(words) < 5:
                raise ValidationError("You need at least 5 words with translations to play.")
            eligible = [w for w in words if w.translation]
            if len(eligible) < 5:
                raise ValidationError("You need at least 5 words with translations to play.")

        random.shuffle(eligible)
        selected = eligible[:min(25, len(eligible))]

        all_translations = [w.translation for w in words if w.translation]

        # Build word items with options
        items = []
        for word in selected:
            distractors = [t for t in all_translations if t != word.translation]
            random.shuffle(distractors)
            options = [word.translation] + distractors[:3]
            while len(options) < 4:
                options.append(f"option_{len(options)}")
            random.shuffle(options)
            items.append({
                "word_id": str(word.id),
                "word": word.original_word,
                "correct_translation": word.translation,
                "options": options,
            })

        session = self.game_session_repo.create(
            user_id=user_id,
            game_type="speed_round",
            max_score=len(items),
        )

        return {
            "session_id": str(session.id),
            "words": items,
            "time_limit": 60,
        }


class SubmitSpeedRoundUseCase:
    """Submit speed round results."""

    def __init__(self, word_repo, game_session_repo, sr_service, activity_repo):
        self.word_repo = word_repo
        self.game_session_repo = game_session_repo
        self.sr_service = sr_service
        self.activity_repo = activity_repo

    def execute(self, session_id, user_id, answers, duration_seconds=60):
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        correct = 0
        incorrect = 0
        now = datetime.now(timezone.utc)

        for ans in answers:
            word_id = UUID(str(ans["word_id"]))
            try:
                word = self.word_repo.get_by_id(word_id=word_id, user_id=user_id)
                is_right = ans.get("selected_answer", "").strip().lower() == word.translation.strip().lower()

                quality = 4 if is_right else 1
                self.sr_service.calculate_next_review(word, quality, now=now)
                word.review_count += 1
                if is_right:
                    word.correct_count += 1
                    correct += 1
                else:
                    word.incorrect_count += 1
                    incorrect += 1
                word.last_reviewed_at = now

                self.word_repo.update(
                    word_id=word.id, user_id=user_id,
                    confidence_score=word.confidence_score,
                    next_review_at=word.next_review_at,
                    review_count=word.review_count,
                    correct_count=word.correct_count,
                    incorrect_count=word.incorrect_count,
                    last_reviewed_at=word.last_reviewed_at,
                    is_mastered=word.is_mastered,
                    easiness_factor=word.easiness_factor,
                    repetition_number=word.repetition_number,
                    interval_days=word.interval_days,
                )
            except Exception as e:
                logger.warning(f"Speed round answer processing failed: {e}")
                incorrect += 1

        total = correct + incorrect
        score_pct = round((correct / total * 100) if total > 0 else 0, 1)
        xp = correct * 10
        if total > 0 and (correct / total) >= 0.8:
            xp *= 2

        session = self.game_session_repo.update(
            session_id=session_id,
            is_completed=True,
            completed_at=now,
            score=correct,
            correct_answers=correct,
            incorrect_answers=incorrect,
            duration_seconds=duration_seconds,
            xp_earned=xp,
        )

        # Update daily activity
        try:
            activity = self.activity_repo.get_or_create_today(user_id=user_id)
            self.activity_repo.update(
                activity_id=activity.id,
                words_reviewed=activity.words_reviewed + total,
                correct_answers=activity.correct_answers + correct,
                incorrect_answers=activity.incorrect_answers + incorrect,
                xp_earned=activity.xp_earned + xp,
            )
        except Exception:
            pass

        return session


class StartWordMatchUseCase:
    """Start a word match game."""

    def __init__(self, word_repo, game_session_repo):
        self.word_repo = word_repo
        self.game_session_repo = game_session_repo

    def execute(self, user_id, pair_count=8):
        user_id = UUID(str(user_id))

        words, _ = self.word_repo.get_all_by_user(
            user_id=user_id, page=1, page_size=200
        )
        eligible = [w for w in words if w.translation]
        if len(eligible) < 5:
            raise ValidationError("You need at least 5 words with translations to play.")

        random.shuffle(eligible)
        selected = eligible[:min(pair_count, len(eligible))]

        word_items = [
            {"word_id": str(w.id), "word": w.original_word}
            for w in selected
        ]
        translations = [w.translation for w in selected]
        random.shuffle(translations)

        session = self.game_session_repo.create(
            user_id=user_id,
            game_type="word_match",
            max_score=len(selected),
        )

        return {
            "session_id": str(session.id),
            "words": word_items,
            "translations": translations,
            "pair_count": len(selected),
        }


class SubmitWordMatchUseCase:
    """Submit word match results."""

    def __init__(self, word_repo, game_session_repo, sr_service, activity_repo):
        self.word_repo = word_repo
        self.game_session_repo = game_session_repo
        self.sr_service = sr_service
        self.activity_repo = activity_repo

    def execute(self, session_id, user_id, pairs, time_seconds):
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        correct = 0
        incorrect = 0
        now = datetime.now(timezone.utc)

        for pair in pairs:
            word_id = UUID(str(pair["word_id"]))
            try:
                word = self.word_repo.get_by_id(word_id=word_id, user_id=user_id)
                is_right = pair.get("matched_translation", "").strip().lower() == word.translation.strip().lower()

                quality = 4 if is_right else 1
                self.sr_service.calculate_next_review(word, quality, now=now)
                word.review_count += 1
                if is_right:
                    word.correct_count += 1
                    correct += 1
                else:
                    word.incorrect_count += 1
                    incorrect += 1
                word.last_reviewed_at = now

                self.word_repo.update(
                    word_id=word.id, user_id=user_id,
                    confidence_score=word.confidence_score,
                    next_review_at=word.next_review_at,
                    review_count=word.review_count,
                    correct_count=word.correct_count,
                    incorrect_count=word.incorrect_count,
                    last_reviewed_at=word.last_reviewed_at,
                    is_mastered=word.is_mastered,
                    easiness_factor=word.easiness_factor,
                    repetition_number=word.repetition_number,
                    interval_days=word.interval_days,
                )
            except Exception as e:
                logger.warning(f"Word match pair processing failed: {e}")
                incorrect += 1

        total = correct + incorrect
        xp = correct * 10
        if total > 0 and (correct / total) >= 0.8:
            xp *= 2

        session = self.game_session_repo.update(
            session_id=session_id,
            is_completed=True,
            completed_at=now,
            score=correct,
            correct_answers=correct,
            incorrect_answers=incorrect,
            duration_seconds=time_seconds,
            xp_earned=xp,
        )

        # Update daily activity
        try:
            activity = self.activity_repo.get_or_create_today(user_id=user_id)
            self.activity_repo.update(
                activity_id=activity.id,
                words_reviewed=activity.words_reviewed + total,
                correct_answers=activity.correct_answers + correct,
                incorrect_answers=activity.incorrect_answers + incorrect,
                xp_earned=activity.xp_earned + xp,
            )
        except Exception:
            pass

        return session


class StartWordContextUseCase:
    """Start a word context game."""

    def __init__(self, word_repo, game_session_repo, ai_provider=None,
                 user_repo=None, prompt_template="", language_map=None):
        self.word_repo = word_repo
        self.game_session_repo = game_session_repo
        self.ai_provider = ai_provider
        self.user_repo = user_repo
        self.prompt_template = prompt_template
        self.language_map = language_map or {}

    def execute(self, user_id):
        user_id = UUID(str(user_id))

        words, _ = self.word_repo.get_all_by_user(
            user_id=user_id, page=1, page_size=200
        )
        eligible = [w for w in words if w.translation]
        if len(eligible) < 5:
            raise ValidationError("You need at least 5 words with translations to play.")

        random.shuffle(eligible)
        selected = eligible[:5]
        all_translations = [w.translation for w in words if w.translation]

        # Try AI generation
        questions = self._generate_ai_context(selected, user_id, all_translations)
        if not questions:
            questions = self._generate_fallback_context(selected, all_translations)

        session = self.game_session_repo.create(
            user_id=user_id,
            game_type="word_context",
            max_score=len(questions),
        )

        return {
            "session_id": str(session.id),
            "questions": questions,
        }

    def _generate_ai_context(self, words, user_id, all_translations):
        """Try generating context via AI."""
        if not self.ai_provider or not self.ai_provider.is_available():
            return []

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

        words_list = ", ".join(w.original_word for w in words)

        try:
            if not self.prompt_template:
                return []
            prompt = self.prompt_template.format(
                native_language=native_lang,
                proficiency_level=proficiency,
                words_list=words_list,
            )
            result = self.ai_provider.generate_json(prompt=prompt, max_tokens=2000)
            if not isinstance(result, list):
                return []

            questions = []
            word_map = {w.original_word.lower(): w for w in words}
            for item in result[:5]:
                word_key = item.get("word", "").lower()
                word_entity = word_map.get(word_key, words[len(questions) % len(words)])
                questions.append({
                    "word_id": str(word_entity.id),
                    "context": item.get("context", ""),
                    "correct_answer": item.get("correct_answer", word_entity.original_word),
                    "options": item.get("options", []),
                })
            return questions
        except Exception as e:
            logger.warning(f"AI context generation failed: {e}")
            return []

    def _generate_fallback_context(self, words, all_translations):
        """Generate context questions from example sentences."""
        questions = []
        for word in words:
            if word.example_sentence:
                context = word.example_sentence.replace(
                    word.original_word, "___"
                ).replace(
                    word.original_word.capitalize(), "___"
                )
            else:
                context = f'"___" means "{word.translation}"'

            correct = word.original_word
            other_words = [w.original_word for w in words if w.id != word.id]
            random.shuffle(other_words)
            options = [correct] + other_words[:3]
            while len(options) < 4:
                options.append(f"word_{len(options)}")
            random.shuffle(options)

            questions.append({
                "word_id": str(word.id),
                "context": context,
                "correct_answer": correct,
                "options": options,
            })
        return questions


class SubmitWordContextUseCase:
    """Submit word context game results."""

    def __init__(self, word_repo, game_session_repo, sr_service, activity_repo):
        self.word_repo = word_repo
        self.game_session_repo = game_session_repo
        self.sr_service = sr_service
        self.activity_repo = activity_repo

    def execute(self, session_id, user_id, answers):
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        correct = 0
        incorrect = 0
        now = datetime.now(timezone.utc)

        for ans in answers:
            word_id = UUID(str(ans["word_id"]))
            try:
                word = self.word_repo.get_by_id(word_id=word_id, user_id=user_id)
                is_right = ans.get("selected_answer", "").strip().lower() == word.original_word.strip().lower()

                quality = 4 if is_right else 1
                self.sr_service.calculate_next_review(word, quality, now=now)
                word.review_count += 1
                if is_right:
                    word.correct_count += 1
                    correct += 1
                else:
                    word.incorrect_count += 1
                    incorrect += 1
                word.last_reviewed_at = now

                self.word_repo.update(
                    word_id=word.id, user_id=user_id,
                    confidence_score=word.confidence_score,
                    next_review_at=word.next_review_at,
                    review_count=word.review_count,
                    correct_count=word.correct_count,
                    incorrect_count=word.incorrect_count,
                    last_reviewed_at=word.last_reviewed_at,
                    is_mastered=word.is_mastered,
                    easiness_factor=word.easiness_factor,
                    repetition_number=word.repetition_number,
                    interval_days=word.interval_days,
                )
            except Exception as e:
                logger.warning(f"Word context answer failed: {e}")
                incorrect += 1

        total = correct + incorrect
        xp = correct * 10
        if total > 0 and (correct / total) >= 0.8:
            xp *= 2

        session = self.game_session_repo.update(
            session_id=session_id,
            is_completed=True,
            completed_at=now,
            score=correct,
            correct_answers=correct,
            incorrect_answers=incorrect,
            xp_earned=xp,
        )

        # Update daily activity
        try:
            activity = self.activity_repo.get_or_create_today(user_id=user_id)
            self.activity_repo.update(
                activity_id=activity.id,
                words_reviewed=activity.words_reviewed + total,
                correct_answers=activity.correct_answers + correct,
                incorrect_answers=activity.incorrect_answers + incorrect,
                xp_earned=activity.xp_earned + xp,
            )
        except Exception:
            pass

        return session


class GetGameHistoryUseCase:
    """Get game session history."""

    def __init__(self, game_session_repo):
        self.game_session_repo = game_session_repo

    def execute(self, user_id, page=1, page_size=20):
        user_id = UUID(str(user_id))
        return self.game_session_repo.get_by_user(
            user_id=user_id, page=page, page_size=page_size
        )


class GetGameStatsUseCase:
    """Get game stats for a user."""

    def __init__(self, game_session_repo):
        self.game_session_repo = game_session_repo

    def execute(self, user_id):
        user_id = UUID(str(user_id))
        return self.game_session_repo.get_stats(user_id=user_id)
