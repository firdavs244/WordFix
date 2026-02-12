"""
Onboarding dependency injection — factory functions.
"""

from apps.users.application.use_cases import (
    GetOnboardingQuestionsUseCase,
    SubmitOnboardingResultUseCase,
    SkipOnboardingUseCase,
)
from apps.users.domain.services.onboarding_service import OnboardingService
from apps.users.infrastructure.models import OnboardingQuestion


def _get_questions():
    """Get all onboarding questions ordered by level and order."""
    return OnboardingQuestion.objects.all().order_by("level", "order")


def get_onboarding_questions_use_case() -> GetOnboardingQuestionsUseCase:
    return GetOnboardingQuestionsUseCase(question_queryset_fn=_get_questions)


def get_submit_onboarding_use_case() -> SubmitOnboardingResultUseCase:
    from .progress_dependencies import get_xp_service

    return SubmitOnboardingResultUseCase(
        repository=None,  # Uses Django ORM directly inside use case
        onboarding_service=OnboardingService(),
        xp_service=get_xp_service(),
    )


def get_skip_onboarding_use_case() -> SkipOnboardingUseCase:
    return SkipOnboardingUseCase()
