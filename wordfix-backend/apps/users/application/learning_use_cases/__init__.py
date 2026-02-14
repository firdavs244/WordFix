"""
Learning use-cases package – adaptive intelligence.

Re-exports every public use case so existing imports keep working:
    from apps.users.application.learning_use_cases import GetLearningProfileUseCase
"""

from .learning_profile import (
    AnalyzeLearningProfileUseCase,
    GetAdaptiveDifficultyUseCase,
    GetLearningProfileUseCase,
)
from .mistake_patterns import GetMistakePatternsUseCase, RecordMistakeUseCase
from .recommendations import AcceptRecommendationUseCase, GetWordRecommendationsUseCase
from .domain_coverage import UpdateDomainCoverageUseCase
from .performance import RecordSessionPerformanceUseCase

__all__ = [
    "GetLearningProfileUseCase",
    "AnalyzeLearningProfileUseCase",
    "GetAdaptiveDifficultyUseCase",
    "GetMistakePatternsUseCase",
    "RecordMistakeUseCase",
    "GetWordRecommendationsUseCase",
    "AcceptRecommendationUseCase",
    "UpdateDomainCoverageUseCase",
    "RecordSessionPerformanceUseCase",
]
