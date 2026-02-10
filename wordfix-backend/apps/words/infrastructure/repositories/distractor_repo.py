"""
WordDistractor repository implementation using Django ORM.
"""

from uuid import UUID

from apps.words.domain.entities import WordDistractorEntity
from apps.words.domain.repositories import AbstractWordDistractorRepository
from apps.words.infrastructure.models import WordDistractor


class DjangoWordDistractorRepository(AbstractWordDistractorRepository):
    """Concrete implementation of AbstractWordDistractorRepository."""

    def _to_entity(self, distractor: WordDistractor) -> WordDistractorEntity:
        return WordDistractorEntity(
            id=distractor.id,
            word_id=distractor.word_id,
            distractors=distractor.distractors,
            language=distractor.language,
            generated_by=distractor.generated_by,
            is_active=distractor.is_active,
            created_at=distractor.created_at,
            updated_at=distractor.updated_at,
        )

    def get_by_word(self, word_id: UUID, language: str = "uz") -> WordDistractorEntity | None:
        try:
            distractor = WordDistractor.objects.get(word_id=word_id, language=language)
            return self._to_entity(distractor)
        except WordDistractor.DoesNotExist:
            return None

    def create(self, word_id: UUID, distractors: list, language: str = "uz",
               generated_by: str = "ai") -> WordDistractorEntity:
        distractor = WordDistractor.objects.create(
            word_id=word_id,
            distractors=distractors,
            language=language,
            generated_by=generated_by,
        )
        return self._to_entity(distractor)

    def update_or_create(self, word_id: UUID, distractors: list, language: str = "uz",
                         generated_by: str = "ai") -> WordDistractorEntity:
        distractor, _ = WordDistractor.objects.update_or_create(
            word_id=word_id,
            language=language,
            defaults={
                "distractors": distractors,
                "generated_by": generated_by,
            },
        )
        return self._to_entity(distractor)
