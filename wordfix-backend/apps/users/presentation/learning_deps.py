"""
Dependency injection factories for adaptive-intelligence use cases.
"""

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
from apps.words.infrastructure.repositories.word_repo import DjangoWordRepository
from apps.users.infrastructure.repositories.learning_repo import (
    DomainCoverageRepository,
    LearningProfileRepository,
    MistakePatternRepository,
    SessionPerformanceRepository,
    WordRecommendationRepository,
)


def get_learning_profile_use_case() -> GetLearningProfileUseCase:
    return GetLearningProfileUseCase(
        profile_repo=LearningProfileRepository(),
    )


def get_analyze_profile_use_case() -> AnalyzeLearningProfileUseCase:
    return AnalyzeLearningProfileUseCase(
        profile_repo=LearningProfileRepository(),
        performance_repo=SessionPerformanceRepository(),
        profile_service=LearningProfileService(),
    )


def get_mistake_patterns_use_case() -> GetMistakePatternsUseCase:
    return GetMistakePatternsUseCase(
        pattern_repo=MistakePatternRepository(),
    )


def get_record_mistake_use_case() -> RecordMistakeUseCase:
    return RecordMistakeUseCase(
        pattern_repo=MistakePatternRepository(),
        pattern_service=MistakePatternService(),
    )


def get_recommendations_use_case() -> GetWordRecommendationsUseCase:
    return GetWordRecommendationsUseCase(
        recommendation_repo=WordRecommendationRepository(),
        ai_provider=None,  # AI provider injected when available
        word_repo=DjangoWordRepository(),
    )


def get_accept_recommendation_use_case() -> AcceptRecommendationUseCase:
    return AcceptRecommendationUseCase(
        recommendation_repo=WordRecommendationRepository(),
        word_repo=DjangoWordRepository(),
    )


def get_domain_coverage_use_case() -> UpdateDomainCoverageUseCase:
    return UpdateDomainCoverageUseCase(
        domain_repo=DomainCoverageRepository(),
        word_repo=DjangoWordRepository(),
    )


def get_adaptive_difficulty_use_case() -> GetAdaptiveDifficultyUseCase:
    return GetAdaptiveDifficultyUseCase(
        profile_repo=LearningProfileRepository(),
        profile_service=LearningProfileService(),
    )


def get_record_performance_use_case() -> RecordSessionPerformanceUseCase:
    return RecordSessionPerformanceUseCase(
        performance_repo=SessionPerformanceRepository(),
    )
