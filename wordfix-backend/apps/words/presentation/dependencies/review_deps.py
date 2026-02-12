"""
Review use-case factories.
"""

from apps.words.application.use_cases import (
    CompleteReviewSessionUseCase,
    GetReviewSummaryUseCase,
    GetReviewWordsUseCase,
    StartReviewSessionUseCase,
    SubmitReviewAnswerUseCase,
    UpdateStreakUseCase,
)
from .common_deps import (
    get_activity_repository,
    get_log_repository,
    get_session_repository,
    get_sr_service,
    get_streak_repository,
    get_user_repository,
    get_word_repository,
)


def get_review_words_use_case() -> GetReviewWordsUseCase:
    return GetReviewWordsUseCase(word_repo=get_word_repository())


def get_start_session_use_case() -> StartReviewSessionUseCase:
    return StartReviewSessionUseCase(
        session_repo=get_session_repository(),
        word_repo=get_word_repository(),
    )


def get_submit_answer_use_case() -> SubmitReviewAnswerUseCase:
    from .confusing_deps import get_confusing_pair_repository
    from .challenge_deps import get_challenge_repository

    return SubmitReviewAnswerUseCase(
        word_repo=get_word_repository(),
        session_repo=get_session_repository(),
        log_repo=get_log_repository(),
        sr_service=get_sr_service(),
        streak_repo=get_streak_repository(),
        activity_repo=get_activity_repository(),
        confusing_pair_repo=get_confusing_pair_repository(),
        challenge_repo=get_challenge_repository(),
    )


def get_complete_session_use_case() -> CompleteReviewSessionUseCase:
    from .challenge_deps import get_challenge_repository

    return CompleteReviewSessionUseCase(
        session_repo=get_session_repository(),
        log_repo=get_log_repository(),
        challenge_repo=get_challenge_repository(),
    )


def get_review_summary_use_case() -> GetReviewSummaryUseCase:
    return GetReviewSummaryUseCase(
        word_repo=get_word_repository(),
        streak_repo=get_streak_repository(),
        activity_repo=get_activity_repository(),
        user_repo=get_user_repository(),
    )


def get_update_streak_use_case() -> UpdateStreakUseCase:
    return UpdateStreakUseCase(streak_repo=get_streak_repository())
