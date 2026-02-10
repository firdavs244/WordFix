"""
Test use-case factories.
"""

from apps.words.application.use_cases import (
    CompleteTestSessionUseCase,
    GenerateTestUseCase,
    GetTestDetailUseCase,
    GetTestHistoryUseCase,
    SubmitTestAnswerUseCase,
)
from .common_deps import (
    _get_ai_provider,
    get_activity_repository,
    get_sr_service,
    get_test_question_repository,
    get_test_session_repository,
    get_user_repository,
    get_word_repository,
)


def get_generate_test_use_case() -> GenerateTestUseCase:
    from core.services.ai.prompts import (
        CONTEXT_GUESS_PROMPT,
        FILL_BLANK_PROMPT,
        MULTIPLE_CHOICE_PROMPT,
        NATIVE_LANGUAGE_MAP,
    )

    return GenerateTestUseCase(
        word_repo=get_word_repository(),
        test_session_repo=get_test_session_repository(),
        test_question_repo=get_test_question_repository(),
        ai_provider=_get_ai_provider(),
        user_repo=get_user_repository(),
        prompt_templates={
            "multiple_choice": MULTIPLE_CHOICE_PROMPT,
            "fill_blank": FILL_BLANK_PROMPT,
            "context_guess": CONTEXT_GUESS_PROMPT,
        },
        language_map=NATIVE_LANGUAGE_MAP,
    )


def get_submit_test_answer_use_case() -> SubmitTestAnswerUseCase:
    from .confusing_deps import get_confusing_pair_repository
    from .challenge_deps import get_challenge_repository

    return SubmitTestAnswerUseCase(
        question_repo=get_test_question_repository(),
        word_repo=get_word_repository(),
        sr_service=get_sr_service(),
        activity_repo=get_activity_repository(),
        test_session_repo=get_test_session_repository(),
        confusing_pair_repo=get_confusing_pair_repository(),
        challenge_repo=get_challenge_repository(),
    )


def get_complete_test_session_use_case() -> CompleteTestSessionUseCase:
    from .challenge_deps import get_challenge_repository

    return CompleteTestSessionUseCase(
        test_session_repo=get_test_session_repository(),
        test_question_repo=get_test_question_repository(),
        activity_repo=get_activity_repository(),
        challenge_repo=get_challenge_repository(),
    )


def get_test_history_use_case() -> GetTestHistoryUseCase:
    return GetTestHistoryUseCase(
        test_session_repo=get_test_session_repository(),
    )


def get_test_detail_use_case() -> GetTestDetailUseCase:
    return GetTestDetailUseCase(
        test_session_repo=get_test_session_repository(),
        test_question_repo=get_test_question_repository(),
    )
