"""
Game use-case factories.
"""

from apps.words.application.use_cases import (
    GetGameHistoryUseCase,
    GetGameStatsUseCase,
    StartSpeedRoundUseCase,
    StartWordContextUseCase,
    StartWordMatchUseCase,
    SubmitSpeedRoundUseCase,
    SubmitWordContextUseCase,
    SubmitWordMatchUseCase,
)
from .common_deps import (
    _get_ai_provider,
    get_activity_repository,
    get_game_session_repository,
    get_sr_service,
    get_user_repository,
    get_word_repository,
)


def get_start_speed_round_use_case() -> StartSpeedRoundUseCase:
    return StartSpeedRoundUseCase(
        word_repo=get_word_repository(),
        game_session_repo=get_game_session_repository(),
    )


def get_submit_speed_round_use_case() -> SubmitSpeedRoundUseCase:
    from .challenge_deps import get_challenge_repository

    return SubmitSpeedRoundUseCase(
        word_repo=get_word_repository(),
        game_session_repo=get_game_session_repository(),
        sr_service=get_sr_service(),
        activity_repo=get_activity_repository(),
        challenge_repo=get_challenge_repository(),
    )


def get_start_word_match_use_case() -> StartWordMatchUseCase:
    return StartWordMatchUseCase(
        word_repo=get_word_repository(),
        game_session_repo=get_game_session_repository(),
    )


def get_submit_word_match_use_case() -> SubmitWordMatchUseCase:
    from .challenge_deps import get_challenge_repository

    return SubmitWordMatchUseCase(
        word_repo=get_word_repository(),
        game_session_repo=get_game_session_repository(),
        sr_service=get_sr_service(),
        activity_repo=get_activity_repository(),
        challenge_repo=get_challenge_repository(),
    )


def get_start_word_context_use_case() -> StartWordContextUseCase:
    from core.services.ai.prompts import NATIVE_LANGUAGE_MAP, WORD_CONTEXT_GAME_PROMPT

    return StartWordContextUseCase(
        word_repo=get_word_repository(),
        game_session_repo=get_game_session_repository(),
        ai_provider=_get_ai_provider(),
        user_repo=get_user_repository(),
        prompt_template=WORD_CONTEXT_GAME_PROMPT,
        language_map=NATIVE_LANGUAGE_MAP,
    )


def get_submit_word_context_use_case() -> SubmitWordContextUseCase:
    from .challenge_deps import get_challenge_repository

    return SubmitWordContextUseCase(
        word_repo=get_word_repository(),
        game_session_repo=get_game_session_repository(),
        sr_service=get_sr_service(),
        activity_repo=get_activity_repository(),
        challenge_repo=get_challenge_repository(),
    )


def get_game_history_use_case() -> GetGameHistoryUseCase:
    return GetGameHistoryUseCase(
        game_session_repo=get_game_session_repository(),
    )


def get_game_stats_use_case() -> GetGameStatsUseCase:
    return GetGameStatsUseCase(
        game_session_repo=get_game_session_repository(),
    )
