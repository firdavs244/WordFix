"""
Tests for Word ORM models: Word, WordCategory, ReviewSession, ReviewLog,
DailyStreak, DailyActivity.
"""

import uuid
from datetime import date, timedelta

import pytest
from django.utils import timezone

from apps.users.infrastructure.models import CustomUser
from apps.words.infrastructure.models import (
    DailyActivity,
    DailyStreak,
    ReviewLog,
    ReviewSession,
    Word,
    WordCategory,
)


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def model_user(db):
    return CustomUser.objects.create_user(
        email="model_test@example.com",
        username="modeltest",
        password="testpass123",
    )


@pytest.fixture
def model_word(model_user):
    return Word.objects.create(
        user=model_user,
        original_word="test_word",
        translation="test_tarjima",
        difficulty_level="medium",
    )


# =============================================================================
# WORD MODEL TESTS
# =============================================================================


@pytest.mark.django_db
class TestWordModel:
    def test_create_word(self, user):
        word = Word.objects.create(
            user=user, original_word="Test", translation="Test_uz"
        )
        assert word.original_word == "test"  # lowercased
        assert word.translation == "Test_uz"

    def test_uuid_pk(self, sample_word):
        assert isinstance(sample_word.id, uuid.UUID)

    def test_str(self, sample_word):
        assert str(sample_word) == sample_word.original_word

    def test_default_difficulty(self, user):
        word = Word.objects.create(user=user, original_word="abc")
        assert word.difficulty_level == "medium"

    def test_accuracy_rate(self, sample_word):
        sample_word.review_count = 10
        sample_word.correct_count = 8
        sample_word.save()
        assert sample_word.accuracy_rate == 80.0

    def test_accuracy_rate_zero(self, sample_word):
        assert sample_word.accuracy_rate == 0.0

    def test_unique_together(self, user, sample_word):
        with pytest.raises(Exception):
            Word.objects.create(user=user, original_word=sample_word.original_word)

    def test_save_lowercases_word(self, user):
        word = Word.objects.create(user=user, original_word="UPPERCASE")
        assert word.original_word == "uppercase"

    def test_json_fields_default(self, user):
        word = Word.objects.create(user=user, original_word="json_test")
        assert word.synonyms == []
        assert word.antonyms == []
        assert word.tags == []

    def test_category_nullable(self, user):
        word = Word.objects.create(user=user, original_word="no_cat")
        assert word.category is None

    def test_cascade_delete_user(self, user, sample_word):
        user.delete()
        assert not Word.objects.filter(id=sample_word.id).exists()


# =============================================================================
# WORD NEW FIELDS
# =============================================================================


@pytest.mark.django_db
class TestWordNewFields:
    def test_enrichment_status_default(self, model_word):
        assert model_word.enrichment_status == "pending"

    def test_mnemonic_default(self, model_word):
        assert model_word.mnemonic == ""

    def test_usage_notes_default(self, model_word):
        assert model_word.usage_notes == ""

    def test_easiness_factor_default(self, model_word):
        assert model_word.easiness_factor == 2.5

    def test_repetition_number_default(self, model_word):
        assert model_word.repetition_number == 0

    def test_interval_days_default(self, model_word):
        assert model_word.interval_days == 0

    def test_enriched_at_null_by_default(self, model_word):
        assert model_word.enriched_at is None

    def test_enrichment_error_default(self, model_word):
        assert model_word.enrichment_error == ""

    def test_update_enrichment_fields(self, model_word):
        model_word.mnemonic = "Think of testing!"
        model_word.usage_notes = "Common word"
        model_word.enrichment_status = "enriched"
        model_word.enriched_at = timezone.now()
        model_word.save()
        model_word.refresh_from_db()
        assert model_word.mnemonic == "Think of testing!"
        assert model_word.enrichment_status == "enriched"

    def test_update_sm2_fields(self, model_word):
        model_word.easiness_factor = 2.8
        model_word.repetition_number = 3
        model_word.interval_days = 15
        model_word.save()
        model_word.refresh_from_db()
        assert model_word.easiness_factor == 2.8
        assert model_word.repetition_number == 3
        assert model_word.interval_days == 15


# =============================================================================
# WORD CATEGORY MODEL
# =============================================================================


@pytest.mark.django_db
class TestWordCategoryModel:
    def test_create_category(self, user):
        cat = WordCategory.objects.create(user=user, name="Category1")
        assert cat.name == "Category1"
        assert cat.color == "#6C5CE7"

    def test_str(self, word_category):
        assert str(word_category) == word_category.name

    def test_unique_together(self, user, word_category):
        with pytest.raises(Exception):
            WordCategory.objects.create(user=user, name=word_category.name)

    def test_different_users_same_name(self, user, another_user):
        WordCategory.objects.create(user=user, name="Shared")
        WordCategory.objects.create(user=another_user, name="Shared")
        assert WordCategory.objects.filter(name="Shared").count() == 2


# =============================================================================
# REVIEW SESSION MODEL
# =============================================================================


@pytest.mark.django_db
class TestReviewSessionModel:
    def test_create_session(self, model_user):
        session = ReviewSession.objects.create(
            user=model_user, session_type="review", total_words=10,
        )
        assert session.id is not None
        assert session.is_completed is False
        assert session.session_type == "review"

    def test_session_types(self, model_user):
        for st in ["review", "quick", "focus"]:
            session = ReviewSession.objects.create(
                user=model_user, session_type=st,
            )
            assert session.session_type == st

    def test_session_completion(self, model_user):
        session = ReviewSession.objects.create(
            user=model_user, session_type="review",
        )
        session.is_completed = True
        session.completed_at = timezone.now()
        session.duration_seconds = 300
        session.save()
        session.refresh_from_db()
        assert session.is_completed is True
        assert session.duration_seconds == 300

    def test_session_str(self, model_user):
        session = ReviewSession.objects.create(
            user=model_user, session_type="review",
        )
        assert str(session)

    def test_session_ordering(self, model_user):
        s1 = ReviewSession.objects.create(user=model_user, session_type="review")
        s2 = ReviewSession.objects.create(user=model_user, session_type="review")
        sessions = list(ReviewSession.objects.filter(user=model_user))
        assert sessions[0].id == s2.id


# =============================================================================
# REVIEW LOG MODEL
# =============================================================================


@pytest.mark.django_db
class TestReviewLogModel:
    def test_create_log(self, model_user, model_word):
        session = ReviewSession.objects.create(
            user=model_user, session_type="review",
        )
        log = ReviewLog.objects.create(
            session=session, user=model_user, word=model_word,
            quality=4, is_correct=True,
        )
        assert log.id is not None
        assert log.quality == 4

    def test_log_quality_range(self, model_user, model_word):
        session = ReviewSession.objects.create(
            user=model_user, session_type="review",
        )
        for q in range(6):
            log = ReviewLog.objects.create(
                session=session, user=model_user, word=model_word,
                quality=q, is_correct=q >= 3,
            )
            assert log.quality == q

    def test_log_with_response_time(self, model_user, model_word):
        session = ReviewSession.objects.create(
            user=model_user, session_type="review",
        )
        log = ReviewLog.objects.create(
            session=session, user=model_user, word=model_word,
            quality=5, is_correct=True, response_time_ms=1500,
            previous_confidence=30.0, new_confidence=55.0,
        )
        assert log.response_time_ms == 1500
        assert log.previous_confidence == 30.0

    def test_log_session_null(self, model_user, model_word):
        log = ReviewLog.objects.create(
            session=None, user=model_user, word=model_word,
            quality=3, is_correct=True,
        )
        assert log.session is None

    def test_log_str(self, model_user, model_word):
        session = ReviewSession.objects.create(
            user=model_user, session_type="review",
        )
        log = ReviewLog.objects.create(
            session=session, user=model_user, word=model_word,
            quality=4, is_correct=True,
        )
        assert str(log)


# =============================================================================
# DAILY STREAK MODEL
# =============================================================================


@pytest.mark.django_db
class TestDailyStreakModel:
    def test_create_streak(self, model_user):
        streak = DailyStreak.objects.create(user=model_user)
        assert streak.current_streak == 0
        assert streak.longest_streak == 0

    def test_update_streak(self, model_user):
        streak = DailyStreak.objects.create(
            user=model_user, current_streak=5, longest_streak=10,
        )
        streak.current_streak = 6
        streak.save()
        streak.refresh_from_db()
        assert streak.current_streak == 6

    def test_one_streak_per_user(self, model_user):
        DailyStreak.objects.create(user=model_user)
        with pytest.raises(Exception):
            DailyStreak.objects.create(user=model_user)

    def test_streak_with_frozen(self, model_user):
        tomorrow = date.today() + timedelta(days=1)
        streak = DailyStreak.objects.create(
            user=model_user, streak_frozen_until=tomorrow,
        )
        assert streak.streak_frozen_until == tomorrow

    def test_streak_str(self, model_user):
        streak = DailyStreak.objects.create(user=model_user)
        assert str(streak)


# =============================================================================
# DAILY ACTIVITY MODEL
# =============================================================================


@pytest.mark.django_db
class TestDailyActivityModel:
    def test_create_activity(self, model_user):
        activity = DailyActivity.objects.create(
            user=model_user, date=date.today(),
        )
        assert activity.words_reviewed == 0
        assert activity.xp_earned == 0

    def test_update_activity(self, model_user):
        activity = DailyActivity.objects.create(
            user=model_user, date=date.today(),
        )
        activity.words_reviewed = 10
        activity.correct_answers = 8
        activity.incorrect_answers = 2
        activity.xp_earned = 50
        activity.save()
        activity.refresh_from_db()
        assert activity.words_reviewed == 10
        assert activity.xp_earned == 50

    def test_unique_together_user_date(self, model_user):
        DailyActivity.objects.create(user=model_user, date=date.today())
        with pytest.raises(Exception):
            DailyActivity.objects.create(user=model_user, date=date.today())

    def test_different_dates_ok(self, model_user):
        DailyActivity.objects.create(user=model_user, date=date.today())
        DailyActivity.objects.create(
            user=model_user, date=date.today() - timedelta(days=1),
        )
        assert DailyActivity.objects.filter(user=model_user).count() == 2

    def test_activity_str(self, model_user):
        activity = DailyActivity.objects.create(
            user=model_user, date=date.today(),
        )
        assert str(activity)
