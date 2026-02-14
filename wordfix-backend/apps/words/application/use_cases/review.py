"""
Review use cases.
"""

import logging
from datetime import datetime, timezone
from uuid import UUID

from apps.common.exceptions import ValidationError

logger = logging.getLogger(__name__)


class GetReviewWordsUseCase:
    """Get words due for review."""

    def __init__(self, word_repo):
        self.word_repo = word_repo

    def execute(self, user_id: UUID, limit: int = 20, session_type: str = "review"):
        return self.word_repo.get_review_words(
            user_id=user_id, limit=limit, session_type=session_type,
        )


class StartReviewSessionUseCase:
    """Start a new review session."""

    def __init__(self, session_repo, word_repo=None):
        self.session_repo = session_repo
        self.word_repo = word_repo

    def execute(self, user_id: UUID, session_type: str = "review", word_count: int = 0):
        # Check that user has enough words for review
        if self.word_repo:
            count = self.word_repo.get_count_by_user(user_id)
            if count < 5:
                from apps.common.exceptions import ValidationError
                raise ValidationError(
                    f"You need at least 5 words to start a review session. "
                    f"You currently have {count} word(s). Please add more words first."
                )
        return self.session_repo.create(
            user_id=user_id,
            session_type=session_type,
            total_words=word_count,
        )


class SubmitReviewAnswerUseCase:
    """Submit a review answer and update all related data."""

    def __init__(self, word_repo, session_repo, log_repo, sr_service, streak_repo, activity_repo,
                 confusing_pair_repo=None, challenge_repo=None, xp_service=None):
        self.word_repo = word_repo
        self.session_repo = session_repo
        self.log_repo = log_repo
        self.sr_service = sr_service
        self.streak_repo = streak_repo
        self.activity_repo = activity_repo
        self.confusing_pair_repo = confusing_pair_repo
        self.challenge_repo = challenge_repo
        self.xp_service = xp_service

    def execute(self, session_id, word_id, user_id, quality: int, response_time_ms: int = 0,
                user_answer: str = ""):
        if quality < 0 or quality > 5:
            raise ValidationError("Quality must be between 0 and 5.")

        session_id = UUID(str(session_id))
        word_id = UUID(str(word_id))
        user_id = UUID(str(user_id))

        # Get word
        word = self.word_repo.get_by_id(word_id=word_id, user_id=user_id)

        # Save previous state
        prev_confidence = word.confidence_score
        prev_interval = word.interval_days

        # Apply SM-2
        now = datetime.now(timezone.utc)
        self.sr_service.calculate_next_review(word, quality, now=now)

        # Update review counts
        word.review_count += 1
        is_correct = quality >= 3
        if is_correct:
            word.correct_count += 1
        else:
            word.incorrect_count += 1
        word.last_reviewed_at = now

        # Save word
        self.word_repo.update(
            word_id=word_id,
            user_id=user_id,
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

        # Create review log
        self.log_repo.create(
            session_id=session_id,
            user_id=user_id,
            word_id=word_id,
            quality=quality,
            response_time_ms=response_time_ms,
            is_correct=is_correct,
            previous_confidence=prev_confidence,
            new_confidence=word.confidence_score,
            previous_interval=prev_interval,
            new_interval=word.interval_days,
        )

        # Update session stats + combo
        session = self.session_repo.get_by_id(session_id=session_id, user_id=user_id)
        update_data = {
            "total_words": session.total_words + 1,
        }
        if is_correct:
            update_data["correct_count"] = session.correct_count + 1
            # Combo tracking
            new_combo = session.current_combo + 1
            update_data["current_combo"] = new_combo
            if new_combo > session.max_combo:
                update_data["max_combo"] = new_combo
            # Calculate combo XP bonus
            from apps.words.domain.services import ComboService
            combo_xp, multiplier = ComboService.calculate_combo_xp(quality * 3, new_combo)
            combo_bonus = combo_xp - (quality * 3)
            update_data["combo_xp_bonus"] = session.combo_xp_bonus + combo_bonus
        else:
            update_data["incorrect_count"] = session.incorrect_count + 1
            update_data["current_combo"] = 0  # Reset combo on wrong answer
        session = self.session_repo.update(session_id=session_id, **update_data)

        # Confusion detection (when wrong answer provided)
        confusion_detected = None
        if not is_correct and user_answer and self.confusing_pair_repo:
            try:
                from .confusing_pairs import DetectConfusionUseCase
                detect_uc = DetectConfusionUseCase(self.word_repo, self.confusing_pair_repo)
                confusion_detected = detect_uc.execute(user_id, word_id, user_answer)
            except Exception as e:
                logger.warning(f"Confusion detection failed: {e}")

        # Record mistake pattern (adaptive intelligence)
        if not is_correct and user_answer:
            try:
                from apps.users.presentation.learning_deps import get_record_mistake_use_case
                mistake_uc = get_record_mistake_use_case()
                correct_text = word.original_word if hasattr(word, "original_word") else ""
                mistake_uc.execute(user_id, user_answer, correct_text, context="review")
            except Exception as e:
                logger.warning(f"Mistake pattern recording failed: {e}")

        # Update daily challenge progress
        if self.challenge_repo:
            try:
                from .daily_challenges import UpdateChallengeProgressUseCase
                challenge_uc = UpdateChallengeProgressUseCase(
                    self.challenge_repo, self.xp_service
                )
                challenge_uc.execute(user_id, "review_words", amount=1)
                # Check for combo streak challenge
                if is_correct and session.current_combo >= 5:
                    challenge_uc.execute(user_id, "combo_streak", amount=1)
                # Check for mastered word challenge
                if word.is_mastered:
                    challenge_uc.execute(user_id, "master_word", amount=1)
            except Exception as e:
                logger.warning(f"Challenge progress update failed: {e}")

        # Update daily activity
        activity = self.activity_repo.get_or_create_today(user_id=user_id)
        act_update = {
            "words_reviewed": activity.words_reviewed + 1,
        }
        if is_correct:
            act_update["correct_answers"] = activity.correct_answers + 1
        else:
            act_update["incorrect_answers"] = activity.incorrect_answers + 1
        if word.is_mastered:
            act_update["words_mastered"] = activity.words_mastered + 1
        act_update["xp_earned"] = activity.xp_earned + (quality * 3)
        self.activity_repo.update(activity_id=activity.id, **act_update)

        # Update streak
        from .streak import UpdateStreakUseCase
        streak_uc = UpdateStreakUseCase(self.streak_repo)
        streak = streak_uc.execute(user_id=user_id)

        result = {
            "word": word,
            "session": session,
            "streak": streak,
            "is_correct": is_correct,
            "combo": {
                "current": session.current_combo,
                "max": session.max_combo,
                "multiplier": ComboService.get_multiplier(session.current_combo) if is_correct else 1.0,
            },
        }
        if confusion_detected:
            result["confusion_detected"] = {
                "pair_id": str(confusion_detected.id),
                "confusion_count": confusion_detected.confusion_count,
            }
        return result


class CompleteReviewSessionUseCase:
    """Complete a review session."""

    def __init__(self, session_repo, log_repo, challenge_repo=None, xp_service=None):
        self.session_repo = session_repo
        self.log_repo = log_repo
        self.challenge_repo = challenge_repo
        self.xp_service = xp_service

    def execute(self, session_id, user_id):
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        session = self.session_repo.get_by_id(session_id=session_id, user_id=user_id)
        now = datetime.now(timezone.utc)

        duration = 0
        if session.started_at:
            duration = int((now - session.started_at).total_seconds())

        # Calculate average quality
        logs = self.log_repo.get_by_session(session_id=session_id)
        avg_quality = 0.0
        if logs:
            avg_quality = sum(log.quality for log in logs) / len(logs)

        updated = self.session_repo.update(
            session_id=session_id,
            is_completed=True,
            completed_at=now,
            duration_seconds=duration,
            average_quality=round(avg_quality, 2),
        )

        # Check for perfect review challenge
        if self.challenge_repo and session.total_words > 0:
            is_perfect = session.incorrect_count == 0 and session.correct_count > 0
            if is_perfect:
                try:
                    from .daily_challenges import UpdateChallengeProgressUseCase
                    challenge_uc = UpdateChallengeProgressUseCase(
                        self.challenge_repo, self.xp_service
                    )
                    challenge_uc.execute(user_id, "perfect_review", amount=1)
                except Exception as e:
                    logger.warning(f"Perfect review challenge update failed: {e}")

        return updated


class GetReviewSummaryUseCase:
    """Get review summary for dashboard display."""

    def __init__(self, word_repo, streak_repo, activity_repo, user_repo=None):
        self.word_repo = word_repo
        self.streak_repo = streak_repo
        self.activity_repo = activity_repo
        self.user_repo = user_repo

    def execute(self, user_id: UUID) -> dict:
        user_id = UUID(str(user_id))

        # Get stats from repository
        stats = self.word_repo.get_review_summary_stats(user_id=user_id)

        # Daily goal
        daily_goal = 10
        if self.user_repo:
            try:
                user_info = self.user_repo.get_user_language_info(user_id)
                daily_goal = user_info.get("daily_goal", 10)
            except Exception:
                pass

        # Today's activity
        activity = self.activity_repo.get_or_create_today(user_id=user_id)
        daily_progress_pct = min(
            round((activity.words_reviewed / daily_goal * 100) if daily_goal > 0 else 0, 1),
            100.0,
        )

        # Streak
        streak = self.streak_repo.get_or_create(user_id=user_id)

        return {
            **stats,
            "daily_goal": daily_goal,
            "daily_progress_pct": daily_progress_pct,
            "streak": {
                "current": streak.current_streak,
                "longest": streak.longest_streak,
                "last_activity": str(streak.last_activity_date) if streak.last_activity_date else None,
            },
        }
