"""
Distractor service dependency injection.
"""

from core.services.ai.distractor_service import DistractorGeneratorService
from .common_deps import _get_ai_provider, get_word_repository


def get_distractor_repository():
    from apps.words.infrastructure.repositories import DjangoWordDistractorRepository
    return DjangoWordDistractorRepository()


def get_distractor_service() -> DistractorGeneratorService:
    return DistractorGeneratorService(
        ai_provider=_get_ai_provider(),
        word_repo=get_word_repository(),
        distractor_repo=get_distractor_repository(),
    )
