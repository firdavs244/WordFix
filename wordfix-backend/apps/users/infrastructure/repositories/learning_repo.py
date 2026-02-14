"""
Repositories for adaptive-intelligence models.

Five repositories that bridge domain logic with Django ORM.
"""

import logging
from datetime import timedelta
from uuid import UUID

from django.utils import timezone

from apps.users.infrastructure.models import (
    DomainCoverage,
    LearningProfile,
    MistakePattern,
    SessionPerformance,
    WordRecommendation,
)

logger = logging.getLogger(__name__)


# ── LearningProfileRepository ────────────────────────────────────


class LearningProfileRepository:
    """CRUD operations for LearningProfile."""

    def get_by_user(self, user_id: UUID) -> LearningProfile | None:
        try:
            return LearningProfile.objects.get(user_id=user_id)
        except LearningProfile.DoesNotExist:
            return None

    def get_or_create(self, user_id: UUID) -> LearningProfile:
        profile, _ = LearningProfile.objects.get_or_create(user_id=user_id)
        return profile

    def create(self, **kwargs) -> LearningProfile:
        return LearningProfile.objects.create(**kwargs)

    def save(self, profile: LearningProfile) -> LearningProfile:
        profile.save()
        return profile


# ── MistakePatternRepository ─────────────────────────────────────


class MistakePatternRepository:
    """CRUD operations for MistakePattern."""

    def get_by_user(
        self, user_id: UUID, include_resolved: bool = False
    ) -> list[MistakePattern]:
        qs = MistakePattern.objects.filter(user_id=user_id)
        if not include_resolved:
            qs = qs.filter(is_resolved=False)
        return list(qs)

    def find_similar(
        self,
        user_id: UUID,
        pattern_type: str,
        related_words: list[str],
    ) -> MistakePattern | None:
        """Find an existing pattern with overlapping related words."""
        patterns = MistakePattern.objects.filter(
            user_id=user_id,
            pattern_type=pattern_type,
            is_resolved=False,
        )
        for p in patterns:
            existing_words = set(p.related_words or [])
            new_words = set(related_words or [])
            if existing_words & new_words:
                return p
        return None

    def create(self, **kwargs) -> MistakePattern:
        return MistakePattern.objects.create(**kwargs)

    def save(self, pattern: MistakePattern) -> MistakePattern:
        pattern.save()
        return pattern


# ── DomainCoverageRepository ─────────────────────────────────────


class DomainCoverageRepository:
    """CRUD operations for DomainCoverage."""

    def get_by_user(self, user_id: UUID) -> list[DomainCoverage]:
        return list(DomainCoverage.objects.filter(user_id=user_id))

    def get_or_create(self, user_id: UUID, domain: str) -> DomainCoverage:
        obj, _ = DomainCoverage.objects.get_or_create(
            user_id=user_id, domain=domain,
        )
        return obj

    def save(self, coverage: DomainCoverage) -> DomainCoverage:
        coverage.save()
        return coverage


# ── WordRecommendationRepository ─────────────────────────────────


class WordRecommendationRepository:
    """CRUD operations for WordRecommendation."""

    def get_active(self, user_id: UUID, limit: int = 10) -> list[WordRecommendation]:
        return list(
            WordRecommendation.objects.filter(
                user_id=user_id,
                is_accepted=False,
                is_dismissed=False,
            )[:limit]
        )

    def get_active_words(self, user_id: UUID) -> list[str]:
        """Return list of recommended words (active, not accepted/dismissed)."""
        return list(
            WordRecommendation.objects.filter(
                user_id=user_id,
                is_accepted=False,
                is_dismissed=False,
            ).values_list("recommended_word", flat=True)
        )

    def get_by_id(self, rec_id: UUID, user_id: UUID) -> WordRecommendation | None:
        """Get a single recommendation by id, scoped to user."""
        try:
            return WordRecommendation.objects.get(id=rec_id, user_id=user_id)
        except WordRecommendation.DoesNotExist:
            return None

    def exists_for_word(self, user_id: UUID, word: str) -> bool:
        """Check if an active recommendation already exists for this word."""
        return WordRecommendation.objects.filter(
            user_id=user_id,
            recommended_word__iexact=word,
            is_accepted=False,
            is_dismissed=False,
        ).exists()

    def create(self, **kwargs) -> WordRecommendation:
        return WordRecommendation.objects.create(**kwargs)

    def accept(self, rec_id: UUID, user_id: UUID) -> bool:
        updated = WordRecommendation.objects.filter(
            id=rec_id, user_id=user_id,
            is_accepted=False,
        ).update(is_accepted=True, accepted_at=timezone.now())
        return updated > 0

    def dismiss(self, rec_id: UUID, user_id: UUID) -> bool:
        updated = WordRecommendation.objects.filter(
            id=rec_id, user_id=user_id,
        ).update(is_dismissed=True)
        return updated > 0


# ── SessionPerformanceRepository ─────────────────────────────────


class SessionPerformanceRepository:
    """CRUD operations for SessionPerformance."""

    def get_recent(self, user_id: UUID, days: int = 30) -> list[SessionPerformance]:
        since = timezone.now() - timedelta(days=days)
        return list(
            SessionPerformance.objects.filter(
                user_id=user_id,
                created_at__gte=since,
            )
        )

    def create(self, **kwargs) -> SessionPerformance:
        return SessionPerformance.objects.create(**kwargs)
