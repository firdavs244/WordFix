"""
Tests for Word infrastructure repositories: DjangoWordRepository,
DjangoWordCategoryRepository, DjangoReviewSessionRepository,
DjangoReviewLogRepository, DjangoStreakRepository,
DjangoDailyActivityRepository.
"""

import uuid
from datetime import date, timedelta

import pytest
from django.utils import timezone

from apps.common.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from apps.users.infrastructure.models import CustomUser
from apps.words.infrastructure.models import (
    DailyActivity,
    DailyStreak,
    Word,
    WordCategory,
)
from apps.words.infrastructure.repositories import (
    DjangoDailyActivityRepository,
    DjangoReviewLogRepository,
    DjangoReviewSessionRepository,
    DjangoStreakRepository,
    DjangoWordCategoryRepository,
    DjangoWordRepository,
)


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def repo_user(db):
    return CustomUser.objects.create_user(
        email="repo@test.com",
        username="repouser",
        password="testpass123",
    )


@pytest.fixture
def repo_word(repo_user):
    return Word.objects.create(
        user=repo_user,
        original_word="repoword",
        translation="tarjima",
    )


# =============================================================================
# DJANGO WORD REPOSITORY
# =============================================================================


@pytest.mark.django_db
class TestDjangoWordRepository:
    @pytest.fixture
    def repo(self):
        return DjangoWordRepository()

    def test_create_word(self, repo, user):
        entity = repo.create(
            user_id=user.id, original_word="example", translation="misol",
        )
        assert entity.original_word == "example"
        assert entity.user_id == user.id

    def test_create_duplicate_raises(self, repo, user, sample_word):
        with pytest.raises(EntityAlreadyExistsError):
            repo.create(
                user_id=user.id, original_word=sample_word.original_word,
            )

    def test_get_by_id(self, repo, user, sample_word):
        entity = repo.get_by_id(word_id=sample_word.id, user_id=user.id)
        assert entity.original_word == sample_word.original_word

    def test_get_by_id_not_found(self, repo, user):
        with pytest.raises(EntityNotFoundError):
            repo.get_by_id(word_id=uuid.uuid4(), user_id=user.id)

    def test_get_by_id_wrong_user(self, repo, user, another_user, sample_word):
        with pytest.raises(EntityNotFoundError):
            repo.get_by_id(word_id=sample_word.id, user_id=another_user.id)

    def test_get_all_by_user(self, repo, user, sample_words):
        words, total = repo.get_all_by_user(user_id=user.id)
        assert total == 5
        assert len(words) == 5

    def test_get_all_by_user_pagination(self, repo, user, sample_words):
        words, total = repo.get_all_by_user(user_id=user.id, page=1, page_size=2)
        assert len(words) == 2
        assert total == 5

    def test_get_all_by_user_page_2(self, repo, user, sample_words):
        words, _ = repo.get_all_by_user(user_id=user.id, page=2, page_size=2)
        assert len(words) == 2

    def test_filter_by_difficulty(self, repo, user, sample_words):
        words, total = repo.get_all_by_user(
            user_id=user.id, filters={"difficulty_level": "easy"}
        )
        assert total == 2
        for w in words:
            assert w.difficulty_level == "easy"

    def test_filter_by_search(self, repo, user, sample_words):
        words, total = repo.get_all_by_user(
            user_id=user.id, filters={"search": "apple"}
        )
        assert total == 1
        assert words[0].original_word == "apple"

    def test_filter_by_part_of_speech(self, repo, user, sample_words):
        words, total = repo.get_all_by_user(
            user_id=user.id, filters={"part_of_speech": "noun"}
        )
        assert total == 2

    def test_ordering(self, repo, user, sample_words):
        words, _ = repo.get_all_by_user(
            user_id=user.id, ordering="original_word"
        )
        names = [w.original_word for w in words]
        assert names == sorted(names)

    def test_update_word(self, repo, user, sample_word):
        entity = repo.update(
            word_id=sample_word.id, user_id=user.id,
            translation="updated_translation",
        )
        assert entity.translation == "updated_translation"

    def test_update_not_found(self, repo, user):
        with pytest.raises(EntityNotFoundError):
            repo.update(word_id=uuid.uuid4(), user_id=user.id, translation="x")

    def test_delete_word(self, repo, user, sample_word):
        repo.delete(word_id=sample_word.id, user_id=user.id)
        assert not Word.objects.filter(id=sample_word.id).exists()

    def test_delete_not_found(self, repo, user):
        with pytest.raises(EntityNotFoundError):
            repo.delete(word_id=uuid.uuid4(), user_id=user.id)

    def test_exists(self, repo, user, sample_word):
        assert repo.exists(original_word=sample_word.original_word, user_id=user.id)

    def test_not_exists(self, repo, user):
        assert not repo.exists(original_word="nonexistent", user_id=user.id)

    def test_get_count_by_user(self, repo, user, sample_words):
        assert repo.get_count_by_user(user_id=user.id) == 5

    def test_search(self, repo, user, sample_words):
        words, total = repo.search(user_id=user.id, query="run")
        assert total >= 1

    def test_get_by_category(self, repo, user, sample_words, word_category):
        words = repo.get_by_category(user_id=user.id, category_id=word_category.id)
        assert len(words) == 5

    def test_get_words_for_review(self, repo, user, sample_word):
        sample_word.next_review_at = timezone.now() - timezone.timedelta(hours=1)
        sample_word.save()
        words = repo.get_words_for_review(user_id=user.id)
        assert len(words) >= 1

    def test_bulk_create(self, repo, user):
        words_data = [
            {"original_word": "bulk1", "translation": "b1"},
            {"original_word": "bulk2", "translation": "b2"},
        ]
        result = repo.bulk_create(user_id=user.id, words_data=words_data)
        assert result["created"] == 2
        assert result["skipped"] == 0

    def test_bulk_create_skip_duplicates(self, repo, user, sample_word):
        words_data = [
            {"original_word": sample_word.original_word, "translation": "dup"},
            {"original_word": "newword", "translation": "new"},
        ]
        result = repo.bulk_create(user_id=user.id, words_data=words_data)
        assert result["created"] == 1
        assert result["skipped"] == 1

    def test_get_stats(self, repo, user, sample_words):
        stats = repo.get_stats(user_id=user.id)
        assert "total" in stats
        assert stats["total"] == 5

    def test_isolation_between_users(self, repo, user, another_user, sample_words):
        words, total = repo.get_all_by_user(user_id=another_user.id)
        assert total == 0


# =============================================================================
# DJANGO WORD CATEGORY REPOSITORY
# =============================================================================


@pytest.mark.django_db
class TestDjangoWordCategoryRepository:
    @pytest.fixture
    def repo(self):
        return DjangoWordCategoryRepository()

    def test_create_category(self, repo, user):
        entity = repo.create(user_id=user.id, name="NewCat", color="#FF0000")
        assert entity.name == "NewCat"

    def test_get_all_by_user(self, repo, user, word_category):
        categories = repo.get_all_by_user(user_id=user.id)
        assert len(categories) == 1

    def test_delete_category(self, repo, user, word_category):
        repo.delete(category_id=word_category.id, user_id=user.id)
        assert not WordCategory.objects.filter(id=word_category.id).exists()

    def test_delete_not_found(self, repo, user):
        with pytest.raises(EntityNotFoundError):
            repo.delete(category_id=uuid.uuid4(), user_id=user.id)

    def test_exists(self, repo, user, word_category):
        assert repo.exists(name=word_category.name, user_id=user.id)

    def test_not_exists(self, repo, user):
        assert not repo.exists(name="NonExistent", user_id=user.id)

    def test_isolation(self, repo, user, another_user, word_category):
        categories = repo.get_all_by_user(user_id=another_user.id)
        assert len(categories) == 0


# =============================================================================
# REVIEW SESSION REPOSITORY
# =============================================================================


@pytest.mark.django_db
class TestDjangoReviewSessionRepository:
    def setup_method(self):
        self.repo = DjangoReviewSessionRepository()

    def test_create(self, repo_user):
        session = self.repo.create(
            user_id=repo_user.id, session_type="review", total_words=10,
        )
        assert session.user_id == repo_user.id
        assert session.session_type == "review"
        assert session.total_words == 10

    def test_get_by_id(self, repo_user):
        session = self.repo.create(user_id=repo_user.id, session_type="quick")
        result = self.repo.get_by_id(session_id=session.id, user_id=repo_user.id)
        assert result.id == session.id

    def test_update(self, repo_user):
        session = self.repo.create(user_id=repo_user.id, session_type="review")
        updated = self.repo.update(
            session_id=session.id, is_completed=True,
            total_words=5, correct_count=4,
        )
        assert updated.is_completed is True
        assert updated.total_words == 5

    def test_get_by_user(self, repo_user):
        for _ in range(3):
            self.repo.create(user_id=repo_user.id, session_type="review")
        sessions, total = self.repo.get_by_user(user_id=repo_user.id)
        assert total == 3
        assert len(sessions) == 3

    def test_get_by_user_pagination(self, repo_user):
        for _ in range(5):
            self.repo.create(user_id=repo_user.id, session_type="review")
        sessions, total = self.repo.get_by_user(
            user_id=repo_user.id, page=1, page_size=2,
        )
        assert total == 5
        assert len(sessions) == 2


# =============================================================================
# REVIEW LOG REPOSITORY
# =============================================================================


@pytest.mark.django_db
class TestDjangoReviewLogRepository:
    def setup_method(self):
        self.repo = DjangoReviewLogRepository()
        self.session_repo = DjangoReviewSessionRepository()

    def test_create(self, repo_user, repo_word):
        session = self.session_repo.create(
            user_id=repo_user.id, session_type="review",
        )
        log = self.repo.create(
            session_id=session.id, user_id=repo_user.id,
            word_id=repo_word.id, quality=4,
            is_correct=True, response_time_ms=1500,
        )
        assert log.quality == 4
        assert log.is_correct is True

    def test_get_by_session(self, repo_user, repo_word):
        session = self.session_repo.create(
            user_id=repo_user.id, session_type="review",
        )
        for q in [3, 4, 5]:
            self.repo.create(
                session_id=session.id, user_id=repo_user.id,
                word_id=repo_word.id, quality=q, is_correct=True,
            )
        logs = self.repo.get_by_session(session_id=session.id)
        assert len(logs) == 3

    def test_get_by_user(self, repo_user, repo_word):
        session = self.session_repo.create(
            user_id=repo_user.id, session_type="review",
        )
        for i in range(3):
            self.repo.create(
                session_id=session.id, user_id=repo_user.id,
                word_id=repo_word.id, quality=i + 2, is_correct=True,
            )
        logs, total = self.repo.get_by_user(user_id=repo_user.id)
        assert total == 3


# =============================================================================
# STREAK REPOSITORY
# =============================================================================


@pytest.mark.django_db
class TestDjangoStreakRepository:
    def setup_method(self):
        self.repo = DjangoStreakRepository()

    def test_get_or_create(self, repo_user):
        streak = self.repo.get_or_create(user_id=repo_user.id)
        assert streak.current_streak == 0
        assert streak.user_id == repo_user.id

    def test_get_or_create_existing(self, repo_user):
        DailyStreak.objects.create(user=repo_user, current_streak=5)
        streak = self.repo.get_or_create(user_id=repo_user.id)
        assert streak.current_streak == 5

    def test_update(self, repo_user):
        streak = self.repo.get_or_create(user_id=repo_user.id)
        updated = self.repo.update(
            streak_id=streak.id, current_streak=3,
            longest_streak=3, last_activity_date=date.today(),
        )
        assert updated.current_streak == 3


# =============================================================================
# DAILY ACTIVITY REPOSITORY
# =============================================================================


@pytest.mark.django_db
class TestDjangoDailyActivityRepository:
    def setup_method(self):
        self.repo = DjangoDailyActivityRepository()

    def test_get_or_create_today(self, repo_user):
        activity = self.repo.get_or_create_today(user_id=repo_user.id)
        assert activity.date == date.today()
        assert activity.words_reviewed == 0

    def test_get_or_create_today_existing(self, repo_user):
        DailyActivity.objects.create(
            user=repo_user, date=date.today(), words_reviewed=5,
        )
        activity = self.repo.get_or_create_today(user_id=repo_user.id)
        assert activity.words_reviewed == 5

    def test_update(self, repo_user):
        activity = self.repo.get_or_create_today(user_id=repo_user.id)
        updated = self.repo.update(
            activity_id=activity.id, words_reviewed=10, xp_earned=50,
        )
        assert updated.words_reviewed == 10
        assert updated.xp_earned == 50

    def test_get_by_date_range(self, repo_user):
        for i in range(5):
            DailyActivity.objects.create(
                user=repo_user,
                date=date.today() - timedelta(days=i),
                words_reviewed=i,
            )
        start = date.today() - timedelta(days=3)
        end = date.today()
        activities = self.repo.get_by_date_range(
            user_id=repo_user.id, start_date=start, end_date=end,
        )
        assert len(activities) == 4
