"""
Mistake Pattern use cases – detect and retrieve mistake patterns.
"""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class GetMistakePatternsUseCase:
    """Return mistake patterns for a user."""

    def __init__(self, pattern_repo):
        self.pattern_repo = pattern_repo

    def execute(self, user_id: UUID, include_resolved: bool = False) -> list[dict]:
        patterns = self.pattern_repo.get_by_user(user_id, include_resolved)
        return [
            {
                "id": str(p.id),
                "pattern_type": p.pattern_type,
                "description": p.description,
                "examples": p.examples,
                "occurrence_count": p.occurrence_count,
                "is_resolved": p.is_resolved,
                "drills_completed": p.drills_completed,
                "success_rate_after_drills": p.success_rate_after_drills,
                "related_words": p.related_words,
            }
            for p in patterns
        ]


class RecordMistakeUseCase:
    """Detect and record a mistake pattern."""

    def __init__(self, pattern_repo, pattern_service):
        self.pattern_repo = pattern_repo
        self.pattern_service = pattern_service

    def execute(
        self,
        user_id: UUID,
        wrong_answer: str,
        correct_answer: str,
        context: str = "",
    ) -> dict:
        detected = self.pattern_service.detect_pattern(wrong_answer, correct_answer, context)
        if detected is None:
            return {"pattern_id": None, "is_new": False}

        # Check for existing similar pattern
        existing = self.pattern_repo.find_similar(
            user_id, detected["type"], detected["related_words"],
        )

        if existing:
            existing.occurrence_count += 1
            examples = existing.examples or []
            examples.append(detected["example"])
            existing.examples = examples[-10:]  # keep last 10
            self.pattern_repo.save(existing)
            return {"pattern_id": str(existing.id), "is_new": False}

        new_pattern = self.pattern_repo.create(
            user_id=user_id,
            pattern_type=detected["type"],
            description=detected["description"],
            examples=[detected["example"]],
            related_words=detected["related_words"],
        )
        return {"pattern_id": str(new_pattern.id), "is_new": True}
