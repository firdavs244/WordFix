"""
Review, Streak, and DailyActivity repository implementations using Django ORM.
"""

from datetime import date
from uuid import UUID

from django.utils import timezone

from apps.common.exceptions import EntityNotFoundError
from apps.words.domain.entities import (
    DailyActivityEntity,
    DailyStreakEntity,
    ReviewLogEntity,
    ReviewSessionEntity,
)
from apps.words.domain.repositories import (
    AbstractDailyActivityRepository,
    AbstractDailyStreakRepository,
    AbstractReviewLogRepository,
    AbstractReviewSessionRepository,
)
from apps.words.infrastructure.models import (
    DailyActivity,
    DailyStreak,
    ReviewLog,
    ReviewSession,
)


class DjangoReviewSessionRepository(AbstractReviewSessionRepository):
    """Concrete implementation for ReviewSession."""

    def _to_entity(self, session: ReviewSession) -> ReviewSessionEntity:
        return ReviewSessionEntity(
            id=session.id,
            user_id=session.user_id,
            started_at=session.started_at,
            completed_at=session.completed_at,
            total_words=session.total_words,
            correct_count=session.correct_count,
            incorrect_count=session.incorrect_count,
            average_quality=session.average_quality,
            duration_seconds=session.duration_seconds,
            session_type=session.session_type,
            is_completed=session.is_completed,
            current_combo=session.current_combo,
            max_combo=session.max_combo,
            combo_xp_bonus=session.combo_xp_bonus,
            is_active=session.is_active,
            created_at=session.created_at,
            updated_at=session.updated_at,
        )

    def create(self, user_id: UUID, **kwargs) -> ReviewSessionEntity:
        session = ReviewSession.objects.create(user_id=user_id, **kwargs)
        return self._to_entity(session)

    def get_by_id(self, session_id: UUID, user_id: UUID) -> ReviewSessionEntity:
        try:
            session = ReviewSession.objects.get(id=session_id, user_id=user_id)
            return self._to_entity(session)
        except ReviewSession.DoesNotExist:
            raise EntityNotFoundError("Review session not found.")

    def update(self, session_id: UUID, **kwargs) -> ReviewSessionEntity:
        try:
            session = ReviewSession.objects.get(id=session_id)
        except ReviewSession.DoesNotExist:
            raise EntityNotFoundError("Review session not found.")
        for field, value in kwargs.items():
            setattr(session, field, value)
        session.save()
        return self._to_entity(session)

    def get_by_user(
        self, user_id: UUID, page: int = 1, page_size: int = 20
    ) -> tuple[list[ReviewSessionEntity], int]:
        qs = ReviewSession.objects.filter(user_id=user_id).order_by("-started_at")
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        sessions = [self._to_entity(s) for s in qs[start:end]]
        return sessions, total


class DjangoReviewLogRepository(AbstractReviewLogRepository):
    """Concrete implementation for ReviewLog."""

    def _to_entity(self, log: ReviewLog) -> ReviewLogEntity:
        return ReviewLogEntity(
            id=log.id,
            session_id=log.session_id,
            user_id=log.user_id,
            word_id=log.word_id,
            quality=log.quality,
            response_time_ms=log.response_time_ms,
            is_correct=log.is_correct,
            reviewed_at=log.reviewed_at,
            previous_confidence=log.previous_confidence,
            new_confidence=log.new_confidence,
            previous_interval=log.previous_interval,
            new_interval=log.new_interval,
            is_active=log.is_active,
            created_at=log.created_at,
            updated_at=log.updated_at,
        )

    def create(self, **kwargs) -> ReviewLogEntity:
        log = ReviewLog.objects.create(**kwargs)
        return self._to_entity(log)

    def get_by_session(self, session_id: UUID) -> list[ReviewLogEntity]:
        qs = ReviewLog.objects.filter(session_id=session_id).order_by("reviewed_at")
        return [self._to_entity(log) for log in qs]

    def get_by_user(
        self, user_id: UUID, page: int = 1, page_size: int = 20
    ) -> tuple[list[ReviewLogEntity], int]:
        qs = ReviewLog.objects.filter(user_id=user_id).order_by("-reviewed_at")
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        logs = [self._to_entity(log) for log in qs[start:end]]
        return logs, total


class DjangoStreakRepository(AbstractDailyStreakRepository):
    """Concrete implementation for DailyStreak."""

    def _to_entity(self, streak: DailyStreak) -> DailyStreakEntity:
        return DailyStreakEntity(
            id=streak.id,
            user_id=streak.user_id,
            current_streak=streak.current_streak,
            longest_streak=streak.longest_streak,
            last_activity_date=streak.last_activity_date,
            streak_frozen_until=streak.streak_frozen_until,
            total_review_days=streak.total_review_days,
            is_active=streak.is_active,
            created_at=streak.created_at,
            updated_at=streak.updated_at,
        )

    def get_or_create(self, user_id: UUID) -> DailyStreakEntity:
        streak, _ = DailyStreak.objects.get_or_create(user_id=user_id)
        return self._to_entity(streak)

    def update(self, streak_id: UUID, **kwargs) -> DailyStreakEntity:
        try:
            streak = DailyStreak.objects.get(id=streak_id)
        except DailyStreak.DoesNotExist:
            raise EntityNotFoundError("Streak not found.")
        for field, value in kwargs.items():
            setattr(streak, field, value)
        streak.save()
        return self._to_entity(streak)


class DjangoDailyActivityRepository(AbstractDailyActivityRepository):
    """Concrete implementation for DailyActivity."""

    def _to_entity(self, activity: DailyActivity) -> DailyActivityEntity:
        return DailyActivityEntity(
            id=activity.id,
            user_id=activity.user_id,
            date=activity.date,
            words_reviewed=activity.words_reviewed,
            words_added=activity.words_added,
            words_mastered=activity.words_mastered,
            correct_answers=activity.correct_answers,
            incorrect_answers=activity.incorrect_answers,
            total_time_seconds=activity.total_time_seconds,
            goal_completed=activity.goal_completed,
            xp_earned=activity.xp_earned,
            is_active=activity.is_active,
            created_at=activity.created_at,
            updated_at=activity.updated_at,
        )

    def get_or_create_today(self, user_id: UUID) -> DailyActivityEntity:
        today = date.today()
        activity, _ = DailyActivity.objects.get_or_create(
            user_id=user_id,
            date=today,
        )
        return self._to_entity(activity)

    def update(self, activity_id: UUID, **kwargs) -> DailyActivityEntity:
        try:
            activity = DailyActivity.objects.get(id=activity_id)
        except DailyActivity.DoesNotExist:
            raise EntityNotFoundError("Activity not found.")
        for field, value in kwargs.items():
            setattr(activity, field, value)
        activity.save()
        return self._to_entity(activity)

    def get_by_date_range(
        self, user_id: UUID, start_date, end_date
    ) -> list[DailyActivityEntity]:
        qs = DailyActivity.objects.filter(
            user_id=user_id,
            date__gte=start_date,
            date__lte=end_date,
        ).order_by("date")
        return [self._to_entity(a) for a in qs]
