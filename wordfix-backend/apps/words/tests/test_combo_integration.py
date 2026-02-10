"""
Tests for combo integration with review/test/game sessions.
"""

import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4
from datetime import datetime, date, timezone

from apps.words.application.use_cases.review import SubmitReviewAnswerUseCase
from apps.words.domain.services import ComboService


def _make_streak_repo():
    """Create a streak repo mock with proper streak entity."""
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


class TestReviewComboIntegration:
    """Test combo tracking within review use case."""

    def _make_word_entity(self, word_id=None, user_id=None):
        """Build a mock word entity."""
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

    def _make_session_entity(self, session_id=None, user_id=None):
        """Build a mock session entity."""
        session = MagicMock()
        session.id = session_id or uuid4()
        session.user_id = user_id or uuid4()
        session.total_words = 0
        session.correct_count = 0
        session.incorrect_count = 0
        session.current_combo = 0
        session.max_combo = 0
        session.combo_xp_bonus = 0
        return session

    def test_correct_answer_increments_combo(self):
        """Correct answer should increment current_combo."""
        user_id = uuid4()
        session_id = uuid4()
        word_id = uuid4()

        word_repo = MagicMock()
        word_repo.get_by_id.return_value = self._make_word_entity(word_id, user_id)

        session = self._make_session_entity(session_id, user_id)
        session_repo = MagicMock()
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

        uc = SubmitReviewAnswerUseCase(
            word_repo, session_repo, log_repo, sr_service,
            streak_repo, activity_repo,
        )
        result = uc.execute(session_id, word_id, user_id, quality=4)

        # Should have updated session with combo
        update_call = session_repo.update.call_args
        assert update_call.kwargs.get("current_combo") == 1

    def test_incorrect_answer_resets_combo(self):
        """Incorrect answer should reset combo to 0."""
        user_id = uuid4()
        session_id = uuid4()
        word_id = uuid4()

        word_repo = MagicMock()
        word_repo.get_by_id.return_value = self._make_word_entity(word_id, user_id)

        session = self._make_session_entity(session_id, user_id)
        session.current_combo = 5  # Had a combo going
        session_repo = MagicMock()
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

        uc = SubmitReviewAnswerUseCase(
            word_repo, session_repo, log_repo, sr_service,
            streak_repo, activity_repo,
        )
        result = uc.execute(session_id, word_id, user_id, quality=1)

        update_call = session_repo.update.call_args
        assert update_call.kwargs.get("current_combo") == 0

    def test_combo_result_included_in_response(self):
        """Response should include combo info."""
        user_id = uuid4()
        session_id = uuid4()
        word_id = uuid4()

        word_repo = MagicMock()
        word_repo.get_by_id.return_value = self._make_word_entity(word_id, user_id)

        session = self._make_session_entity(session_id, user_id)
        session_repo = MagicMock()
        session_repo.get_by_id.return_value = session
        updated_session = self._make_session_entity(session_id, user_id)
        updated_session.current_combo = 1
        updated_session.max_combo = 1
        session_repo.update.return_value = updated_session

        log_repo = MagicMock()
        sr_service = MagicMock()
        streak_repo = _make_streak_repo()
        activity_repo = MagicMock()
        activity_repo.get_or_create_today.return_value = MagicMock(
            id=uuid4(), words_reviewed=0, correct_answers=0,
            incorrect_answers=0, words_mastered=0, xp_earned=0,
        )

        uc = SubmitReviewAnswerUseCase(
            word_repo, session_repo, log_repo, sr_service,
            streak_repo, activity_repo,
        )
        result = uc.execute(session_id, word_id, user_id, quality=4)

        assert "combo" in result
        assert "current" in result["combo"]
        assert "max" in result["combo"]
        assert "multiplier" in result["combo"]

    def test_max_combo_tracked(self):
        """Max combo should update when current exceeds it."""
        user_id = uuid4()
        session_id = uuid4()
        word_id = uuid4()

        word_repo = MagicMock()
        word_repo.get_by_id.return_value = self._make_word_entity(word_id, user_id)

        session = self._make_session_entity(session_id, user_id)
        session.current_combo = 4
        session.max_combo = 4
        session_repo = MagicMock()
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

        uc = SubmitReviewAnswerUseCase(
            word_repo, session_repo, log_repo, sr_service,
            streak_repo, activity_repo,
        )
        result = uc.execute(session_id, word_id, user_id, quality=5)

        update_call = session_repo.update.call_args
        assert update_call.kwargs.get("current_combo") == 5
        assert update_call.kwargs.get("max_combo") == 5
