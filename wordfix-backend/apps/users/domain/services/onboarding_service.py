"""
Onboarding level test domain service.

Adaptive test: if user scores < 2/3 at a level, stop and assign previous level.
"""

import logging

logger = logging.getLogger(__name__)

LEVELS_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"]


class OnboardingService:
    """Domain service for onboarding level assessment."""

    def calculate_level(self, answers: list[dict]) -> str:
        """
        Calculate proficiency level from answers.

        Each answer has: {question_id, answer, is_correct, level}

        Algorithm:
        - Group answers by level
        - For each level (A1→C2), check if user got >= 2/3 correct
        - If yes, move to next level
        - If no, return the previous level (or A1 if failed at A1)
        - If all levels passed, return C2
        """
        if not answers:
            return "A1"

        # Group by level
        level_scores: dict[str, dict] = {}
        for answer in answers:
            level = answer.get("level", "A1")
            if level not in level_scores:
                level_scores[level] = {"correct": 0, "total": 0}
            level_scores[level]["total"] += 1
            if answer.get("is_correct", False):
                level_scores[level]["correct"] += 1

        # Walk through levels
        highest_passed = None
        for level in LEVELS_ORDER:
            score = level_scores.get(level)
            if score is None:
                # No questions for this level — assume not passed
                break
            if score["total"] == 0:
                break
            if score["correct"] >= 2:
                highest_passed = level
            else:
                break

        if highest_passed is None:
            return "A1"

        return highest_passed
