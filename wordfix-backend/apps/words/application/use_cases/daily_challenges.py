"""
Daily challenges use cases — generate, track progress, claim bonus.
"""

import logging
from uuid import UUID

from apps.common.exceptions import ValidationError

logger = logging.getLogger(__name__)


class GetDailyChallengesUseCase:
    """Get today's daily challenges, creating them if needed."""

    def __init__(self, challenge_repo, word_repo, progress_repo, challenge_service):
        self.challenge_repo = challenge_repo
        self.word_repo = word_repo
        self.progress_repo = progress_repo
        self.challenge_service = challenge_service

    def execute(self, user_id) -> dict:
        user_id = UUID(str(user_id))

        # Try to get today's challenges
        challenge, created = self.challenge_repo.get_or_create_today(user_id=user_id)

        if created or not challenge.challenges:
            # Generate new challenges
            try:
                progress = self.progress_repo.get_or_create(user_id)
                level = progress.level
            except Exception:
                level = 1

            word_count = self.word_repo.get_count_by_user(user_id=user_id)
            challenges = self.challenge_service.generate_daily_challenges(level, word_count)

            challenge = self.challenge_repo.update(
                challenge_id=challenge.id,
                challenges=challenges,
            )

        return {
            "date": str(challenge.date),
            "challenges": challenge.challenges,
            "all_completed": challenge.all_completed,
            "bonus_claimed": challenge.bonus_claimed,
        }


class UpdateChallengeProgressUseCase:
    """Update progress on a daily challenge when actions happen."""

    def __init__(self, challenge_repo, xp_service=None):
        self.challenge_repo = challenge_repo
        self.xp_service = xp_service

    def execute(self, user_id, challenge_type: str, amount: int = 1) -> dict:
        user_id = UUID(str(user_id))

        try:
            challenge, _ = self.challenge_repo.get_or_create_today(user_id=user_id)
        except Exception:
            return {"challenge_updated": False}

        if not challenge.challenges:
            return {"challenge_updated": False}

        challenges = list(challenge.challenges)
        updated = False
        xp_earned = 0
        challenge_completed = False

        for c in challenges:
            if c.get("type") == challenge_type and not c.get("completed", False):
                c["current"] = c.get("current", 0) + amount
                if c["current"] >= c.get("target", 1):
                    c["current"] = c["target"]
                    c["completed"] = True
                    challenge_completed = True
                    xp_earned = c.get("xp_reward", 0)
                updated = True
                break

        if not updated:
            return {"challenge_updated": False}

        # Check if all completed
        all_completed = all(c.get("completed", False) for c in challenges)

        update_data = {"challenges": challenges}
        if all_completed and not challenge.all_completed:
            update_data["all_completed"] = True
            # All completed bonus
            if self.xp_service:
                try:
                    self.xp_service.award_xp(
                        user_id, 50, "daily_goal",
                        "All daily challenges completed!"
                    )
                    xp_earned += 50
                except Exception as e:
                    logger.warning(f"Failed to award daily bonus XP: {e}")

        self.challenge_repo.update(challenge_id=challenge.id, **update_data)

        # Award XP for individual challenge completion
        if challenge_completed and xp_earned > 0 and self.xp_service:
            try:
                if not all_completed:  # Don't double-award
                    self.xp_service.award_xp(
                        user_id, c.get("xp_reward", 0), "daily_goal",
                        f"Challenge completed: {c.get('title', '')}",
                    )
            except Exception as e:
                logger.warning(f"Failed to award challenge XP: {e}")

        return {
            "challenge_updated": True,
            "completed": challenge_completed,
            "all_completed": all_completed,
            "xp_earned": xp_earned,
        }


class ClaimDailyBonusUseCase:
    """Claim daily bonus when all challenges are completed."""

    def __init__(self, challenge_repo):
        self.challenge_repo = challenge_repo

    def execute(self, user_id) -> dict:
        user_id = UUID(str(user_id))

        challenge, _ = self.challenge_repo.get_or_create_today(user_id=user_id)

        if not challenge.all_completed:
            raise ValidationError("Not all challenges are completed yet.")

        if challenge.bonus_claimed:
            raise ValidationError("Daily bonus has already been claimed.")

        self.challenge_repo.update(
            challenge_id=challenge.id,
            bonus_claimed=True,
        )

        return {
            "claimed": True,
            "message": "Daily bonus claimed!",
        }
