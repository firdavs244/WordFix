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
from apps.words.application.use_cases.games import (
    StartStoryBuilderUseCase,
    SubmitStoryRoundUseCase,
    CompleteStoryBuilderUseCase,
    StartListeningChallengeUseCase,
    SubmitListeningAnswerUseCase,
    CompleteListeningChallengeUseCase,
    StartSynonymAntonymUseCase,
    SubmitSynonymAntonymUseCase,
    CompleteSynonymAntonymUseCase,
    StartIrregularVerbsUseCase,
    SubmitIrregularVerbUseCase,
    CompleteIrregularVerbsUseCase,
)
from .common_deps import (
    _get_ai_provider,
    _get_tts_provider,
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


# =============================================================================
# Story Builder
# =============================================================================


def get_story_builder_start_use_case() -> StartStoryBuilderUseCase:
    from core.services.ai.prompts import NATIVE_LANGUAGE_MAP

    return StartStoryBuilderUseCase(
        word_repo=get_word_repository(),
        game_repo=get_game_session_repository(),
        ai_provider=_get_ai_provider(),
        user_repo=get_user_repository(),
        language_map=NATIVE_LANGUAGE_MAP,
    )


def get_story_builder_submit_use_case() -> SubmitStoryRoundUseCase:
    from core.services.ai.prompts import NATIVE_LANGUAGE_MAP

    try:
        from .challenge_deps import get_challenge_repository
        challenge_repo = get_challenge_repository()
    except Exception:
        challenge_repo = None

    try:
        from apps.users.presentation.progress_dependencies import get_xp_service
        xp_service = get_xp_service()
    except Exception:
        xp_service = None

    return SubmitStoryRoundUseCase(
        word_repo=get_word_repository(),
        game_repo=get_game_session_repository(),
        ai_provider=_get_ai_provider(),
        sr_service=get_sr_service(),
        xp_service=xp_service,
        user_repo=get_user_repository(),
        language_map=NATIVE_LANGUAGE_MAP,
        challenge_repo=challenge_repo,
    )


def get_story_builder_complete_use_case() -> CompleteStoryBuilderUseCase:
    try:
        from apps.users.presentation.progress_dependencies import (
            get_xp_service,
            get_badge_service,
        )
        xp_service = get_xp_service()
        badge_service = get_badge_service()
    except Exception:
        xp_service = None
        badge_service = None

    return CompleteStoryBuilderUseCase(
        game_repo=get_game_session_repository(),
        xp_service=xp_service,
        badge_service=badge_service,
    )


# =============================================================================
# Listening Challenge
# =============================================================================


def get_listening_start_use_case() -> StartListeningChallengeUseCase:
    return StartListeningChallengeUseCase(
        word_repo=get_word_repository(),
        game_repo=get_game_session_repository(),
        tts_provider=_get_tts_provider(),
    )


def get_listening_answer_use_case() -> SubmitListeningAnswerUseCase:
    try:
        from apps.users.presentation.progress_dependencies import get_xp_service
        xp_service = get_xp_service()
    except Exception:
        xp_service = None

    try:
        from .challenge_deps import get_challenge_repository
        challenge_repo = get_challenge_repository()
    except Exception:
        challenge_repo = None

    return SubmitListeningAnswerUseCase(
        word_repo=get_word_repository(),
        game_repo=get_game_session_repository(),
        sr_service=get_sr_service(),
        xp_service=xp_service,
        challenge_repo=challenge_repo,
    )


def get_listening_complete_use_case() -> CompleteListeningChallengeUseCase:
    try:
        from apps.users.presentation.progress_dependencies import (
            get_xp_service,
            get_badge_service,
        )
        xp_service = get_xp_service()
        badge_service = get_badge_service()
    except Exception:
        xp_service = None
        badge_service = None

    return CompleteListeningChallengeUseCase(
        game_repo=get_game_session_repository(),
        xp_service=xp_service,
        badge_service=badge_service,
    )


# =============================================================================
# Synonym & Antonym
# =============================================================================


def get_synonym_antonym_start_use_case() -> StartSynonymAntonymUseCase:
    return StartSynonymAntonymUseCase(
        word_repo=get_word_repository(),
        game_repo=get_game_session_repository(),
        ai_provider=_get_ai_provider(),
        user_repo=get_user_repository(),
    )


def get_synonym_antonym_answer_use_case() -> SubmitSynonymAntonymUseCase:
    try:
        from apps.users.presentation.progress_dependencies import get_xp_service
        xp_service = get_xp_service()
    except Exception:
        xp_service = None

    try:
        from .challenge_deps import get_challenge_repository
        challenge_repo = get_challenge_repository()
    except Exception:
        challenge_repo = None

    return SubmitSynonymAntonymUseCase(
        word_repo=get_word_repository(),
        game_repo=get_game_session_repository(),
        sr_service=get_sr_service(),
        xp_service=xp_service,
        challenge_repo=challenge_repo,
    )


def get_synonym_antonym_complete_use_case() -> CompleteSynonymAntonymUseCase:
    try:
        from apps.users.presentation.progress_dependencies import (
            get_xp_service,
            get_badge_service,
        )
        xp_service = get_xp_service()
        badge_service = get_badge_service()
    except Exception:
        xp_service = None
        badge_service = None

    return CompleteSynonymAntonymUseCase(
        game_repo=get_game_session_repository(),
        xp_service=xp_service,
        badge_service=badge_service,
    )


# =============================================================================
# Irregular Verbs
# =============================================================================


def get_irregular_verbs_start_use_case() -> StartIrregularVerbsUseCase:
    return StartIrregularVerbsUseCase(
        game_repo=get_game_session_repository(),
        user_repo=get_user_repository(),
    )


def get_irregular_verbs_answer_use_case() -> SubmitIrregularVerbUseCase:
    try:
        from apps.users.presentation.progress_dependencies import get_xp_service
        xp_service = get_xp_service()
    except Exception:
        xp_service = None

    try:
        from .challenge_deps import get_challenge_repository
        challenge_repo = get_challenge_repository()
    except Exception:
        challenge_repo = None

    return SubmitIrregularVerbUseCase(
        game_repo=get_game_session_repository(),
        xp_service=xp_service,
        challenge_repo=challenge_repo,
    )


def get_irregular_verbs_complete_use_case() -> CompleteIrregularVerbsUseCase:
    try:
        from apps.users.presentation.progress_dependencies import (
            get_xp_service,
            get_badge_service,
        )
        xp_service = get_xp_service()
        badge_service = get_badge_service()
    except Exception:
        xp_service = None
        badge_service = None

    return CompleteIrregularVerbsUseCase(
        game_repo=get_game_session_repository(),
        xp_service=xp_service,
        badge_service=badge_service,
    )
