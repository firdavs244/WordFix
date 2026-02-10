"""
Tests for daily challenge integration with use cases.
"""

import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from apps.words.application.use_cases.review import (
    SubmitReviewAnswerUseCase,
    CompleteReviewSessionUseCase,
)
from apps.words.application.use_cases.testing import CompleteTestSessionUseCase


class TestChallengeProgressInReview:
    """Test challenge progress updates during review."""

    def _make_word_entity(self):
        word = MagicMock()
        word.id = uuid4()
        word.confidence_score = 50
        word.interval_days = 1
        word.review_count = 0
        word.correct_count = 0
        word.incorrect_count = 0
        word.is_mastered = False
        word.easiness_factor = 2.5
        word.repetition_number = 0
        return word

    def _make_session(self):
        session = MagicMock()
        session.id = uuid4()
        session.total_words = 0
        session.correct_count = 0
        session.incorrect_count = 0
        session.current_combo = 0
        session.max_combo = 0
        session.combo_xp_bonus = 0
        return session

    def test_review_answer_updates_challenge_progress(self):
        """Submitting review answer should update review_words challenge."""
        user_id = uuid4()
        word_repo = MagicMock()
        word_repo.get_by_id.return_value = self._make_word_entity()

        session_repo = MagicMock()
        session_repo.get_by_id.return_value = self._make_session()
        session_repo.update.return_value = self._make_session()

        log_repo = MagicMock()
        sr_service = MagicMock()
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
        activity_repo = MagicMock()
        activity_repo.get_or_create_today.return_value = MagicMock(
            id=uuid4(), words_reviewed=0, correct_answers=0,
            incorrect_answers=0, words_mastered=0, xp_earned=0,
        )

        challenge_repo = MagicMock()
        challenge_entity = MagicMock()
        challenge_entity.challenges = [
            {"type": "review_words", "target": 5, "current": 0,
             "completed": False, "xp_reward": 20},
        ]
        challenge_entity.all_completed = False
        challenge_entity.id = uuid4()
        challenge_repo.get_or_create_today.return_value = (challenge_entity, False)
        challenge_repo.update.return_value = challenge_entity

        uc = SubmitReviewAnswerUseCase(
            word_repo, session_repo, log_repo, sr_service,
            streak_repo, activity_repo,
            challenge_repo=challenge_repo,
        )
        uc.execute(uuid4(), uuid4(), user_id, quality=4)

        # Challenge repo should have been called
        challenge_repo.get_or_create_today.assert_called_once()


class TestChallengeProgressInTestComplete:
    """Test challenge progress on test completion."""

    def test_complete_test_updates_challenge(self):
        """Completing a test should update complete_test challenge."""
        user_id = uuid4()
        session_id = uuid4()

        session = MagicMock()
        session.id = session_id
        session.started_at = MagicMock()
        session.total_words = 5

        test_session_repo = MagicMock()
        test_session_repo.get_by_id.return_value = session
        test_session_repo.update.return_value = session

        test_question_repo = MagicMock()
        test_question_repo.get_by_session.return_value = [
            MagicMock(is_correct=True),
            MagicMock(is_correct=True),
            MagicMock(is_correct=False),
        ]

        activity_repo = MagicMock()
        activity_repo.get_or_create_today.return_value = MagicMock(
            id=uuid4(), words_reviewed=0, correct_answers=0,
            incorrect_answers=0, xp_earned=0,
        )

        challenge_repo = MagicMock()
        challenge_entity = MagicMock()
        challenge_entity.challenges = [
            {"type": "complete_test", "target": 1, "current": 0,
             "completed": False, "xp_reward": 25},
        ]
        challenge_entity.all_completed = False
        challenge_entity.id = uuid4()
        challenge_repo.get_or_create_today.return_value = (challenge_entity, False)
        challenge_repo.update.return_value = challenge_entity

        uc = CompleteTestSessionUseCase(
            test_session_repo, test_question_repo, activity_repo,
            challenge_repo=challenge_repo,
        )
        uc.execute(session_id, user_id)

        challenge_repo.get_or_create_today.assert_called_once()
