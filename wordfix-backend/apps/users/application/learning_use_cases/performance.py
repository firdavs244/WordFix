"""
Session Performance use case – record effectiveness metrics.
"""

import logging
from datetime import datetime
from uuid import UUID

logger = logging.getLogger(__name__)


class RecordSessionPerformanceUseCase:
    """Record performance metrics for a completed session."""

    EXPECTED_DURATIONS = {
        "review": 10 * 60,
        "test": 15 * 60,
        "game": 5 * 60,
        "chat": 10 * 60,
    }

    def __init__(self, performance_repo):
        self.performance_repo = performance_repo

    def execute(
        self,
        user_id: UUID,
        session_type: str,
        started_at,
        ended_at,
        accuracy: float = 0.0,
        completion_rate: float = 1.0,
    ) -> dict:
        if isinstance(started_at, str):
            started_at = datetime.fromisoformat(started_at)
        if isinstance(ended_at, str):
            ended_at = datetime.fromisoformat(ended_at)

        duration = (ended_at - started_at).total_seconds()
        expected = self.EXPECTED_DURATIONS.get(session_type, 600)
        engagement = min(duration / expected, 1.0) if expected > 0 else 0.5

        effectiveness = accuracy * 0.4 + completion_rate * 0.3 + engagement * 0.3

        perf = self.performance_repo.create(
            user_id=user_id,
            session_type=session_type,
            started_at=started_at,
            ended_at=ended_at,
            hour_of_day=started_at.hour,
            day_of_week=started_at.weekday(),
            accuracy=round(accuracy, 4),
            completion_rate=round(completion_rate, 4),
            engagement_score=round(engagement, 4),
            effectiveness_score=round(effectiveness, 4),
        )

        return {
            "performance_id": str(perf.id),
            "effectiveness": round(effectiveness, 4),
        }
