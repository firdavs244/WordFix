"""
Chat use-case factories.
"""

from apps.words.application.use_cases import (
    EndChatUseCase,
    GetChatHistoryUseCase,
    GetChatSessionDetailUseCase,
    SendChatMessageUseCase,
    StartChatUseCase,
)
from .common_deps import (
    _get_ai_provider,
    get_chat_repository,
    get_sr_service,
    get_user_repository,
    get_word_repository,
)


def get_start_chat_use_case() -> StartChatUseCase:
    from core.services.ai.prompts import CHAT_SYSTEM_PROMPT, NATIVE_LANGUAGE_MAP

    return StartChatUseCase(
        chat_repo=get_chat_repository(),
        word_repo=get_word_repository(),
        ai_provider=_get_ai_provider(),
        user_repo=get_user_repository(),
        prompt_template=CHAT_SYSTEM_PROMPT,
        language_map=NATIVE_LANGUAGE_MAP,
    )


def get_send_chat_message_use_case() -> SendChatMessageUseCase:
    from core.services.ai.prompts import CHAT_SYSTEM_PROMPT, NATIVE_LANGUAGE_MAP

    return SendChatMessageUseCase(
        chat_repo=get_chat_repository(),
        ai_provider=_get_ai_provider(),
        word_repo=get_word_repository(),
        user_repo=get_user_repository(),
        sr_service=get_sr_service(),
        prompt_template=CHAT_SYSTEM_PROMPT,
        language_map=NATIVE_LANGUAGE_MAP,
    )


def get_end_chat_use_case() -> EndChatUseCase:
    return EndChatUseCase(chat_repo=get_chat_repository())


def get_chat_history_use_case() -> GetChatHistoryUseCase:
    return GetChatHistoryUseCase(chat_repo=get_chat_repository())


def get_chat_session_detail_use_case() -> GetChatSessionDetailUseCase:
    return GetChatSessionDetailUseCase(chat_repo=get_chat_repository())
