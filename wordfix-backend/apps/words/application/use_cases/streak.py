"""
Streak use case.
"""

from datetime import date, timedelta
from uuid import UUID


class UpdateStreakUseCase:
    """Update user's daily streak."""

    def __init__(self, streak_repo):
        self.streak_repo = streak_repo

    def execute(self, user_id: UUID):
        user_id = UUID(str(user_id))
        streak = self.streak_repo.get_or_create(user_id=user_id)
        today = date.today()

        if streak.last_activity_date == today:
            return streak  # Already counted today

        yesterday = today - timedelta(days=1)

        if streak.last_activity_date == yesterday:
            new_streak = streak.current_streak + 1
        elif streak.last_activity_date is None:
            new_streak = 1
        elif (
            streak.streak_frozen_until
            and streak.streak_frozen_until >= today
        ):
            new_streak = streak.current_streak  # Frozen
        else:
            new_streak = 1  # Reset

        longest = max(new_streak, streak.longest_streak)

        return self.streak_repo.update(
            streak_id=streak.id,
            current_streak=new_streak,
            longest_streak=longest,
            last_activity_date=today,
            total_review_days=streak.total_review_days + 1,
        )
