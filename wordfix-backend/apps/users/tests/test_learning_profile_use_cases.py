"""
Tests for learning-profile use cases.
"""

import uuid
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch

import pytest

from apps.users.application.learning_use_cases import (
    AcceptRecommendationUseCase,
    AnalyzeLearningProfileUseCase,
    GetAdaptiveDifficultyUseCase,
    GetLearningProfileUseCase,
    GetMistakePatternsUseCase,
    GetWordRecommendationsUseCase,
    RecordMistakeUseCase,
    RecordSessionPerformanceUseCase,
    UpdateDomainCoverageUseCase,
)
from apps.users.domain.services.learning_profile_service import LearningProfileService
from apps.users.domain.services.mistake_pattern_service import MistakePatternService


def _mock_profile(**overrides):
    defaults = {
        "id": uuid.uuid4(),
        "user_id": uuid.uuid4(),
        "preferred_style": "visual",
        "style_confidence": 0.5,
        "best_hour_start": 9,
        "best_hour_end": 12,
        "best_days": [0, 1, 2, 3, 4],
        "avg_session_duration": 15,
        "optimal_words_per_session": 10,
        "avg_retention_rate": 0.0,
        "strongest_skills": [],
        "weakest_skills": [],
        "current_difficulty_level": 0.5,
        "difficulty_adjustment_rate": 0.05,
        "last_analyzed_at": None,
        "analysis_data": {},
    }
    defaults.update(overrides)
    profile = MagicMock(**defaults)
    for k, v in defaults.items():
        setattr(profile, k, v)
    return profile


def _mock_performance(hour=10, day=1, accuracy=0.8, session_type="review"):
    perf = MagicMock()
    perf.hour_of_day = hour
    perf.day_of_week = day
    perf.accuracy = accuracy
    perf.effectiveness_score = accuracy * 0.4 + 1.0 * 0.3 + 0.5 * 0.3
    perf.session_type = session_type
    return perf


class TestGetLearningProfile:

    def test_get_profile_creates_new(self):
        repo = MagicMock()
        repo.get_or_create.return_value = _mock_profile()
        uc = GetLearningProfileUseCase(repo)
        result = uc.execute(uuid.uuid4())
        assert result["preferred_style"] == "visual"
        repo.get_or_create.assert_called_once()

    def test_get_profile_returns_existing(self):
        profile = _mock_profile(preferred_style="auditory", style_confidence=0.8)
        repo = MagicMock()
        repo.get_or_create.return_value = profile
        uc = GetLearningProfileUseCase(repo)
        result = uc.execute(uuid.uuid4())
        assert result["preferred_style"] == "auditory"
        assert result["style_confidence"] == 0.8


class TestAnalyzeLearningProfile:

    def test_analyze_updates_profile(self):
        profile = _mock_profile()
        profile_repo = MagicMock()
        profile_repo.get_or_create.return_value = profile
        perf_repo = MagicMock()
        perf_repo.get_recent.return_value = [
            _mock_performance(hour=9, accuracy=0.9),
            _mock_performance(hour=10, accuracy=0.7),
        ]
        service = LearningProfileService()
        uc = AnalyzeLearningProfileUseCase(
            profile_repo=profile_repo,
            performance_repo=perf_repo,
            profile_service=service,
        )
        result = uc.execute(uuid.uuid4())
        assert "learning_style" in result
        assert "optimal_time" in result
        assert "skills" in result
        profile_repo.save.assert_called_once()


class TestRecordMistake:

    def test_record_mistake_new_pattern(self):
        repo = MagicMock()
        repo.find_similar.return_value = None
        new_pattern = MagicMock()
        new_pattern.id = uuid.uuid4()
        repo.create.return_value = new_pattern
        service = MistakePatternService()
        uc = RecordMistakeUseCase(repo, service)
        result = uc.execute(uuid.uuid4(), "goed", "went", "I goed there")
        assert result["is_new"] is True
        assert result["pattern_id"] is not None

    def test_record_mistake_existing_pattern(self):
        existing = MagicMock()
        existing.id = uuid.uuid4()
        existing.occurrence_count = 2
        existing.examples = [{"wrong": "goed", "correct": "went", "context": ""}]
        repo = MagicMock()
        repo.find_similar.return_value = existing
        service = MistakePatternService()
        uc = RecordMistakeUseCase(repo, service)
        result = uc.execute(uuid.uuid4(), "goed", "went", "I goed again")
        assert result["is_new"] is False
        assert existing.occurrence_count == 3


class TestGetMistakePatterns:

    def test_get_patterns(self):
        pattern = MagicMock()
        pattern.id = uuid.uuid4()
        pattern.pattern_type = "spelling"
        pattern.description = "Spelling error"
        pattern.examples = []
        pattern.occurrence_count = 1
        pattern.is_resolved = False
        pattern.drills_completed = 0
        pattern.success_rate_after_drills = 0.0
        pattern.related_words = ["recieve", "receive"]
        repo = MagicMock()
        repo.get_by_user.return_value = [pattern]
        uc = GetMistakePatternsUseCase(repo)
        result = uc.execute(uuid.uuid4())
        assert len(result) == 1
        assert result[0]["pattern_type"] == "spelling"


class TestGetWordRecommendations:

    def test_get_recommendations_cached(self):
        rec = MagicMock()
        rec.id = uuid.uuid4()
        rec.recommended_word = "analyze"
        rec.translation = "tahlil qilmoq"
        rec.reason = "Academic"
        rec.reason_type = "high_frequency"
        rec.priority_score = 0.7
        rec.is_accepted = False
        rec.ai_confidence = 0.5
        repo = MagicMock()
        repo.get_active.return_value = [rec] * 10
        uc = GetWordRecommendationsUseCase(repo)
        result = uc.execute(uuid.uuid4(), count=10)
        assert len(result) == 10

    def test_get_recommendations_generates(self):
        repo = MagicMock()
        repo.get_active.return_value = []
        new_rec = MagicMock()
        new_rec.id = uuid.uuid4()
        new_rec.recommended_word = "analyze"
        new_rec.translation = "tahlil qilmoq"
        new_rec.reason = "Academic vocabulary"
        new_rec.reason_type = "high_frequency"
        new_rec.priority_score = 0.5
        new_rec.is_accepted = False
        new_rec.ai_confidence = 0.0
        repo.create.return_value = new_rec
        uc = GetWordRecommendationsUseCase(repo, ai_provider=None)
        result = uc.execute(uuid.uuid4(), count=5)
        assert len(result) == 5

    def test_recommendations_fallback(self):
        """When AI is unavailable, fallback words are used."""
        repo = MagicMock()
        repo.get_active.return_value = []
        new_rec = MagicMock()
        new_rec.id = uuid.uuid4()
        new_rec.recommended_word = "analyze"
        new_rec.translation = "tahlil qilmoq"
        new_rec.reason = "Academic vocabulary"
        new_rec.reason_type = "high_frequency"
        new_rec.priority_score = 0.5
        new_rec.is_accepted = False
        new_rec.ai_confidence = 0.0
        repo.create.return_value = new_rec
        uc = GetWordRecommendationsUseCase(repo, ai_provider=None)
        result = uc.execute(uuid.uuid4(), count=3)
        assert len(result) == 3


class TestAcceptRecommendation:

    def test_accept_recommendation(self):
        repo = MagicMock()
        repo.accept.return_value = True
        uc = AcceptRecommendationUseCase(repo)
        result = uc.execute(uuid.uuid4(), uuid.uuid4())
        assert result["success"] is True


class TestUpdateDomainCoverage:

    def test_update_domain_coverage(self):
        domain_repo = MagicMock()
        coverage = MagicMock()
        coverage.total_words_in_domain = 0
        coverage.coverage_percentage = 0
        coverage.mastered_count = 0
        coverage.learning_count = 0
        domain_repo.get_or_create.return_value = coverage
        uc = UpdateDomainCoverageUseCase(domain_repo, word_repo=None)
        result = uc.execute(uuid.uuid4())
        assert len(result) == 10  # 10 domains


class TestAdaptiveDifficulty:

    def test_adaptive_difficulty(self):
        profile = _mock_profile(current_difficulty_level=0.5, difficulty_adjustment_rate=0.05)
        repo = MagicMock()
        repo.get_or_create.return_value = profile
        service = LearningProfileService()
        uc = GetAdaptiveDifficultyUseCase(repo, service)
        result = uc.execute(uuid.uuid4(), recent_accuracy=0.9)
        assert result["adjusted"] is True
        assert result["direction"] == "up"
        assert result["difficulty_level"] == 0.55


class TestRecordSessionPerformance:

    def test_record_session_performance(self):
        repo = MagicMock()
        perf = MagicMock()
        perf.id = uuid.uuid4()
        repo.create.return_value = perf
        uc = RecordSessionPerformanceUseCase(repo)
        now = datetime.now(timezone.utc)
        result = uc.execute(
            user_id=uuid.uuid4(),
            session_type="review",
            started_at=now - timedelta(minutes=10),
            ended_at=now,
            accuracy=0.8,
            completion_rate=1.0,
        )
        assert "performance_id" in result
        assert "effectiveness" in result
        assert result["effectiveness"] > 0
