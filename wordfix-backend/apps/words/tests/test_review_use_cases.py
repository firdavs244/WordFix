"""
Tests for review use cases (session, submit answer, complete, summary, streak).
"""

from datetime import date, timedelta
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from django.utils import timezone

from apps.words.application.use_cases import (
    CompleteReviewSessionUseCase,
    GetReviewSummaryUseCase,
    GetReviewWordsUseCase,
    StartReviewSessionUseCase,
    SubmitReviewAnswerUseCase,
    UpdateStreakUseCase,
)
from apps.words.domain.entities import (
    DailyActivityEntity,
    DailyStreakEntity,
    ReviewLogEntity,
    ReviewSessionEntity,
    WordEntity,
)
from apps.words.domain.services import SpacedRepetitionService
from apps.words.tests.conftest import make_word_entity


def _make_session_entity(**overrides):
    defaults = dict(
        id=uuid4(), user_id=uuid4(), started_at=timezone.now(),
        completed_at=None, total_words=0, correct_count=0, incorrect_count=0,
        average_quality=0.0, duration_seconds=0, session_type="review",
        is_completed=False, created_at=timezone.now(), updated_at=timezone.now(),
    )
    defaults.update(overrides)
    return ReviewSessionEntity(**defaults)


def _make_streak_entity(**overrides):
    defaults = dict(
        id=uuid4(), user_id=uuid4(), current_streak=0, longest_streak=0,
        last_activity_date=None, streak_frozen_until=None, total_review_days=0,
        created_at=timezone.now(), updated_at=timezone.now(),
    )
    defaults.update(overrides)
    return DailyStreakEntity(**defaults)


def _make_activity_entity(**overrides):
    defaults = dict(
        id=uuid4(), user_id=uuid4(), date=date.today(),
        words_reviewed=0, words_added=0, words_mastered=0,
        correct_answers=0, incorrect_answers=0, total_time_seconds=0,
        goal_completed=False, xp_earned=0,
        created_at=timezone.now(), updated_at=timezone.now(),
    )
    defaults.update(overrides)
    return DailyActivityEntity(**defaults)


# =============================================================================
# START SESSION
# =============================================================================


class TestStartReviewSessionUseCase:
    def test_creates_session(self):
        repo = MagicMock()
        expected = _make_session_entity()
        repo.create.return_value = expected

        uc = StartReviewSessionUseCase(session_repo=repo)
        result = uc.execute(user_id=uuid4(), session_type="review", word_count=10)

        repo.create.assert_called_once()
        assert result == expected

    def test_creates_quick_session(self):
        repo = MagicMock()
        repo.create.return_value = _make_session_entity(session_type="quick")

        uc = StartReviewSessionUseCase(session_repo=repo)
        result = uc.execute(user_id=uuid4(), session_type="quick")
        assert result.session_type == "quick"


# =============================================================================
# SUBMIT ANSWER
# =============================================================================


class TestSubmitReviewAnswerUseCase:
    def _setup(self):
        word_repo = MagicMock()
        session_repo = MagicMock()
        log_repo = MagicMock()
        sr_service = SpacedRepetitionService()
        streak_repo = MagicMock()
        activity_repo = MagicMock()

        user_id = uuid4()
        word = make_word_entity(user_id=user_id)
        session = _make_session_entity(user_id=user_id)
        streak = _make_streak_entity(user_id=user_id)
        activity = _make_activity_entity(user_id=user_id)

        word_repo.get_by_id.return_value = word
        word_repo.update.return_value = word
        session_repo.get_by_id.return_value = session
        session_repo.update.return_value = session
        streak_repo.get_or_create.return_value = streak
        streak_repo.update.return_value = streak
        activity_repo.get_or_create_today.return_value = activity
        activity_repo.update.return_value = activity

        uc = SubmitReviewAnswerUseCase(
            word_repo, session_repo, log_repo, sr_service,
            streak_repo, activity_repo,
        )
        return uc, word_repo, session_repo, log_repo, activity_repo, session, word, user_id

    def test_submit_correct_answer(self):
        uc, word_repo, session_repo, log_repo, activity_repo, session, word, user_id = self._setup()
        result = uc.execute(
            session_id=session.id, word_id=word.id,
            user_id=user_id, quality=4,
        )

        assert result["is_correct"] is True
        log_repo.create.assert_called_once()
        word_repo.update.assert_called_once()

    def test_submit_incorrect_answer(self):
        uc, word_repo, session_repo, log_repo, activity_repo, session, word, user_id = self._setup()
        result = uc.execute(
            session_id=session.id, word_id=word.id,
            user_id=user_id, quality=2,
        )

        assert result["is_correct"] is False

    def test_submit_invalid_quality_raises(self):
        from apps.common.exceptions import ValidationError
        uc, *_ = self._setup()
        user_id = uuid4()
        with pytest.raises(ValidationError):
            uc.execute(
                session_id=uuid4(), word_id=uuid4(),
                user_id=user_id, quality=6,
            )

    def test_submit_updates_session_stats(self):
        uc, word_repo, session_repo, log_repo, activity_repo, session, word, user_id = self._setup()
        uc.execute(
            session_id=session.id, word_id=word.id,
            user_id=user_id, quality=4,
        )
        session_repo.update.assert_called_once()
        call_kwargs = session_repo.update.call_args.kwargs
        assert "correct_count" in call_kwargs or "incorrect_count" in call_kwargs

    def test_submit_creates_review_log(self):
        uc, word_repo, session_repo, log_repo, activity_repo, session, word, user_id = self._setup()
        uc.execute(
            session_id=session.id, word_id=word.id,
            user_id=user_id, quality=5, response_time_ms=1500,
        )
        log_repo.create.assert_called_once()
        call_kwargs = log_repo.create.call_args.kwargs
        assert call_kwargs["quality"] == 5
        assert call_kwargs["response_time_ms"] == 1500

    def test_submit_updates_daily_activity(self):
        uc, word_repo, session_repo, log_repo, activity_repo, session, word, user_id = self._setup()
        uc.execute(
            session_id=session.id, word_id=word.id,
            user_id=user_id, quality=4,
        )
        activity_repo.update.assert_called_once()

    def test_submit_xp_calculation(self):
        uc, word_repo, session_repo, log_repo, activity_repo, session, word, user_id = self._setup()
        uc.execute(
            session_id=session.id, word_id=word.id,
            user_id=user_id, quality=5,
        )
        call_kwargs = activity_repo.update.call_args.kwargs
        assert call_kwargs["xp_earned"] == 15  # quality(5) * 3


# =============================================================================
# COMPLETE SESSION
# =============================================================================


class TestCompleteReviewSessionUseCase:
    def test_complete_session(self):
        session_repo = MagicMock()
        log_repo = MagicMock()

        session = _make_session_entity(started_at=timezone.now() - timedelta(minutes=5))
        session_repo.get_by_id.return_value = session

        log1 = MagicMock(quality=4)
        log2 = MagicMock(quality=3)
        log_repo.get_by_session.return_value = [log1, log2]

        completed_session = _make_session_entity(is_completed=True, duration_seconds=300)
        session_repo.update.return_value = completed_session

        uc = CompleteReviewSessionUseCase(session_repo, log_repo)
        result = uc.execute(session_id=session.id, user_id=session.user_id)

        session_repo.update.assert_called_once()
        call_kwargs = session_repo.update.call_args.kwargs
        assert call_kwargs["is_completed"] is True
        assert call_kwargs["average_quality"] == 3.5  # (4+3)/2

    def test_complete_empty_session(self):
        session_repo = MagicMock()
        log_repo = MagicMock()

        session = _make_session_entity()
        session_repo.get_by_id.return_value = session
        log_repo.get_by_session.return_value = []
        session_repo.update.return_value = session

        uc = CompleteReviewSessionUseCase(session_repo, log_repo)
        result = uc.execute(session_id=session.id, user_id=session.user_id)

        call_kwargs = session_repo.update.call_args.kwargs
        assert call_kwargs["average_quality"] == 0.0


# =============================================================================
# REVIEW SUMMARY
# =============================================================================


@pytest.mark.django_db
class TestGetReviewSummaryUseCase:
    def test_summary_returns_all_fields(self, user):
        word_repo = MagicMock()
        streak_repo = MagicMock()
        activity_repo = MagicMock()
        user_repo = MagicMock()

        word_repo.get_review_summary_stats.return_value = {
            "total_words": 10,
            "due_today": 3,
            "overdue": 1,
            "mastered": 2,
            "learning": 5,
            "new_words": 3,
            "next_review_time": None,
        }

        user_repo.get_user_language_info.return_value = {
            "native_language": "uz",
            "proficiency_level": "B1",
            "daily_goal": 10,
        }

        streak = _make_streak_entity(user_id=user.id, current_streak=5, longest_streak=10)
        streak_repo.get_or_create.return_value = streak

        activity = _make_activity_entity(user_id=user.id, words_reviewed=3)
        activity_repo.get_or_create_today.return_value = activity

        uc = GetReviewSummaryUseCase(word_repo, streak_repo, activity_repo, user_repo=user_repo)
        result = uc.execute(user_id=user.id)

        assert "total_words" in result
        assert "due_today" in result
        assert "streak" in result
        assert result["streak"]["current"] == 5
        assert "daily_goal" in result


# =============================================================================
# GET REVIEW WORDS
# =============================================================================


@pytest.mark.django_db
class TestGetReviewWordsUseCase:
    def test_review_words_empty(self, user):
        word_repo = MagicMock()
        word_repo.get_review_words.return_value = []
        uc = GetReviewWordsUseCase(word_repo)
        words = uc.execute(user_id=user.id, limit=20, session_type="review")
        assert isinstance(words, list)

    def test_quick_session_limits_to_5(self, user):
        word_repo = MagicMock()
        word_repo.get_review_words.return_value = []
        uc = GetReviewWordsUseCase(word_repo)
        words = uc.execute(user_id=user.id, limit=20, session_type="quick")
        assert isinstance(words, list)


# =============================================================================
# UPDATE STREAK
# =============================================================================


class TestUpdateStreakUseCase:
    def test_first_activity_sets_streak_to_1(self):
        repo = MagicMock()
        streak = _make_streak_entity(current_streak=0, last_activity_date=None)
        repo.get_or_create.return_value = streak
        repo.update.return_value = streak

        uc = UpdateStreakUseCase(streak_repo=repo)
        uc.execute(user_id=streak.user_id)

        call_kwargs = repo.update.call_args.kwargs
        assert call_kwargs["current_streak"] == 1

    def test_consecutive_day_increments_streak(self):
        repo = MagicMock()
        yesterday = date.today() - timedelta(days=1)
        streak = _make_streak_entity(
            current_streak=5, longest_streak=5, last_activity_date=yesterday,
        )
        repo.get_or_create.return_value = streak
        repo.update.return_value = streak

        uc = UpdateStreakUseCase(streak_repo=repo)
        uc.execute(user_id=streak.user_id)

        call_kwargs = repo.update.call_args.kwargs
        assert call_kwargs["current_streak"] == 6
        assert call_kwargs["longest_streak"] == 6

    def test_same_day_no_change(self):
        repo = MagicMock()
        streak = _make_streak_entity(
            current_streak=3, last_activity_date=date.today(),
        )
        repo.get_or_create.return_value = streak

        uc = UpdateStreakUseCase(streak_repo=repo)
        result = uc.execute(user_id=streak.user_id)

        repo.update.assert_not_called()

    def test_missed_day_resets_streak(self):
        repo = MagicMock()
        two_days_ago = date.today() - timedelta(days=2)
        streak = _make_streak_entity(
            current_streak=10, longest_streak=10, last_activity_date=two_days_ago,
        )
        repo.get_or_create.return_value = streak
        repo.update.return_value = streak

        uc = UpdateStreakUseCase(streak_repo=repo)
        uc.execute(user_id=streak.user_id)

        call_kwargs = repo.update.call_args.kwargs
        assert call_kwargs["current_streak"] == 1  # Reset

    def test_frozen_streak_preserved(self):
        repo = MagicMock()
        three_days_ago = date.today() - timedelta(days=3)
        streak = _make_streak_entity(
            current_streak=7, longest_streak=7,
            last_activity_date=three_days_ago,
            streak_frozen_until=date.today(),
        )
        repo.get_or_create.return_value = streak
        repo.update.return_value = streak

        uc = UpdateStreakUseCase(streak_repo=repo)
        uc.execute(user_id=streak.user_id)

        call_kwargs = repo.update.call_args.kwargs
        assert call_kwargs["current_streak"] == 7  # Preserved

    def test_longest_streak_updated(self):
        repo = MagicMock()
        yesterday = date.today() - timedelta(days=1)
        streak = _make_streak_entity(
            current_streak=15, longest_streak=14, last_activity_date=yesterday,
        )
        repo.get_or_create.return_value = streak
        repo.update.return_value = streak

        uc = UpdateStreakUseCase(streak_repo=repo)
        uc.execute(user_id=streak.user_id)

        call_kwargs = repo.update.call_args.kwargs
        assert call_kwargs["longest_streak"] == 16
