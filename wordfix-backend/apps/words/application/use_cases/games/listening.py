"""Listening Challenge game use cases."""

import logging
import random
from datetime import datetime, timezone
from uuid import UUID

from apps.common.exceptions import ValidationError

logger = logging.getLogger(__name__)


class StartListeningChallengeUseCase:
    """Start a Listening Challenge game."""

    def __init__(self, word_repo, game_repo, tts_provider=None):
        self.word_repo = word_repo
        self.game_repo = game_repo
        self.tts_provider = tts_provider

    def execute(self, user_id, word_count=10) -> dict:
        user_id = UUID(str(user_id))

        words, _ = self.word_repo.get_all_by_user(user_id=user_id, page=1, page_size=200)
        eligible = [w for w in words if w.original_word]
        if len(eligible) < 5:
            raise ValidationError(
                "You need at least 5 words to play. Add more words first!"
            )

        # Prefer words with audio or pronunciation
        with_audio = [w for w in eligible if w.audio_url]
        without_audio = [w for w in eligible if not w.audio_url]
        random.shuffle(with_audio)
        random.shuffle(without_audio)
        ordered = with_audio + without_audio
        selected = ordered[:min(word_count, len(ordered))]

        # Generate audio for words without it
        final_words = []
        for word in selected:
            audio_url = self._get_or_generate_audio(word, user_id)
            if audio_url or word.audio_url:
                word.audio_url = audio_url or word.audio_url
                final_words.append(word)
            else:
                # TTS failed and no existing audio - still include (frontend shows text fallback)
                final_words.append(word)

            if len(final_words) >= word_count:
                break

        if len(final_words) < 5:
            # If TTS fails massively, still allow with available words
            final_words = selected[:max(5, len(final_words))]

        actual_count = len(final_words)

        session = self.game_repo.create(
            user_id=user_id,
            game_type="listening_challenge",
            max_score=actual_count * 10,
        )

        # Create listening rounds
        for i, word in enumerate(final_words, start=1):
            self.game_repo.create_listening_round(
                session_id=session.id,
                word_id=word.id,
                round_number=i,
                correct_answer=word.original_word.lower(),
            )

        first_word = final_words[0]
        return {
            "session_id": str(session.id),
            "total_rounds": actual_count,
            "current_round": 1,
            "first_word": {
                "round_number": 1,
                "audio_url": first_word.audio_url or "",
                "hint": " ".join(["_"] * len(first_word.original_word)),
                "difficulty": first_word.difficulty_level,
                "max_attempts": 3,
            },
        }

    def _get_or_generate_audio(self, word, user_id):
        """Get existing audio or generate via TTS."""
        if word.audio_url:
            return word.audio_url

        if not self.tts_provider:
            return ""

        try:
            import os
            from django.conf import settings

            audio_bytes = self.tts_provider.generate_audio(word.original_word)
            if not audio_bytes:
                return ""

            audio_dir = os.path.join(settings.MEDIA_ROOT, "audio", "words")
            os.makedirs(audio_dir, exist_ok=True)

            filename = f"{word.id}.mp3"
            filepath = os.path.join(audio_dir, filename)
            with open(filepath, "wb") as f:
                f.write(audio_bytes)

            audio_url = f"/media/audio/words/{filename}"
            # Update word audio_url
            try:
                self.word_repo.update(
                    word_id=word.id, user_id=user_id,
                    audio_url=audio_url,
                )
            except Exception:
                pass
            return audio_url
        except Exception as e:
            logger.warning(f"TTS generation failed for '{word.original_word}': {e}")
            return ""


class SubmitListeningAnswerUseCase:
    """Submit an answer for a listening round."""

    def __init__(self, word_repo, game_repo, sr_service, xp_service=None,
                 challenge_repo=None):
        self.word_repo = word_repo
        self.game_repo = game_repo
        self.sr_service = sr_service
        self.xp_service = xp_service
        self.challenge_repo = challenge_repo

    def execute(self, session_id, user_id, round_number, answer) -> dict:
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        session = self.game_repo.get_by_id(session_id=session_id, user_id=user_id)
        if session.is_completed:
            raise ValidationError("This game session is already completed.")

        lr = self.game_repo.get_listening_round(session_id, round_number)

        if lr.is_correct:
            raise ValidationError("This round is already answered correctly.")
        if lr.attempts_used >= lr.max_attempts:
            raise ValidationError("No attempts remaining for this round.")

        answer_normalized = answer.strip().lower()
        correct = lr.correct_answer.strip().lower()
        is_correct = answer_normalized == correct

        new_attempts = lr.attempts_used + 1
        user_answers = list(lr.user_answers) + [answer_normalized]
        hints_shown = list(lr.hints_shown)

        if is_correct:
            score = {1: 10, 2: 7, 3: 4}.get(new_attempts, 4)
            self.game_repo.update_listening_round(
                round_id=lr.id,
                is_correct=True,
                attempts_used=new_attempts,
                user_answers=user_answers,
                score=score,
            )

            # SR update — quality correlates with attempt count
            quality = max(5 - new_attempts, 3)
            self._update_sr(lr.word_id, user_id, quality)

            # Combo increment
            current_combo = session.current_combo + 1
            max_combo = max(session.max_combo, current_combo)
            from apps.words.domain.services import ComboService
            combo_xp, multiplier = ComboService.calculate_combo_xp(10, current_combo)
            combo_bonus = combo_xp - 10
        else:
            score = 0
            hint = self._generate_hint(correct, new_attempts)
            hints_shown.append(hint)

            update_data = {
                "attempts_used": new_attempts,
                "user_answers": user_answers,
                "hints_shown": hints_shown,
            }

            if new_attempts >= lr.max_attempts:
                update_data["score"] = 0
                update_data["is_correct"] = False
                # SR update — failed
                self._update_sr(lr.word_id, user_id, 1)

            self.game_repo.update_listening_round(round_id=lr.id, **update_data)

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

        # Next round info
        next_round = None
        move_to_next = is_correct or new_attempts >= lr.max_attempts
        if move_to_next:
            try:
                next_lr = self.game_repo.get_listening_round(session_id, round_number + 1)
                # Find the word for audio
                try:
                    word = self.word_repo.get_by_id(next_lr.word_id, user_id)
                    audio_url = word.audio_url or ""
                    word_len = len(word.original_word)
                except Exception:
                    audio_url = ""
                    word_len = len(next_lr.correct_answer)

                next_round = {
                    "round_number": next_lr.round_number,
                    "audio_url": audio_url,
                    "hint": " ".join(["_"] * word_len),
                    "max_attempts": next_lr.max_attempts,
                }
            except Exception:
                next_round = None  # No more rounds

        # Show correct answer only if answered correctly or out of attempts
        show_answer = is_correct or new_attempts >= lr.max_attempts

        return {
            "is_correct": is_correct,
            "score": score,
            "attempts_used": new_attempts,
            "attempts_remaining": max(lr.max_attempts - new_attempts, 0),
            "hint": hints_shown[-1] if hints_shown and not is_correct and new_attempts < lr.max_attempts else "",
            "correct_answer": correct if show_answer else "",
            "next_round": next_round,
            "combo": current_combo,
            "multiplier": multiplier,
            "xp_earned": xp_earned,
        }

    def _update_sr(self, word_id, user_id, quality):
        """Update spaced repetition for a word."""
        try:
            word = self.word_repo.get_by_id(word_id=word_id, user_id=user_id)
            now = datetime.now(timezone.utc)
            self.sr_service.calculate_next_review(word, quality, now=now)
            word.review_count += 1
            if quality >= 3:
                word.correct_count += 1
            else:
                word.incorrect_count += 1
            word.last_reviewed_at = now
            self.word_repo.update(
                word_id=word.id, user_id=user_id,
                confidence_score=word.confidence_score,
                next_review_at=word.next_review_at,
                review_count=word.review_count,
                correct_count=word.correct_count,
                incorrect_count=word.incorrect_count,
                last_reviewed_at=word.last_reviewed_at,
                is_mastered=word.is_mastered,
                easiness_factor=word.easiness_factor,
                repetition_number=word.repetition_number,
                interval_days=word.interval_days,
            )
        except Exception as e:
            logger.warning(f"SR update failed for listening word: {e}")

    @staticmethod
    def _generate_hint(word, attempt_number):
        """Generate progressive hint showing more letters."""
        letters = list(word.lower())
        hint = ["_"] * len(letters)
        for i in range(min(attempt_number, len(letters))):
            hint[i] = letters[i]
        return " ".join(hint)


class CompleteListeningChallengeUseCase:
    """Complete a Listening Challenge game."""

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

        rounds = self.game_repo.get_listening_rounds(session_id)
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
                    "game_complete", "Completed Listening Challenge",
                )
                xp_earned = xp_result.get("xp_gained", 0)

                if accuracy_pct >= 80:
                    bonus = self.xp_service.award_xp(
                        user_id, XP_REWARDS.get("game_good", 10),
                        "game_good", "Good Listening Challenge score",
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
                        "listening_score": total_score,
                        "listening_accuracy": accuracy_pct,
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
                    "correct_answer": r.correct_answer,
                    "is_correct": r.is_correct,
                    "attempts_used": r.attempts_used,
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
