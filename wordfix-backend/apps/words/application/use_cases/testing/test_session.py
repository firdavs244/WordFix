"""
Test session management use cases — submit answers, complete session, history, detail.
"""

import logging
from datetime import datetime, timezone
from uuid import UUID

logger = logging.getLogger(__name__)


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

        # Record mistake pattern (adaptive intelligence)
        if not is_correct and answer:
            try:
                from apps.users.presentation.learning_deps import get_record_mistake_use_case
                mistake_uc = get_record_mistake_use_case()
                mistake_uc.execute(user_id, answer, question.correct_answer, context="test")
            except Exception as e:
                logger.warning(f"Mistake pattern recording failed: {e}")

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
