"""
Integration tests for learning-related repositories.
Covers: LearningProfileRepository, MistakePatternRepository,
        DomainCoverageRepository, WordRecommendationRepository,
        SessionPerformanceRepository
"""

from datetime import timedelta

import pytest
from django.utils import timezone

from apps.users.infrastructure.models import (
    DomainCoverage,
    LearningProfile,
    MistakePattern,
    SessionPerformance,
    WordRecommendation,
)
from apps.users.infrastructure.repositories.learning_repo import (
    DomainCoverageRepository,
    LearningProfileRepository,
    MistakePatternRepository,
    SessionPerformanceRepository,
    WordRecommendationRepository,
)


@pytest.mark.django_db
class TestLearningProfileRepository:
    def setup_method(self):
        self.repo = LearningProfileRepository()

    def test_get_by_user_none(self, user):
        result = self.repo.get_by_user(user.id)
        assert result is None

    def test_get_or_create(self, user):
        profile = self.repo.get_or_create(user.id)
        assert profile is not None
        assert profile.user_id == user.id

    def test_get_or_create_returns_existing(self, user):
        p1 = self.repo.get_or_create(user.id)
        p2 = self.repo.get_or_create(user.id)
        assert p1.id == p2.id

    def test_create(self, user):
        profile = self.repo.create(user_id=user.id)
        assert profile.user_id == user.id

    def test_save(self, user):
        profile = self.repo.get_or_create(user.id)
        profile.total_sessions = 42
        saved = self.repo.save(profile)
        assert saved.total_sessions == 42

    def test_get_by_user_after_create(self, user):
        self.repo.get_or_create(user.id)
        result = self.repo.get_by_user(user.id)
        assert result is not None


@pytest.mark.django_db
class TestMistakePatternRepository:
    def setup_method(self):
        self.repo = MistakePatternRepository()

    def test_get_by_user_empty(self, user):
        result = self.repo.get_by_user(user.id)
        assert result == []

    def test_create_and_get(self, user):
        pattern = self.repo.create(
            user_id=user.id,
            pattern_type="spelling",
            description="Common spelling error",
            related_words=["hello", "helo"],
            occurrence_count=3,
        )
        patterns = self.repo.get_by_user(user.id)
        assert len(patterns) == 1
        assert patterns[0].pattern_type == "spelling"

    def test_get_by_user_excludes_resolved(self, user):
        self.repo.create(
            user_id=user.id,
            pattern_type="spelling",
            description="test",
            related_words=["a"],
            occurrence_count=1,
            is_resolved=True,
        )
        result = self.repo.get_by_user(user.id, include_resolved=False)
        assert len(result) == 0

    def test_get_by_user_includes_resolved(self, user):
        self.repo.create(
            user_id=user.id,
            pattern_type="spelling",
            description="test",
            related_words=["a"],
            occurrence_count=1,
            is_resolved=True,
        )
        result = self.repo.get_by_user(user.id, include_resolved=True)
        assert len(result) == 1

    def test_find_similar_match(self, user):
        self.repo.create(
            user_id=user.id,
            pattern_type="spelling",
            description="test",
            related_words=["hello", "world"],
            occurrence_count=1,
        )
        result = self.repo.find_similar(user.id, "spelling", ["hello", "new"])
        assert result is not None

    def test_find_similar_no_match(self, user):
        self.repo.create(
            user_id=user.id,
            pattern_type="spelling",
            description="test",
            related_words=["hello", "world"],
            occurrence_count=1,
        )
        result = self.repo.find_similar(user.id, "spelling", ["xyz", "abc"])
        assert result is None

    def test_find_similar_different_type(self, user):
        self.repo.create(
            user_id=user.id,
            pattern_type="spelling",
            description="test",
            related_words=["hello"],
            occurrence_count=1,
        )
        result = self.repo.find_similar(user.id, "grammar", ["hello"])
        assert result is None

    def test_save(self, user):
        pattern = self.repo.create(
            user_id=user.id,
            pattern_type="spelling",
            description="test",
            related_words=["a"],
            occurrence_count=1,
        )
        pattern.occurrence_count = 5
        saved = self.repo.save(pattern)
        assert saved.occurrence_count == 5


@pytest.mark.django_db
class TestDomainCoverageRepository:
    def setup_method(self):
        self.repo = DomainCoverageRepository()

    def test_get_by_user_empty(self, user):
        result = self.repo.get_by_user(user.id)
        assert result == []

    def test_get_or_create(self, user):
        coverage = self.repo.get_or_create(user.id, "technology")
        assert coverage.domain == "technology"
        assert coverage.user_id == user.id

    def test_save(self, user):
        coverage = self.repo.get_or_create(user.id, "technology")
        coverage.total_words_in_domain = 15
        saved = self.repo.save(coverage)
        assert saved.total_words_in_domain == 15

    def test_get_by_user_multiple(self, user):
        self.repo.get_or_create(user.id, "technology")
        self.repo.get_or_create(user.id, "travel")
        result = self.repo.get_by_user(user.id)
        assert len(result) == 2


@pytest.mark.django_db
class TestWordRecommendationRepository:
    def setup_method(self):
        self.repo = WordRecommendationRepository()

    def test_create_and_get_active(self, user):
        self.repo.create(
            user_id=user.id,
            recommended_word="example",
            reason="Common word",
            priority_score=0.8,
        )
        recs = self.repo.get_active(user.id)
        assert len(recs) == 1
        assert recs[0].recommended_word == "example"

    def test_get_active_excludes_accepted(self, user):
        rec = self.repo.create(
            user_id=user.id,
            recommended_word="example",
            reason="test",
            priority_score=0.5,
        )
        self.repo.accept(rec.id, user.id)
        recs = self.repo.get_active(user.id)
        assert len(recs) == 0

    def test_get_active_excludes_dismissed(self, user):
        rec = self.repo.create(
            user_id=user.id,
            recommended_word="example",
            reason="test",
            priority_score=0.5,
        )
        self.repo.dismiss(rec.id, user.id)
        recs = self.repo.get_active(user.id)
        assert len(recs) == 0

    def test_accept_returns_true(self, user):
        rec = self.repo.create(
            user_id=user.id,
            recommended_word="example",
            reason="test",
            priority_score=0.5,
        )
        result = self.repo.accept(rec.id, user.id)
        assert result is True

    def test_dismiss_returns_true(self, user):
        rec = self.repo.create(
            user_id=user.id,
            recommended_word="example",
            reason="test",
            priority_score=0.5,
        )
        result = self.repo.dismiss(rec.id, user.id)
        assert result is True

    def test_get_active_limit(self, user):
        for i in range(15):
            self.repo.create(
                user_id=user.id,
                recommended_word=f"word_{i}",
                reason="test",
                priority_score=0.5,
            )
        recs = self.repo.get_active(user.id, limit=5)
        assert len(recs) == 5


@pytest.mark.django_db
class TestSessionPerformanceRepository:
    def setup_method(self):
        self.repo = SessionPerformanceRepository()

    def test_create(self, user):
        now = timezone.now()
        perf = self.repo.create(
            user_id=user.id,
            session_type="review",
            accuracy=0.85,
            started_at=now - timedelta(minutes=10),
            ended_at=now,
        )
        assert perf.session_type == "review"
        assert perf.accuracy == 0.85

    def test_get_recent(self, user):
        now = timezone.now()
        self.repo.create(
            user_id=user.id,
            session_type="review",
            accuracy=0.8,
            started_at=now - timedelta(minutes=5),
            ended_at=now,
        )
        results = self.repo.get_recent(user.id, days=30)
        assert len(results) == 1

    def test_get_recent_empty(self, user):
        results = self.repo.get_recent(user.id, days=30)
        assert results == []
