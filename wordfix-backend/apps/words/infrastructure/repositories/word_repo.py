"""
Word & WordCategory repository implementations using Django ORM.
"""

from uuid import UUID

from django.core.cache import cache
from django.db.models import Q
from django.utils import timezone

from apps.common.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from apps.words.domain.entities import (
    WordCategoryEntity,
    WordEntity,
)
from apps.words.domain.repositories import (
    AbstractWordCategoryRepository,
    AbstractWordRepository,
)
from apps.words.infrastructure.models import (
    Word,
    WordCategory,
)
from apps.words.infrastructure.repositories.word_stats_repo import WordStatsMixin


class DjangoWordRepository(WordStatsMixin, AbstractWordRepository):
    """Concrete implementation of AbstractWordRepository."""

    @staticmethod
    def _invalidate_user_cache(user_id: UUID):
        """Invalidate all cached analytics data for this user."""
        cache.delete(f"word_count_{user_id}")
        cache.delete(f"word_stats_{user_id}")
        cache.delete(f"analytics_overview_{user_id}")
        cache.delete(f"weekly_stats_{user_id}")
        cache.delete(f"word_progress_{user_id}")

    def _to_entity(self, word: Word) -> WordEntity:
        """Convert Word model to WordEntity."""
        category_entity = None
        if word.category:
            category_entity = WordCategoryEntity(
                id=word.category.id,
                user_id=word.category.user_id,
                name=word.category.name,
                color=word.category.color,
                icon=word.category.icon,
                words_count=word.category.words_count,
            )

        return WordEntity(
            id=word.id,
            user_id=word.user_id,
            original_word=word.original_word,
            translation=word.translation,
            pronunciation=word.pronunciation,
            part_of_speech=word.part_of_speech,
            definition=word.definition,
            example_sentence=word.example_sentence,
            example_translation=word.example_translation,
            synonyms=word.synonyms,
            antonyms=word.antonyms,
            collocations=word.collocations,
            word_family=word.word_family,
            image_url=word.image_url,
            audio_url=word.audio_url,
            notes=word.notes,
            mnemonic=word.mnemonic,
            usage_notes=word.usage_notes,
            category_id=word.category_id,
            category=category_entity,
            tags=word.tags,
            difficulty_level=word.difficulty_level,
            is_enriched=word.is_enriched,
            enrichment_status=word.enrichment_status,
            enrichment_error=word.enrichment_error,
            enriched_at=word.enriched_at,
            confidence_score=word.confidence_score,
            next_review_at=word.next_review_at,
            review_count=word.review_count,
            correct_count=word.correct_count,
            incorrect_count=word.incorrect_count,
            last_reviewed_at=word.last_reviewed_at,
            is_mastered=word.is_mastered,
            easiness_factor=word.easiness_factor,
            repetition_number=word.repetition_number,
            interval_days=word.interval_days,
            is_archived=word.is_archived,
            archived_at=word.archived_at,
            is_active=word.is_active,
            created_at=word.created_at,
            updated_at=word.updated_at,
        )

    def get_by_id(self, word_id: UUID, user_id: UUID) -> WordEntity:
        try:
            word = Word.objects.select_related("category").get(id=word_id, user_id=user_id)
            return self._to_entity(word)
        except Word.DoesNotExist:
            raise EntityNotFoundError("Word not found.")

    def get_all_by_user(
        self, user_id: UUID, filters: dict | None = None,
        ordering: str = "-created_at", page: int = 1, page_size: int = 20,
    ) -> tuple[list[WordEntity], int]:
        qs = Word.objects.filter(user_id=user_id, is_archived=False).select_related("category")

        if filters:
            if filters.get("category_id"):
                qs = qs.filter(category_id=filters["category_id"])
            if filters.get("difficulty_level"):
                qs = qs.filter(difficulty_level=filters["difficulty_level"])
            if "is_mastered" in filters:
                qs = qs.filter(is_mastered=filters["is_mastered"])
            if "is_enriched" in filters:
                qs = qs.filter(is_enriched=filters["is_enriched"])
            if filters.get("part_of_speech"):
                qs = qs.filter(part_of_speech=filters["part_of_speech"])
            if filters.get("search"):
                query = filters["search"]
                qs = qs.filter(
                    Q(original_word__icontains=query) | Q(translation__icontains=query)
                )

        # Ordering
        allowed_ordering = {
            "created_at", "-created_at",
            "original_word", "-original_word",
            "confidence_score", "-confidence_score",
        }
        if ordering not in allowed_ordering:
            ordering = "-created_at"

        total = qs.count()
        qs = qs.order_by(ordering)

        # Pagination
        start = (page - 1) * page_size
        end = start + page_size
        words = [self._to_entity(w) for w in qs[start:end]]

        return words, total

    def create(self, user_id: UUID, **kwargs) -> WordEntity:
        original_word = kwargs.get("original_word", "").strip().lower()
        if Word.objects.filter(user_id=user_id, original_word__iexact=original_word).exists():
            raise EntityAlreadyExistsError(
                f"Word '{original_word}' already exists in your word bank."
            )
        kwargs["original_word"] = original_word
        word = Word.objects.create(user_id=user_id, **kwargs)
        word = Word.objects.select_related("category").get(id=word.id)
        self._invalidate_user_cache(user_id)
        return self._to_entity(word)

    def update(self, word_id: UUID, user_id: UUID, **kwargs) -> WordEntity:
        try:
            word = Word.objects.get(id=word_id, user_id=user_id)
        except Word.DoesNotExist:
            raise EntityNotFoundError("Word not found.")

        for field, value in kwargs.items():
            setattr(word, field, value)
        word.save()
        word = Word.objects.select_related("category").get(id=word.id)
        self._invalidate_user_cache(user_id)
        return self._to_entity(word)

    def delete(self, word_id: UUID, user_id: UUID) -> None:
        try:
            word = Word.objects.get(id=word_id, user_id=user_id)
        except Word.DoesNotExist:
            raise EntityNotFoundError("Word not found.")
        word.delete()
        self._invalidate_user_cache(user_id)

    def exists(self, original_word: str, user_id: UUID) -> bool:
        return Word.objects.filter(
            user_id=user_id, original_word__iexact=original_word.strip()
        ).exists()

    def get_count_by_user(self, user_id: UUID) -> int:
        cache_key = f"word_count_{user_id}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
        count = Word.objects.filter(user_id=user_id, is_archived=False).count()
        cache.set(cache_key, count, timeout=120)  # 2 min
        return count

    def search(
        self, user_id: UUID, query: str, page: int = 1, page_size: int = 20,
    ) -> tuple[list[WordEntity], int]:
        qs = Word.objects.filter(
            user_id=user_id,
            is_archived=False,
        ).filter(
            Q(original_word__icontains=query) | Q(translation__icontains=query)
        ).select_related("category")

        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        words = [self._to_entity(w) for w in qs[start:end]]
        return words, total

    def get_by_category(self, user_id: UUID, category_id: UUID) -> list[WordEntity]:
        qs = Word.objects.filter(
            user_id=user_id, category_id=category_id, is_archived=False
        ).select_related("category")
        return [self._to_entity(w) for w in qs]

    def bulk_create(self, user_id: UUID, words_data: list[dict]) -> dict:
        created = 0
        skipped = 0
        errors = []

        for item in words_data:
            original_word = item.get("original_word", "").strip().lower()
            if not original_word:
                errors.append({"word": original_word, "error": "Word is required."})
                continue

            if Word.objects.filter(user_id=user_id, original_word__iexact=original_word).exists():
                skipped += 1
                continue

            try:
                Word.objects.create(
                    user_id=user_id,
                    original_word=original_word,
                    translation=item.get("translation", ""),
                    difficulty_level=item.get("difficulty_level", "medium"),
                    notes=item.get("notes", ""),
                    tags=item.get("tags", []),
                )
                created += 1
            except Exception as e:
                errors.append({"word": original_word, "error": str(e)})

        return {"created": created, "skipped": skipped, "errors": errors}

    # ─── Archive methods ──────────────────────────────────────────────────────

    def archive_word(self, user_id: UUID, word_id: UUID) -> WordEntity:
        try:
            word = Word.objects.get(id=word_id, user_id=user_id)
        except Word.DoesNotExist:
            raise EntityNotFoundError("Word not found.")
        word.is_archived = True
        word.archived_at = timezone.now()
        word.save(update_fields=["is_archived", "archived_at", "updated_at"])
        self._invalidate_user_cache(user_id)
        return self._to_entity(Word.objects.select_related("category").get(id=word.id))

    def unarchive_word(self, user_id: UUID, word_id: UUID) -> WordEntity:
        try:
            word = Word.objects.get(id=word_id, user_id=user_id)
        except Word.DoesNotExist:
            raise EntityNotFoundError("Word not found.")
        word.is_archived = False
        word.archived_at = None
        word.save(update_fields=["is_archived", "archived_at", "updated_at"])
        self._invalidate_user_cache(user_id)
        return self._to_entity(Word.objects.select_related("category").get(id=word.id))

    def get_archived_words(
        self, user_id: UUID, page: int = 1, page_size: int = 20,
    ) -> tuple[list[WordEntity], int]:
        qs = Word.objects.filter(
            user_id=user_id, is_archived=True
        ).select_related("category").order_by("-archived_at")
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        words = [self._to_entity(w) for w in qs[start:end]]
        return words, total

    def bulk_archive(self, user_id: UUID, word_ids: list[UUID]) -> int:
        now = timezone.now()
        count = Word.objects.filter(
            id__in=word_ids, user_id=user_id, is_archived=False,
        ).update(is_archived=True, archived_at=now)
        self._invalidate_user_cache(user_id)
        return count


class DjangoWordCategoryRepository(AbstractWordCategoryRepository):
    """Concrete implementation of AbstractWordCategoryRepository."""

    def _to_entity(self, cat: WordCategory) -> WordCategoryEntity:
        return WordCategoryEntity(
            id=cat.id,
            user_id=cat.user_id,
            name=cat.name,
            color=cat.color,
            icon=cat.icon,
            words_count=cat.words_count,
            is_active=cat.is_active,
            created_at=cat.created_at,
            updated_at=cat.updated_at,
        )

    def get_all_by_user(self, user_id: UUID) -> list[WordCategoryEntity]:
        qs = WordCategory.objects.filter(user_id=user_id)
        return [self._to_entity(c) for c in qs]

    def create(self, user_id: UUID, **kwargs) -> WordCategoryEntity:
        name = kwargs.get("name", "").strip()
        if WordCategory.objects.filter(user_id=user_id, name__iexact=name).exists():
            raise EntityAlreadyExistsError(f"Category '{name}' already exists.")
        cat = WordCategory.objects.create(user_id=user_id, **kwargs)
        return self._to_entity(cat)

    def delete(self, category_id: UUID, user_id: UUID) -> None:
        try:
            cat = WordCategory.objects.get(id=category_id, user_id=user_id)
        except WordCategory.DoesNotExist:
            raise EntityNotFoundError("Category not found.")
        cat.delete()

    def exists(self, name: str, user_id: UUID) -> bool:
        return WordCategory.objects.filter(
            user_id=user_id, name__iexact=name.strip()
        ).exists()

    def update_words_count(self, category_id: UUID) -> None:
        try:
            cat = WordCategory.objects.get(id=category_id)
        except WordCategory.DoesNotExist:
            raise EntityNotFoundError("Category not found.")
        cat.words_count = Word.objects.filter(category_id=category_id).count()
        cat.save(update_fields=["words_count", "updated_at"])
