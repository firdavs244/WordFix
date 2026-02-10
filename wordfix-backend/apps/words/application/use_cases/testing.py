"""
Test generation and submission use cases.
"""

import logging
import random
from datetime import datetime, timezone
from uuid import UUID

from apps.common.exceptions import ValidationError
from core.interfaces.ai_provider import AIProviderError

logger = logging.getLogger(__name__)


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

    def __init__(self, question_repo, word_repo, sr_service, activity_repo,
                 test_session_repo=None, confusing_pair_repo=None,
                 challenge_repo=None, xp_service=None):
        self.question_repo = question_repo
        self.word_repo = word_repo
        self.sr_service = sr_service
        self.activity_repo = activity_repo
        self.test_session_repo = test_session_repo
        self.confusing_pair_repo = confusing_pair_repo
        self.challenge_repo = challenge_repo
        self.xp_service = xp_service

    def execute(self, question_id, user_id, answer: str, response_time_ms: int = 0,
                session_id=None):
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

        # Combo tracking on test session
        combo_info = None
        if session_id and self.test_session_repo:
            try:
                sid = UUID(str(session_id))
                session = self.test_session_repo.get_by_id(session_id=sid, user_id=user_id)
                from apps.words.domain.services import ComboService
                update_data = {}
                if is_correct:
                    new_combo = session.current_combo + 1
                    update_data["current_combo"] = new_combo
                    if new_combo > session.max_combo:
                        update_data["max_combo"] = new_combo
                    combo_xp, multiplier = ComboService.calculate_combo_xp(5, new_combo)
                    combo_bonus = combo_xp - 5
                    update_data["combo_xp_bonus"] = session.combo_xp_bonus + combo_bonus
                    combo_info = {"current": new_combo, "multiplier": multiplier}
                else:
                    update_data["current_combo"] = 0
                    combo_info = {"current": 0, "multiplier": 1.0}
                self.test_session_repo.update(session_id=sid, **update_data)
            except Exception as e:
                logger.warning(f"Test combo tracking failed: {e}")

        # Confusion detection
        confusion_detected = None
        if not is_correct and answer and self.confusing_pair_repo:
            try:
                from apps.words.application.use_cases.confusing_pairs import DetectConfusionUseCase
                detect_uc = DetectConfusionUseCase(self.word_repo, self.confusing_pair_repo)
                confusion_detected = detect_uc.execute(user_id, question.word_id, answer)
            except Exception as e:
                logger.warning(f"Test confusion detection failed: {e}")

        result = {
            "is_correct": is_correct,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation,
        }
        if combo_info:
            result["combo"] = combo_info
        if confusion_detected:
            result["confusion_detected"] = {
                "pair_id": str(confusion_detected.id),
                "confusion_count": confusion_detected.confusion_count,
            }
        return result


class CompleteTestSessionUseCase:
    """Complete a test session and calculate results."""

    def __init__(self, test_session_repo, test_question_repo, activity_repo,
                 challenge_repo=None, xp_service=None):
        self.test_session_repo = test_session_repo
        self.test_question_repo = test_question_repo
        self.activity_repo = activity_repo
        self.challenge_repo = challenge_repo
        self.xp_service = xp_service

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

        # Update daily challenge progress
        if self.challenge_repo:
            try:
                from apps.words.application.use_cases.daily_challenges import UpdateChallengeProgressUseCase
                challenge_uc = UpdateChallengeProgressUseCase(
                    self.challenge_repo, self.xp_service
                )
                challenge_uc.execute(user_id, "complete_test", amount=1)
            except Exception as e:
                logger.warning(f"Test challenge progress update failed: {e}")

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
