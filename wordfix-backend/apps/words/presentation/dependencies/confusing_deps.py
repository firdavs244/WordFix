"""
Confusing pairs dependency injection.
"""

from apps.words.application.use_cases.confusing_pairs import (
    DetectConfusionUseCase,
    GenerateConfusionDrillUseCase,
    GetConfusingPairCountUseCase,
    GetConfusingPairDetailUseCase,
    GetConfusingPairsUseCase,
    ResolveConfusingPairUseCase,
)
from .common_deps import (
    _get_ai_provider,
    get_user_repository,
    get_word_repository,
)


def get_confusing_pair_repository():
    from apps.words.infrastructure.repositories import DjangoConfusingPairRepository
    return DjangoConfusingPairRepository()


def get_detect_confusion_use_case() -> DetectConfusionUseCase:
    return DetectConfusionUseCase(
        word_repo=get_word_repository(),
        confusing_pair_repo=get_confusing_pair_repository(),
    )


def get_confusing_pairs_use_case() -> GetConfusingPairsUseCase:
    return GetConfusingPairsUseCase(
        confusing_pair_repo=get_confusing_pair_repository(),
        word_repo=get_word_repository(),
    )


def get_confusing_pair_detail_use_case() -> GetConfusingPairDetailUseCase:
    return GetConfusingPairDetailUseCase(
        confusing_pair_repo=get_confusing_pair_repository(),
        word_repo=get_word_repository(),
    )


def get_generate_drill_use_case() -> GenerateConfusionDrillUseCase:
    from core.services.ai.prompts import CONFUSING_PAIR_DRILL_PROMPT, NATIVE_LANGUAGE_MAP

    return GenerateConfusionDrillUseCase(
        confusing_pair_repo=get_confusing_pair_repository(),
        word_repo=get_word_repository(),
        ai_provider=_get_ai_provider(),
        user_repo=get_user_repository(),
        prompt_template=CONFUSING_PAIR_DRILL_PROMPT,
        language_map=NATIVE_LANGUAGE_MAP,
    )


def get_resolve_pair_use_case() -> ResolveConfusingPairUseCase:
    return ResolveConfusingPairUseCase(
        confusing_pair_repo=get_confusing_pair_repository(),
    )


def get_confusing_pair_count_use_case() -> GetConfusingPairCountUseCase:
    return GetConfusingPairCountUseCase(
        confusing_pair_repo=get_confusing_pair_repository(),
    )
