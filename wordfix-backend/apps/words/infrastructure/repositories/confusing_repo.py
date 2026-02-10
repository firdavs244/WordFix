"""
ConfusingPair repository implementation using Django ORM.
"""

from uuid import UUID

from django.utils import timezone

from apps.common.exceptions import EntityNotFoundError
from apps.words.domain.entities import ConfusingPairEntity
from apps.words.domain.repositories import AbstractConfusingPairRepository
from apps.words.infrastructure.models import ConfusingPair


class DjangoConfusingPairRepository(AbstractConfusingPairRepository):
    """Concrete implementation of AbstractConfusingPairRepository."""

    def _to_entity(self, pair: ConfusingPair) -> ConfusingPairEntity:
        return ConfusingPairEntity(
            id=pair.id,
            user_id=pair.user_id,
            word_1_id=pair.word_1_id,
            word_2_id=pair.word_2_id,
            confusion_count=pair.confusion_count,
            last_confused_at=pair.last_confused_at,
            is_resolved=pair.is_resolved,
            drill_data=pair.drill_data,
            is_active=pair.is_active,
            created_at=pair.created_at,
            updated_at=pair.updated_at,
        )

    def get_or_create(self, user_id: UUID, word_1_id: UUID, word_2_id: UUID) -> tuple[ConfusingPairEntity, bool]:
        # Always store the smaller ID first for consistency
        if str(word_1_id) > str(word_2_id):
            word_1_id, word_2_id = word_2_id, word_1_id

        pair, created = ConfusingPair.objects.get_or_create(
            user_id=user_id,
            word_1_id=word_1_id,
            word_2_id=word_2_id,
            defaults={"confusion_count": 1},
        )
        return self._to_entity(pair), created

    def increment_confusion(self, pair_id: UUID) -> ConfusingPairEntity:
        try:
            pair = ConfusingPair.objects.get(id=pair_id)
        except ConfusingPair.DoesNotExist:
            raise EntityNotFoundError("Confusing pair not found.")
        pair.confusion_count += 1
        pair.is_resolved = False
        pair.save(update_fields=["confusion_count", "is_resolved", "last_confused_at", "updated_at"])
        return self._to_entity(pair)

    def get_by_user(self, user_id: UUID, include_resolved: bool = False) -> list[ConfusingPairEntity]:
        qs = ConfusingPair.objects.filter(user_id=user_id)
        if not include_resolved:
            qs = qs.filter(is_resolved=False)
        return [self._to_entity(p) for p in qs]

    def get_by_id(self, pair_id: UUID, user_id: UUID) -> ConfusingPairEntity:
        try:
            pair = ConfusingPair.objects.get(id=pair_id, user_id=user_id)
        except ConfusingPair.DoesNotExist:
            raise EntityNotFoundError("Confusing pair not found.")
        return self._to_entity(pair)

    def update(self, pair_id: UUID, **kwargs) -> ConfusingPairEntity:
        try:
            pair = ConfusingPair.objects.get(id=pair_id)
        except ConfusingPair.DoesNotExist:
            raise EntityNotFoundError("Confusing pair not found.")
        for field, value in kwargs.items():
            setattr(pair, field, value)
        pair.save()
        return self._to_entity(pair)

    def resolve(self, pair_id: UUID) -> ConfusingPairEntity:
        try:
            pair = ConfusingPair.objects.get(id=pair_id)
        except ConfusingPair.DoesNotExist:
            raise EntityNotFoundError("Confusing pair not found.")
        pair.is_resolved = True
        pair.save(update_fields=["is_resolved", "updated_at"])
        return self._to_entity(pair)

    def get_unresolved_count(self, user_id: UUID) -> int:
        return ConfusingPair.objects.filter(user_id=user_id, is_resolved=False).count()
