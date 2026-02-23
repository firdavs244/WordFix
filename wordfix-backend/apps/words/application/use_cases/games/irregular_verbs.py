"""Irregular Verbs game use cases."""

import logging
import random
from datetime import datetime, timezone
from uuid import UUID

from apps.common.exceptions import ValidationError

logger = logging.getLogger(__name__)


class StartIrregularVerbsUseCase:
    """Start an Irregular Verbs game session."""

    def __init__(self, game_repo, user_repo=None):
        self.game_repo = game_repo
        self.user_repo = user_repo

    def execute(self, user_id, word_count: int = 10, tier: str = "") -> dict:
        user_id = UUID(str(user_id))

        from core.services.ai.irregular_verbs_data import get_verbs_by_tier, IRREGULAR_VERBS

        # Determine tier from user proficiency if not specified
        if not tier:
            tier = self._get_user_tier(user_id)

        verbs = get_verbs_by_tier(tier)
        if len(verbs) < 5:
            verbs = IRREGULAR_VERBS

        random.shuffle(verbs)
        selected = verbs[:min(word_count, len(verbs))]

        session = self.game_repo.create(
            user_id=user_id,
            game_type="irregular_verbs",
            max_score=len(selected) * 10,
        )

        # Create rounds
        rounds_data = []
        for i, (infinitive, past_simple, past_participle, translation) in enumerate(selected, start=1):
            self.game_repo.create_irregular_verb_round(
                session_id=session.id,
                round_number=i,
                infinitive=infinitive,
                translation=translation,
                correct_past_simple=past_simple,
                correct_past_participle=past_participle,
            )
            rounds_data.append({
                "round_number": i,
                "infinitive": infinitive,
                "translation": translation,
                "max_attempts": 2,
            })

        return {
            "session_id": str(session.id),
            "total_rounds": len(selected),
            "current_round": 1,
            "tier": tier,
            "rounds": rounds_data,
        }

    def _get_user_tier(self, user_id) -> str:
        """Determine tier based on user proficiency level."""
        if not self.user_repo:
            return "A2"
        try:
            user = self.user_repo.get_by_id(user_id)
            level = getattr(user, "proficiency_level", "B1") or "B1"
            mapping = {
                "A1": "A1",
                "A2": "A2",
                "B1": "B1",
                "B2": "B2",
                "C1": "B2",
                "C2": "B2",
            }
            return mapping.get(level, "A2")
        except Exception:
            return "A2"


class SubmitIrregularVerbUseCase:
    """Submit an answer for an irregular verb round."""

    def __init__(self, game_repo, xp_service=None, challenge_repo=None):
        self.game_repo = game_repo
        self.xp_service = xp_service
        self.challenge_repo = challenge_repo

    def execute(
        self,
        session_id,
        user_id,
        round_number: int,
        past_simple: str,
        past_participle: str,
    ) -> dict:
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        session = self.game_repo.get_by_id(session_id=session_id, user_id=user_id)
        if session.is_completed:
            raise ValidationError("This game session is already completed.")

        iv_round = self.game_repo.get_irregular_verb_round(session_id, round_number)

        # Check if already fully answered
        if iv_round.past_simple_correct is not None and iv_round.past_participle_correct is not None:
            if iv_round.attempts_used >= 2:
                raise ValidationError("No more attempts for this round.")

        ps_normalized = past_simple.strip().lower()
        pp_normalized = past_participle.strip().lower()

        # Handle verbs with alternatives (e.g. "was/were")
        correct_ps_options = [
            opt.strip().lower()
            for opt in iv_round.correct_past_simple.split("/")
        ]
        correct_pp_options = [
            opt.strip().lower()
            for opt in iv_round.correct_past_participle.split("/")
        ]

        ps_correct = ps_normalized in correct_ps_options
        pp_correct = pp_normalized in correct_pp_options

        new_attempts = iv_round.attempts_used + 1

        # Scoring: 5 pts per correct form, max 10
        score = 0
        if ps_correct:
            score += 5
        if pp_correct:
            score += 5

        # Second attempt penalty
        if new_attempts > 1:
            score = max(score - 2, 0)

        hints = dict(iv_round.hints_shown) if iv_round.hints_shown else {}

        # If wrong and has attempts left, provide hints
        if (not ps_correct or not pp_correct) and new_attempts < 2:
            if not ps_correct:
                # Show first letter hint
                correct_ps = iv_round.correct_past_simple
                hints["past_simple"] = correct_ps[0] + "_" * (len(correct_ps.split("/")[0]) - 1)
            if not pp_correct:
                correct_pp = iv_round.correct_past_participle
                hints["past_participle"] = correct_pp[0] + "_" * (len(correct_pp.split("/")[0]) - 1)

        self.game_repo.update_irregular_verb_round(
            round_id=iv_round.id,
            user_past_simple=ps_normalized,
            user_past_participle=pp_normalized,
            past_simple_correct=ps_correct,
            past_participle_correct=pp_correct,
            attempts_used=new_attempts,
            hints_shown=hints,
            score=score,
        )

        # Combo
        both_correct = ps_correct and pp_correct
        if both_correct:
            current_combo = session.current_combo + 1
            max_combo = max(session.max_combo, current_combo)
            from apps.words.domain.services import ComboService
            combo_xp, multiplier = ComboService.calculate_combo_xp(10, current_combo)
            combo_bonus = combo_xp - 10
        else:
            current_combo = 0
            max_combo = session.max_combo
            multiplier = 1.0
            combo_bonus = 0

        self.game_repo.update(
            session_id=session_id,
            current_combo=current_combo,
            max_combo=max_combo,
            combo_xp_bonus=session.combo_xp_bonus + combo_bonus,
        )

        xp_earned = score + combo_bonus

        # Determine if we should show correct answers
        show_answers = both_correct or new_attempts >= 2

        # Next round info
        next_round = None
        if show_answers:
            try:
                next_iv = self.game_repo.get_irregular_verb_round(session_id, round_number + 1)
                next_round = {
                    "round_number": next_iv.round_number,
                    "infinitive": next_iv.infinitive,
                    "translation": next_iv.translation,
                    "max_attempts": 2,
                }
            except Exception:
                next_round = None

        return {
            "past_simple_correct": ps_correct,
            "past_participle_correct": pp_correct,
            "correct_past_simple": iv_round.correct_past_simple if show_answers else "",
            "correct_past_participle": iv_round.correct_past_participle if show_answers else "",
            "score": score,
            "attempts_used": new_attempts,
            "attempts_remaining": max(2 - new_attempts, 0),
            "hints": hints if not show_answers else {},
            "next_round": next_round,
            "combo": current_combo,
            "multiplier": multiplier,
            "xp_earned": xp_earned,
        }


class CompleteIrregularVerbsUseCase:
    """Complete an Irregular Verbs game session."""

    def __init__(self, game_repo, xp_service=None, badge_service=None):
        self.game_repo = game_repo
        self.xp_service = xp_service
        self.badge_service = badge_service

    def execute(self, session_id, user_id) -> dict:
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        session = self.game_repo.get_by_id(session_id=session_id, user_id=user_id)
        if session.is_completed:
            raise ValidationError("This game session is already completed.")

        rounds = self.game_repo.get_irregular_verb_rounds(session_id)
        total_score = sum(r.score for r in rounds)
        fully_correct = sum(
            1 for r in rounds
            if r.past_simple_correct and r.past_participle_correct
        )
        total_rounds = len(rounds)
        max_score = total_rounds * 10
        accuracy_pct = round(
            (fully_correct / total_rounds * 100), 1
        ) if total_rounds > 0 else 0

        now = datetime.now(timezone.utc)
        self.game_repo.update(
            session_id=session_id,
            is_completed=True,
            completed_at=now,
            score=total_score,
            correct_answers=fully_correct,
            incorrect_answers=total_rounds - fully_correct,
        )

        # XP
        xp_earned = 0
        if self.xp_service:
            try:
                from apps.users.domain.services import XP_REWARDS
                xp_result = self.xp_service.award_xp(
                    user_id, XP_REWARDS.get("game_complete", 15),
                    "game_complete", "Completed Irregular Verbs",
                )
                xp_earned = xp_result.get("xp_gained", 0)

                if accuracy_pct >= 80:
                    bonus = self.xp_service.award_xp(
                        user_id, XP_REWARDS.get("game_good", 10),
                        "game_good", "Good Irregular Verbs score",
                    )
                    xp_earned += bonus.get("xp_gained", 0)
            except Exception as e:
                logger.warning(f"XP award failed: {e}")

        # Badges
        badges_earned = []
        if self.badge_service:
            try:
                badges_earned = self.badge_service.check_and_award_badges(
                    user_id, context={
                        "irregular_verbs_score": total_score,
                        "irregular_verbs_accuracy": accuracy_pct,
                    }
                )
            except Exception as e:
                logger.warning(f"Badge check failed: {e}")

        return {
            "total_score": total_score,
            "max_score": max_score,
            "rounds": [
                {
                    "round_number": r.round_number,
                    "infinitive": r.infinitive,
                    "translation": r.translation,
                    "correct_past_simple": r.correct_past_simple,
                    "correct_past_participle": r.correct_past_participle,
                    "user_past_simple": r.user_past_simple,
                    "user_past_participle": r.user_past_participle,
                    "past_simple_correct": r.past_simple_correct,
                    "past_participle_correct": r.past_participle_correct,
                    "score": r.score,
                }
                for r in rounds
            ],
            "accuracy_pct": accuracy_pct,
            "xp_earned": xp_earned,
            "badges_earned": [
                {"code": b.code, "name": b.name, "icon": b.icon}
                for b in badges_earned
            ],
        }
