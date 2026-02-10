"""
Progress repository implementation using Django ORM.
"""

from dataclasses import dataclass
from uuid import UUID

from apps.users.infrastructure.models import UserProgress


@dataclass
class ProgressEntity:
    id: UUID
    user_id: UUID
    total_xp: int
    level: int
    words_learned_total: int
    words_mastered_total: int
    tests_completed: int
    games_played: int
    reviews_completed: int
    perfect_scores: int
    total_study_time_seconds: int


class DjangoProgressRepository:
    """Repository for UserProgress."""

    def _to_entity(self, p: UserProgress) -> ProgressEntity:
        return ProgressEntity(
            id=p.id, user_id=p.user_id, total_xp=p.total_xp, level=p.level,
            words_learned_total=p.words_learned_total,
            words_mastered_total=p.words_mastered_total,
            tests_completed=p.tests_completed, games_played=p.games_played,
            reviews_completed=p.reviews_completed, perfect_scores=p.perfect_scores,
            total_study_time_seconds=p.total_study_time_seconds,
        )

    def get_or_create(self, user_id: UUID) -> ProgressEntity:
        p, _ = UserProgress.objects.get_or_create(user_id=user_id)
        return self._to_entity(p)

    def update(self, progress_id: UUID, **kwargs) -> ProgressEntity:
        UserProgress.objects.filter(id=progress_id).update(**kwargs)
        p = UserProgress.objects.get(id=progress_id)
        return self._to_entity(p)

    def increment(self, user_id: UUID, **kwargs):
        """Increment counters atomically."""
        from django.db.models import F
        p, _ = UserProgress.objects.get_or_create(user_id=user_id)
        updates = {k: F(k) + v for k, v in kwargs.items()}
        UserProgress.objects.filter(id=p.id).update(**updates)
