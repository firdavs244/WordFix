"""
Daily challenges dependency injection.
"""

from apps.words.application.use_cases.daily_challenges import (
    ClaimDailyBonusUseCase,
    GetDailyChallengesUseCase,
    UpdateChallengeProgressUseCase,
)
from apps.words.domain.services import DailyChallengeService
from .common_deps import get_word_repository


def get_challenge_repository():
    from apps.words.infrastructure.repositories import DjangoDailyChallengeRepository
    return DjangoDailyChallengeRepository()


def get_progress_repository():
    from apps.users.infrastructure.repositories import DjangoProgressRepository
    return DjangoProgressRepository()


def _get_xp_service():
    try:
        from apps.users.presentation.progress_dependencies import get_xp_service
        return get_xp_service()
    except Exception:
        return None


def get_daily_challenges_use_case() -> GetDailyChallengesUseCase:
    return GetDailyChallengesUseCase(
        challenge_repo=get_challenge_repository(),
        word_repo=get_word_repository(),
        progress_repo=get_progress_repository(),
        challenge_service=DailyChallengeService(),
    )


def get_update_challenge_progress_use_case() -> UpdateChallengeProgressUseCase:
    return UpdateChallengeProgressUseCase(
        challenge_repo=get_challenge_repository(),
        xp_service=_get_xp_service(),
    )


def get_claim_daily_bonus_use_case() -> ClaimDailyBonusUseCase:
    return ClaimDailyBonusUseCase(
        challenge_repo=get_challenge_repository(),
    )
