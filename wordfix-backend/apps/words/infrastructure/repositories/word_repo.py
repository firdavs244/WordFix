"""
Word & WordCategory repository implementations using Django ORM.
"""

from uuid import UUID

from django.db.models import Count, Q, Avg
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


class DjangoWordRepository(AbstractWordRepository):
    """Concrete implementation of AbstractWordRepository."""

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
        qs = Word.objects.filter(user_id=user_id).select_related("category")

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
        return self._to_entity(word)

    def delete(self, word_id: UUID, user_id: UUID) -> None:
        try:
            word = Word.objects.get(id=word_id, user_id=user_id)
        except Word.DoesNotExist:
            raise EntityNotFoundError("Word not found.")
        word.delete()

    def exists(self, original_word: str, user_id: UUID) -> bool:
        return Word.objects.filter(
            user_id=user_id, original_word__iexact=original_word.strip()
        ).exists()

    def get_count_by_user(self, user_id: UUID) -> int:
        return Word.objects.filter(user_id=user_id).count()

    def search(
        self, user_id: UUID, query: str, page: int = 1, page_size: int = 20,
    ) -> tuple[list[WordEntity], int]:
        qs = Word.objects.filter(
            user_id=user_id,
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
            user_id=user_id, category_id=category_id
        ).select_related("category")
        return [self._to_entity(w) for w in qs]

    def get_words_for_review(self, user_id: UUID) -> list[WordEntity]:
        now = timezone.now()
        qs = Word.objects.filter(
            user_id=user_id,
            is_mastered=False,
        ).filter(
            Q(next_review_at__isnull=True) | Q(next_review_at__lte=now)
        ).select_related("category").order_by("confidence_score")[:20]
        return [self._to_entity(w) for w in qs]

    def get_review_words(
        self, user_id: UUID, limit: int = 20, session_type: str = "review",
    ) -> list[WordEntity]:
        """Get words due for review based on session type."""
        now = timezone.now()

        if session_type == "quick":
            limit = 5

        if session_type == "focus":
            qs = Word.objects.filter(
                user_id=user_id,
                is_mastered=False,
                confidence_score__lt=30,
            ).select_related("category").order_by("confidence_score")[:limit]
            return [self._to_entity(w) for w in qs]

        # Due words + some new words
        due_qs = Word.objects.filter(
            user_id=user_id,
            is_mastered=False,
            next_review_at__lte=now,
        ).select_related("category").order_by("next_review_at")

        new_qs = Word.objects.filter(
            user_id=user_id,
            is_mastered=False,
            next_review_at__isnull=True,
        ).select_related("category").order_by("created_at")[:5]

        due_list = list(due_qs[:limit])
        remaining = limit - len(due_list)
        if remaining > 0:
            due_list.extend(list(new_qs[:remaining]))

        return [self._to_entity(w) for w in due_list]

    def get_review_summary_stats(self, user_id: UUID) -> dict:
        """Get review summary statistics for a user."""
        from datetime import timedelta

        now = timezone.now()

        total = Word.objects.filter(user_id=user_id).count()
        mastered = Word.objects.filter(user_id=user_id, is_mastered=True).count()
        due_today = Word.objects.filter(
            user_id=user_id, is_mastered=False, next_review_at__lte=now
        ).count()
        overdue = Word.objects.filter(
            user_id=user_id, is_mastered=False,
            next_review_at__lt=now - timedelta(days=1)
        ).count()
        new_words = Word.objects.filter(
            user_id=user_id, next_review_at__isnull=True
        ).count()
        learning = total - mastered - new_words

        next_word = Word.objects.filter(
            user_id=user_id, is_mastered=False, next_review_at__gt=now
        ).order_by("next_review_at").first()
        next_review_time = next_word.next_review_at.isoformat() if next_word else None

        # Aggregate review stats
        from django.db.models import Sum
        review_agg = Word.objects.filter(user_id=user_id).aggregate(
            total_reviews=Sum("review_count"),
            total_correct=Sum("correct_count"),
        )
        total_reviews_agg = review_agg["total_reviews"] or 0
        total_correct_agg = review_agg["total_correct"] or 0

        return {
            "total_words": total,
            "due_today": due_today + new_words,
            "overdue": overdue,
            "mastered": mastered,
            "learning": learning,
            "new": new_words,
            "next_review_time": next_review_time,
            "total_reviews": total_reviews_agg,
            "total_correct": total_correct_agg,
        }

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

    def get_stats(self, user_id: UUID) -> dict:
        qs = Word.objects.filter(user_id=user_id)
        total = qs.count()
        if total == 0:
            return {
                "total": 0,
                "mastered": 0,
                "learning": 0,
                "new": 0,
                "by_difficulty": {"easy": 0, "medium": 0, "hard": 0},
                "by_category": [],
                "average_confidence": 0,
            }

        mastered = qs.filter(is_mastered=True).count()
        learning = qs.filter(is_mastered=False, review_count__gt=0).count()
        new_words = qs.filter(review_count=0).count()

        by_difficulty = {}
        for level in ("easy", "medium", "hard"):
            by_difficulty[level] = qs.filter(difficulty_level=level).count()

        by_category = list(
            qs.values("category__name", "category__color", "category__icon")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        by_category_formatted = [
            {
                "name": c["category__name"] or "Uncategorized",
                "color": c["category__color"] or "#6C5CE7",
                "icon": c["category__icon"] or "book",
                "count": c["count"],
            }
            for c in by_category
        ]

        avg_confidence = qs.aggregate(avg=Avg("confidence_score"))["avg"] or 0

        return {
            "total": total,
            "mastered": mastered,
            "learning": learning,
            "new": new_words,
            "by_difficulty": by_difficulty,
            "by_category": by_category_formatted,
            "average_confidence": round(avg_confidence, 1),
        }


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
