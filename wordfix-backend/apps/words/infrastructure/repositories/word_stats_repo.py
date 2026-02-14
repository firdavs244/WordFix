"""
Word statistics & review repository methods (extracted from word_repo.py).

Provides ``WordStatsMixin`` which is mixed into ``DjangoWordRepository``
so all existing call-sites keep working.
"""

from uuid import UUID

from django.core.cache import cache
from django.db.models import Avg, Count, Q, Sum
from django.utils import timezone

from apps.words.domain.entities import WordEntity


class WordStatsMixin:
    """Stats / review helpers for DjangoWordRepository.

    Expects the host class to expose ``_to_entity(word) -> WordEntity``
    and the ``Word`` model to be importable.
    """

    # ── review helpers ───────────────────────────────────────────

    def get_words_for_review(self, user_id: UUID) -> list[WordEntity]:
        from apps.words.infrastructure.models import Word

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
        from apps.words.infrastructure.models import Word

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

    # ── stats helpers ────────────────────────────────────────────

    def get_review_summary_stats(self, user_id: UUID) -> dict:
        """Get review summary statistics for a user."""
        from datetime import timedelta

        from apps.words.infrastructure.models import Word

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

    def get_stats(self, user_id: UUID) -> dict:
        from apps.words.infrastructure.models import Word

        cache_key = f"word_stats_{user_id}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

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

        result = {
            "total": total,
            "mastered": mastered,
            "learning": learning,
            "new": new_words,
            "by_difficulty": by_difficulty,
            "by_category": by_category_formatted,
            "average_confidence": round(avg_confidence, 1),
        }

        cache.set(cache_key, result, timeout=300)  # 5 min
        return result
