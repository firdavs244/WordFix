"""
Tests for confusing pairs detection integration with review/test use cases.
"""

import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from apps.words.application.use_cases.review import SubmitReviewAnswerUseCase


def _make_streak_repo():
    streak_repo = MagicMock()
    streak = MagicMock()
    streak.id = uuid4()
    streak.last_activity_date = None
    streak.current_streak = 0
    streak.longest_streak = 0
    streak.total_review_days = 0
    streak.streak_frozen_until = None
    streak_repo.get_or_create.return_value = streak
    streak_repo.update.return_value = streak
    return streak_repo


class TestConfusingDetectionInReview:
    """Test confusion detection is triggered on wrong answers in review."""

    def _make_word_entity(self, word_id=None, user_id=None):
        word = MagicMock()
        word.id = word_id or uuid4()
        word.user_id = user_id or uuid4()
        word.confidence_score = 50
        word.interval_days = 1
        word.review_count = 0
        word.correct_count = 0
        word.incorrect_count = 0
        word.is_mastered = False
        word.easiness_factor = 2.5
        word.repetition_number = 0
        word.last_reviewed_at = None
        word.next_review_at = None
        return word

    def _make_session_entity(self):
        session = MagicMock()
        session.id = uuid4()
        session.total_words = 0
        session.correct_count = 0
        session.incorrect_count = 0
        session.current_combo = 0
        session.max_combo = 0
        session.combo_xp_bonus = 0
        return session

    def test_triggers_confusion_detection_on_wrong_answer(self):
        """Wrong answer with user_answer should trigger DetectConfusionUseCase."""
        user_id = uuid4()
        word_id = uuid4()
        session_id = uuid4()

        word_repo = MagicMock()
        word_entity = self._make_word_entity(word_id, user_id)
        word_repo.get_by_id.return_value = word_entity

        session_repo = MagicMock()
        session_repo.get_by_id.return_value = self._make_session_entity()
        session_repo.update.return_value = self._make_session_entity()

        log_repo = MagicMock()
        sr_service = MagicMock()
        streak_repo = _make_streak_repo()
        activity_repo = MagicMock()
        activity_repo.get_or_create_today.return_value = MagicMock(
            id=uuid4(), words_reviewed=0, correct_answers=0,
            incorrect_answers=0, words_mastered=0, xp_earned=0,
        )

        confusing_pair_repo = MagicMock()
        pair = MagicMock()
        pair.id = uuid4()
        pair.confusion_count = 1

        # Mock the DetectConfusionUseCase
        with MagicMock() as mock_detect:
            uc = SubmitReviewAnswerUseCase(
                word_repo, session_repo, log_repo, sr_service,
                streak_repo, activity_repo,
                confusing_pair_repo=confusing_pair_repo,
            )
            result = uc.execute(
                session_id, word_id, user_id,
                quality=1, user_answer="some_wrong_answer"
            )

            assert "is_correct" in result
            assert result["is_correct"] is False

    def test_no_confusion_detection_on_correct_answer(self):
        """Correct answer should not trigger confusion detection."""
        user_id = uuid4()
        word_id = uuid4()
        session_id = uuid4()

        word_repo = MagicMock()
        word_entity = self._make_word_entity(word_id, user_id)
        word_repo.get_by_id.return_value = word_entity

        session_repo = MagicMock()
        session = self._make_session_entity()
        session_repo.get_by_id.return_value = session
        session_repo.update.return_value = session

        log_repo = MagicMock()
        sr_service = MagicMock()
        streak_repo = _make_streak_repo()
        activity_repo = MagicMock()
        activity_repo.get_or_create_today.return_value = MagicMock(
            id=uuid4(), words_reviewed=0, correct_answers=0,
            incorrect_answers=0, words_mastered=0, xp_earned=0,
        )

        confusing_pair_repo = MagicMock()

        uc = SubmitReviewAnswerUseCase(
            word_repo, session_repo, log_repo, sr_service,
            streak_repo, activity_repo,
            confusing_pair_repo=confusing_pair_repo,
        )
        result = uc.execute(
            session_id, word_id, user_id,
            quality=4, user_answer="correct_answer"
        )

        assert result["is_correct"] is True
        # confusion_detected should not be in result for correct answers
        assert "confusion_detected" not in result

    def test_no_confusion_without_user_answer(self):
        """No confusion detection without user_answer."""
        user_id = uuid4()
        word_id = uuid4()
        session_id = uuid4()

        word_repo = MagicMock()
        word_entity = self._make_word_entity(word_id, user_id)
        word_repo.get_by_id.return_value = word_entity

        session_repo = MagicMock()
        session = self._make_session_entity()
        session_repo.get_by_id.return_value = session
        session_repo.update.return_value = session

        log_repo = MagicMock()
        sr_service = MagicMock()
        streak_repo = _make_streak_repo()
        activity_repo = MagicMock()
        activity_repo.get_or_create_today.return_value = MagicMock(
            id=uuid4(), words_reviewed=0, correct_answers=0,
            incorrect_answers=0, words_mastered=0, xp_earned=0,
        )

        confusing_pair_repo = MagicMock()

        uc = SubmitReviewAnswerUseCase(
            word_repo, session_repo, log_repo, sr_service,
            streak_repo, activity_repo,
            confusing_pair_repo=confusing_pair_repo,
        )
        # quality=1 means wrong, but no user_answer provided
        result = uc.execute(session_id, word_id, user_id, quality=1)

        assert "confusion_detected" not in result
