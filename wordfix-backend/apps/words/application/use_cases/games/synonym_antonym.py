"""Synonym & Antonym game use cases."""

import json
import logging
import random
from datetime import datetime, timezone
from uuid import UUID

from apps.common.exceptions import ValidationError

logger = logging.getLogger(__name__)

# ── Fallback synonym/antonym pairs ──────────────────────────────────────────
FALLBACK_DATA: dict[str, dict] = {
    "happy": {"synonym": "joyful", "antonym": "sad", "syn_opts": ["joyful", "angry", "tired", "slow"], "ant_opts": ["sad", "quick", "bright", "loud"]},
    "big": {"synonym": "large", "antonym": "small", "syn_opts": ["large", "thin", "dark", "weak"], "ant_opts": ["small", "tall", "wide", "fast"]},
    "fast": {"synonym": "quick", "antonym": "slow", "syn_opts": ["quick", "heavy", "quiet", "cold"], "ant_opts": ["slow", "bright", "warm", "deep"]},
    "hot": {"synonym": "warm", "antonym": "cold", "syn_opts": ["warm", "light", "loud", "thin"], "ant_opts": ["cold", "soft", "rich", "safe"]},
    "good": {"synonym": "great", "antonym": "bad", "syn_opts": ["great", "cheap", "tiny", "loud"], "ant_opts": ["bad", "soft", "near", "old"]},
    "strong": {"synonym": "powerful", "antonym": "weak", "syn_opts": ["powerful", "gentle", "narrow", "plain"], "ant_opts": ["weak", "hard", "wide", "full"]},
    "beautiful": {"synonym": "lovely", "antonym": "ugly", "syn_opts": ["lovely", "rough", "empty", "flat"], "ant_opts": ["ugly", "sharp", "deep", "calm"]},
    "old": {"synonym": "ancient", "antonym": "new", "syn_opts": ["ancient", "smooth", "round", "brief"], "ant_opts": ["new", "bold", "rare", "dry"]},
    "easy": {"synonym": "simple", "antonym": "difficult", "syn_opts": ["simple", "narrow", "steep", "bitter"], "ant_opts": ["difficult", "smooth", "distant", "wild"]},
    "rich": {"synonym": "wealthy", "antonym": "poor", "syn_opts": ["wealthy", "clever", "brave", "rough"], "ant_opts": ["poor", "clean", "sharp", "calm"]},
    "bright": {"synonym": "vivid", "antonym": "dark", "syn_opts": ["vivid", "silent", "cheap", "mild"], "ant_opts": ["dark", "sweet", "wide", "short"]},
    "brave": {"synonym": "courageous", "antonym": "cowardly", "syn_opts": ["courageous", "gentle", "sleepy", "narrow"], "ant_opts": ["cowardly", "heavy", "empty", "plain"]},
    "clean": {"synonym": "pure", "antonym": "dirty", "syn_opts": ["pure", "loud", "rough", "thick"], "ant_opts": ["dirty", "bright", "sharp", "tall"]},
    "deep": {"synonym": "profound", "antonym": "shallow", "syn_opts": ["profound", "smooth", "narrow", "sweet"], "ant_opts": ["shallow", "strong", "rough", "plain"]},
    "full": {"synonym": "complete", "antonym": "empty", "syn_opts": ["complete", "narrow", "gentle", "steep"], "ant_opts": ["empty", "wild", "round", "calm"]},
    "loud": {"synonym": "noisy", "antonym": "quiet", "syn_opts": ["noisy", "gentle", "thick", "plain"], "ant_opts": ["quiet", "sweet", "round", "heavy"]},
    "safe": {"synonym": "secure", "antonym": "dangerous", "syn_opts": ["secure", "steep", "bitter", "mild"], "ant_opts": ["dangerous", "gentle", "smooth", "round"]},
    "smart": {"synonym": "clever", "antonym": "stupid", "syn_opts": ["clever", "rough", "bitter", "steep"], "ant_opts": ["stupid", "soft", "wild", "plain"]},
    "wide": {"synonym": "broad", "antonym": "narrow", "syn_opts": ["broad", "steep", "bitter", "gentle"], "ant_opts": ["narrow", "bright", "smooth", "sweet"]},
    "young": {"synonym": "youthful", "antonym": "old", "syn_opts": ["youthful", "rough", "plain", "bitter"], "ant_opts": ["old", "sharp", "wild", "round"]},
}


class StartSynonymAntonymUseCase:
    """Start a Synonym & Antonym game session."""

    def __init__(self, word_repo, game_repo, ai_provider=None, user_repo=None):
        self.word_repo = word_repo
        self.game_repo = game_repo
        self.ai_provider = ai_provider
        self.user_repo = user_repo

    def execute(self, user_id, word_count: int = 10) -> dict:
        user_id = UUID(str(user_id))

        # Get user's words
        words, _ = self.word_repo.get_all_by_user(user_id=user_id, page=1, page_size=200)
        eligible = [w for w in words if w.original_word and w.translation]

        # Try AI-generated questions if we have enough words
        questions = []
        if len(eligible) >= 5:
            random.shuffle(eligible)
            selected = eligible[:min(word_count, len(eligible))]
            word_texts = [w.original_word for w in selected]
            questions = self._generate_questions_ai(word_texts, user_id)

        # Fallback to built-in data if AI failed or not enough words
        if not questions:
            questions = self._generate_fallback_questions(word_count)

        # Create session
        total_rounds = len(questions)
        session = self.game_repo.create(
            user_id=user_id,
            game_type="synonym_antonym",
            max_score=total_rounds * 10,
        )

        # Create rounds
        for i, q in enumerate(questions, start=1):
            # Randomly pick synonym or antonym for each round
            qtype = random.choice(["synonym", "antonym"])
            if qtype == "synonym":
                correct = q["synonym"]["correct"]
                options = q["synonym"]["options"]
            else:
                correct = q["antonym"]["correct"]
                options = q["antonym"]["options"]

            self.game_repo.create_synonym_antonym_round(
                session_id=session.id,
                round_number=i,
                question_type=qtype,
                word_text=q["word"],
                correct_answer=correct,
                options=options,
            )

        # Return first round info
        return {
            "session_id": str(session.id),
            "total_rounds": total_rounds,
            "current_round": 1,
            "rounds": [
                {
                    "round_number": i + 1,
                    "word": questions[i]["word"],
                    "question_type": "synonym" if (i % 2 == 0) else "antonym",
                    "options": questions[i]["synonym"]["options"] if (i % 2 == 0) else questions[i]["antonym"]["options"],
                }
                for i in range(len(questions))
            ],
        }

    def _generate_questions_ai(self, word_texts: list[str], user_id) -> list[dict]:
        """Try to generate questions via AI."""
        if not self.ai_provider:
            return []

        try:
            from core.services.ai.prompts import SYNONYM_ANTONYM_PROMPT, NATIVE_LANGUAGE_MAP

            proficiency = "B1"
            if self.user_repo:
                try:
                    user = self.user_repo.get_by_id(user_id)
                    proficiency = getattr(user, "proficiency_level", "B1") or "B1"
                except Exception:
                    pass

            prompt = SYNONYM_ANTONYM_PROMPT.format(
                proficiency_level=proficiency,
                words=", ".join(word_texts[:10]),
            )

            response = self.ai_provider.generate(prompt)
            data = json.loads(response)
            questions = data.get("questions", [])

            # Validate structure
            valid = []
            for q in questions:
                if (
                    "word" in q
                    and "synonym" in q
                    and "antonym" in q
                    and "correct" in q["synonym"]
                    and "options" in q["synonym"]
                    and "correct" in q["antonym"]
                    and "options" in q["antonym"]
                    and len(q["synonym"]["options"]) >= 2
                    and len(q["antonym"]["options"]) >= 2
                ):
                    # Ensure correct answer is in options
                    if q["synonym"]["correct"] not in q["synonym"]["options"]:
                        q["synonym"]["options"][0] = q["synonym"]["correct"]
                    if q["antonym"]["correct"] not in q["antonym"]["options"]:
                        q["antonym"]["options"][0] = q["antonym"]["correct"]
                    random.shuffle(q["synonym"]["options"])
                    random.shuffle(q["antonym"]["options"])
                    valid.append(q)

            return valid if len(valid) >= 3 else []

        except Exception as e:
            logger.warning(f"AI synonym/antonym generation failed: {e}")
            return []

    def _generate_fallback_questions(self, count: int) -> list[dict]:
        """Generate questions from built-in fallback data."""
        items = list(FALLBACK_DATA.items())
        random.shuffle(items)
        selected = items[:min(count, len(items))]

        questions = []
        for word, data in selected:
            syn_opts = list(data["syn_opts"])
            ant_opts = list(data["ant_opts"])
            random.shuffle(syn_opts)
            random.shuffle(ant_opts)
            questions.append({
                "word": word,
                "synonym": {"correct": data["synonym"], "options": syn_opts},
                "antonym": {"correct": data["antonym"], "options": ant_opts},
            })

        return questions


class SubmitSynonymAntonymUseCase:
    """Submit an answer for a synonym/antonym round."""

    def __init__(self, word_repo, game_repo, sr_service, xp_service=None,
                 challenge_repo=None):
        self.word_repo = word_repo
        self.game_repo = game_repo
        self.sr_service = sr_service
        self.xp_service = xp_service
        self.challenge_repo = challenge_repo

    def execute(self, session_id, user_id, round_number: int, answer: str) -> dict:
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        session = self.game_repo.get_by_id(session_id=session_id, user_id=user_id)
        if session.is_completed:
            raise ValidationError("This game session is already completed.")

        sa_round = self.game_repo.get_synonym_antonym_round(session_id, round_number)

        if sa_round.is_correct is not None:
            raise ValidationError("This round is already answered.")

        answer_normalized = answer.strip().lower()
        correct = sa_round.correct_answer.strip().lower()
        is_correct = answer_normalized == correct

        score = 10 if is_correct else 0

        self.game_repo.update_synonym_antonym_round(
            round_id=sa_round.id,
            user_answer=answer_normalized,
            is_correct=is_correct,
            score=score,
        )

        # Combo logic
        if is_correct:
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

        # Update session combo
        self.game_repo.update(
            session_id=session_id,
            current_combo=current_combo,
            max_combo=max_combo,
            combo_xp_bonus=session.combo_xp_bonus + combo_bonus,
        )

        xp_earned = score + combo_bonus

        # Check if there's a next round
        next_round = None
        try:
            next_sa = self.game_repo.get_synonym_antonym_round(session_id, round_number + 1)
            next_round = {
                "round_number": next_sa.round_number,
                "word": next_sa.word_text,
                "question_type": next_sa.question_type,
                "options": next_sa.options,
            }
        except Exception:
            next_round = None

        return {
            "is_correct": is_correct,
            "correct_answer": correct,
            "score": score,
            "next_round": next_round,
            "combo": current_combo,
            "multiplier": multiplier,
            "xp_earned": xp_earned,
        }


class CompleteSynonymAntonymUseCase:
    """Complete a Synonym & Antonym game session."""

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

        rounds = self.game_repo.get_synonym_antonym_rounds(session_id)
        total_score = sum(r.score for r in rounds)
        correct_count = sum(1 for r in rounds if r.is_correct)
        total_rounds = len(rounds)
        max_score = total_rounds * 10
        accuracy_pct = round((correct_count / total_rounds * 100), 1) if total_rounds > 0 else 0

        now = datetime.now(timezone.utc)
        self.game_repo.update(
            session_id=session_id,
            is_completed=True,
            completed_at=now,
            score=total_score,
            correct_answers=correct_count,
            incorrect_answers=total_rounds - correct_count,
        )

        # XP
        xp_earned = 0
        if self.xp_service:
            try:
                from apps.users.domain.services import XP_REWARDS
                xp_result = self.xp_service.award_xp(
                    user_id, XP_REWARDS.get("game_complete", 15),
                    "game_complete", "Completed Synonym & Antonym",
                )
                xp_earned = xp_result.get("xp_gained", 0)

                if accuracy_pct >= 80:
                    bonus = self.xp_service.award_xp(
                        user_id, XP_REWARDS.get("game_good", 10),
                        "game_good", "Good Synonym & Antonym score",
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
                        "synonym_antonym_score": total_score,
                        "synonym_antonym_accuracy": accuracy_pct,
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
                    "word": r.word_text,
                    "question_type": r.question_type,
                    "correct_answer": r.correct_answer,
                    "user_answer": r.user_answer,
                    "is_correct": r.is_correct,
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
