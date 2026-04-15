"""
Immersive game use-case factories (dependency injection).
"""

from django.conf import settings

from apps.immersive.application.use_cases.conversation_use_cases import (
    RequestHintUseCase,
    SubmitResponseUseCase,
    SubmitVoiceResponseUseCase,
)
from apps.immersive.application.use_cases.scenario_use_cases import (
    GetScenarioDetailUseCase,
    ListScenariosUseCase,
)
from apps.immersive.application.use_cases.session_use_cases import (
    CompleteImmersiveSessionUseCase,
    StartImmersiveSessionUseCase,
)
from apps.immersive.domain.services.scoring_service import ImmersiveScoringService
from apps.immersive.infrastructure.repositories.scenario_repo import DjangoScenarioRepository
from apps.immersive.infrastructure.repositories.session_repo import DjangoSessionRepository
from apps.immersive.infrastructure.services.groq_stt_service import GroqSTTService


LANGUAGE_MAP = {
    "uz": "Uzbek", "en": "English", "ru": "Russian",
    "ko": "Korean", "de": "German", "fr": "French",
    "es": "Spanish", "ja": "Japanese", "zh": "Chinese",
}


def _get_scenario_repo():
    return DjangoScenarioRepository()


def _get_session_repo():
    return DjangoSessionRepository()


def _get_scoring_service():
    return ImmersiveScoringService()


def _get_ai_provider():
    try:
        from core.services.ai.provider_factory import AIProviderFactory
        return AIProviderFactory.get_provider()
    except Exception:
        return None


def _get_tts_provider():
    try:
        from core.services.tts.google_tts import GoogleTTSProvider
        return GoogleTTSProvider()
    except Exception:
        return None


def _get_stt_service():
    return GroqSTTService()


def _get_user_repo():
    try:
        from apps.users.infrastructure.repositories import DjangoUserRepository
        return DjangoUserRepository()
    except Exception:
        return None


def _get_xp_service():
    try:
        from apps.words.presentation.dependencies.common_deps import get_xp_service
        return get_xp_service()
    except Exception:
        return None


def _get_badge_service():
    try:
        from apps.words.presentation.dependencies.common_deps import get_badge_service
        return get_badge_service()
    except Exception:
        return None


def get_list_scenarios_use_case():
    return ListScenariosUseCase(scenario_repo=_get_scenario_repo())


def get_scenario_detail_use_case():
    return GetScenarioDetailUseCase(scenario_repo=_get_scenario_repo())


def get_start_session_use_case():
    return StartImmersiveSessionUseCase(
        session_repo=_get_session_repo(),
        scenario_repo=_get_scenario_repo(),
        ai_provider=_get_ai_provider(),
        tts_provider=_get_tts_provider(),
        user_repo=_get_user_repo(),
        language_map=LANGUAGE_MAP,
    )


def get_submit_response_use_case():
    return SubmitResponseUseCase(
        session_repo=_get_session_repo(),
        scenario_repo=_get_scenario_repo(),
        ai_provider=_get_ai_provider(),
        scoring_service=_get_scoring_service(),
        tts_provider=_get_tts_provider(),
        user_repo=_get_user_repo(),
        language_map=LANGUAGE_MAP,
    )


def get_submit_voice_response_use_case():
    return SubmitVoiceResponseUseCase(
        stt_service=_get_stt_service(),
        submit_response_use_case=get_submit_response_use_case(),
    )


def get_complete_session_use_case():
    return CompleteImmersiveSessionUseCase(
        session_repo=_get_session_repo(),
        scoring_service=_get_scoring_service(),
        xp_service=_get_xp_service(),
        badge_service=_get_badge_service(),
    )


def get_request_hint_use_case():
    return RequestHintUseCase(
        session_repo=_get_session_repo(),
        scenario_repo=_get_scenario_repo(),
        ai_provider=_get_ai_provider(),
        user_repo=_get_user_repo(),
        language_map=LANGUAGE_MAP,
    )
