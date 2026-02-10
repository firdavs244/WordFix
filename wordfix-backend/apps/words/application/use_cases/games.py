"""
Game use cases: Speed Round, Word Match, Word Context.
"""

import logging
import random
from datetime import datetime, timezone
from uuid import UUID

from apps.common.exceptions import ValidationError
from core.interfaces.ai_provider import AIProviderError

logger = logging.getLogger(__name__)


class StartSpeedRoundUseCase:
    """Start a speed round game."""

    def __init__(self, word_repo, game_session_repo):
        self.word_repo = word_repo
        self.game_session_repo = game_session_repo

    def execute(self, user_id):
        user_id = UUID(str(user_id))

        words, _ = self.word_repo.get_all_by_user(
            user_id=user_id, page=1, page_size=200
        )
        eligible = [w for w in words if w.confidence_score < 90 and w.translation]
        if len(eligible) < 5:
            if len(words) < 5:
                raise ValidationError("You need at least 5 words with translations to play.")
            eligible = [w for w in words if w.translation]
            if len(eligible) < 5:
                raise ValidationError("You need at least 5 words with translations to play.")

        random.shuffle(eligible)
        selected = eligible[:min(25, len(eligible))]

        all_translations = [w.translation for w in words if w.translation]

        # Build word items with options
        items = []
        for word in selected:
            distractors = [t for t in all_translations if t != word.translation]
            random.shuffle(distractors)
            options = [word.translation] + distractors[:3]
            while len(options) < 4:
                options.append(f"option_{len(options)}")
            random.shuffle(options)
            items.append({
                "word_id": str(word.id),
                "word": word.original_word,
                "correct_translation": word.translation,
                "options": options,
            })

        session = self.game_session_repo.create(
            user_id=user_id,
            game_type="speed_round",
            max_score=len(items),
        )

        return {
            "session_id": str(session.id),
            "words": items,
            "time_limit": 60,
        }


class SubmitSpeedRoundUseCase:
    """Submit speed round results."""

    def __init__(self, word_repo, game_session_repo, sr_service, activity_repo,
                 challenge_repo=None, xp_service=None):
        self.word_repo = word_repo
        self.game_session_repo = game_session_repo
        self.sr_service = sr_service
        self.activity_repo = activity_repo
        self.challenge_repo = challenge_repo
        self.xp_service = xp_service

    def execute(self, session_id, user_id, answers, duration_seconds=60):
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        correct = 0
        incorrect = 0
        current_combo = 0
        max_combo = 0
        total_combo_bonus = 0
        now = datetime.now(timezone.utc)

        for ans in answers:
            word_id = UUID(str(ans["word_id"]))
            try:
                word = self.word_repo.get_by_id(word_id=word_id, user_id=user_id)
                is_right = ans.get("selected_answer", "").strip().lower() == word.translation.strip().lower()

                quality = 4 if is_right else 1
                self.sr_service.calculate_next_review(word, quality, now=now)
                word.review_count += 1
                if is_right:
                    word.correct_count += 1
                    correct += 1
                    current_combo += 1
                    if current_combo > max_combo:
                        max_combo = current_combo
                    # Combo XP bonus
                    from apps.words.domain.services import ComboService
                    combo_xp, _ = ComboService.calculate_combo_xp(10, current_combo)
                    total_combo_bonus += (combo_xp - 10)
                else:
                    word.incorrect_count += 1
                    incorrect += 1
                    current_combo = 0
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
                logger.warning(f"Speed round answer processing failed: {e}")
                incorrect += 1
                current_combo = 0

        total = correct + incorrect
        score_pct = round((correct / total * 100) if total > 0 else 0, 1)
        xp = correct * 10
        if total > 0 and (correct / total) >= 0.8:
            xp *= 2

        session = self.game_session_repo.update(
            session_id=session_id,
            is_completed=True,
            completed_at=now,
            score=correct,
            correct_answers=correct,
            incorrect_answers=incorrect,
            duration_seconds=duration_seconds,
            xp_earned=xp,
            current_combo=current_combo,
            max_combo=max_combo,
            combo_xp_bonus=total_combo_bonus,
        )

        # Update daily activity
        try:
            activity = self.activity_repo.get_or_create_today(user_id=user_id)
            self.activity_repo.update(
                activity_id=activity.id,
                words_reviewed=activity.words_reviewed + total,
                correct_answers=activity.correct_answers + correct,
                incorrect_answers=activity.incorrect_answers + incorrect,
                xp_earned=activity.xp_earned + xp,
            )
        except Exception:
            pass

        # Update daily challenge progress
        if self.challenge_repo:
            try:
                from apps.words.application.use_cases.daily_challenges import UpdateChallengeProgressUseCase
                challenge_uc = UpdateChallengeProgressUseCase(
                    self.challenge_repo, self.xp_service
                )
                challenge_uc.execute(user_id, "play_game", amount=1)
            except Exception as e:
                logger.warning(f"Game challenge progress failed: {e}")

        return session


class StartWordMatchUseCase:
    """Start a word match game."""

    def __init__(self, word_repo, game_session_repo):
        self.word_repo = word_repo
        self.game_session_repo = game_session_repo

    def execute(self, user_id, pair_count=8):
        user_id = UUID(str(user_id))

        words, _ = self.word_repo.get_all_by_user(
            user_id=user_id, page=1, page_size=200
        )
        eligible = [w for w in words if w.translation]
        if len(eligible) < 5:
            raise ValidationError("You need at least 5 words with translations to play.")

        random.shuffle(eligible)
        selected = eligible[:min(pair_count, len(eligible))]

        word_items = [
            {"word_id": str(w.id), "word": w.original_word}
            for w in selected
        ]
        translations = [w.translation for w in selected]
        random.shuffle(translations)

        session = self.game_session_repo.create(
            user_id=user_id,
            game_type="word_match",
            max_score=len(selected),
        )

        return {
            "session_id": str(session.id),
            "words": word_items,
            "translations": translations,
            "pair_count": len(selected),
        }


class SubmitWordMatchUseCase:
    """Submit word match results."""

    def __init__(self, word_repo, game_session_repo, sr_service, activity_repo,
                 challenge_repo=None, xp_service=None):
        self.word_repo = word_repo
        self.game_session_repo = game_session_repo
        self.sr_service = sr_service
        self.activity_repo = activity_repo
        self.challenge_repo = challenge_repo
        self.xp_service = xp_service

    def execute(self, session_id, user_id, pairs, time_seconds):
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        correct = 0
        incorrect = 0
        current_combo = 0
        max_combo = 0
        total_combo_bonus = 0
        now = datetime.now(timezone.utc)

        for pair in pairs:
            word_id = UUID(str(pair["word_id"]))
            try:
                word = self.word_repo.get_by_id(word_id=word_id, user_id=user_id)
                is_right = pair.get("matched_translation", "").strip().lower() == word.translation.strip().lower()

                quality = 4 if is_right else 1
                self.sr_service.calculate_next_review(word, quality, now=now)
                word.review_count += 1
                if is_right:
                    word.correct_count += 1
                    correct += 1
                    current_combo += 1
                    if current_combo > max_combo:
                        max_combo = current_combo
                    from apps.words.domain.services import ComboService
                    combo_xp, _ = ComboService.calculate_combo_xp(10, current_combo)
                    total_combo_bonus += (combo_xp - 10)
                else:
                    word.incorrect_count += 1
                    incorrect += 1
                    current_combo = 0
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
                logger.warning(f"Word match pair processing failed: {e}")
                incorrect += 1
                current_combo = 0

        total = correct + incorrect
        xp = correct * 10
        if total > 0 and (correct / total) >= 0.8:
            xp *= 2

        session = self.game_session_repo.update(
            session_id=session_id,
            is_completed=True,
            completed_at=now,
            score=correct,
            correct_answers=correct,
            incorrect_answers=incorrect,
            duration_seconds=time_seconds,
            xp_earned=xp,
            current_combo=current_combo,
            max_combo=max_combo,
            combo_xp_bonus=total_combo_bonus,
        )

        # Update daily activity
        try:
            activity = self.activity_repo.get_or_create_today(user_id=user_id)
            self.activity_repo.update(
                activity_id=activity.id,
                words_reviewed=activity.words_reviewed + total,
                correct_answers=activity.correct_answers + correct,
                incorrect_answers=activity.incorrect_answers + incorrect,
                xp_earned=activity.xp_earned + xp,
            )
        except Exception:
            pass

        # Update daily challenge progress
        if self.challenge_repo:
            try:
                from apps.words.application.use_cases.daily_challenges import UpdateChallengeProgressUseCase
                challenge_uc = UpdateChallengeProgressUseCase(
                    self.challenge_repo, self.xp_service
                )
                challenge_uc.execute(user_id, "play_game", amount=1)
            except Exception as e:
                logger.warning(f"Game challenge progress failed: {e}")

        return session


class StartWordContextUseCase:
    """Start a word context game."""

    def __init__(self, word_repo, game_session_repo, ai_provider=None,
                 user_repo=None, prompt_template="", language_map=None):
        self.word_repo = word_repo
        self.game_session_repo = game_session_repo
        self.ai_provider = ai_provider
        self.user_repo = user_repo
        self.prompt_template = prompt_template
        self.language_map = language_map or {}

    def execute(self, user_id):
        user_id = UUID(str(user_id))

        words, _ = self.word_repo.get_all_by_user(
            user_id=user_id, page=1, page_size=200
        )
        eligible = [w for w in words if w.translation]
        if len(eligible) < 5:
            raise ValidationError("You need at least 5 words with translations to play.")

        random.shuffle(eligible)
        selected = eligible[:5]
        all_translations = [w.translation for w in words if w.translation]

        # Try AI generation
        questions = self._generate_ai_context(selected, user_id, all_translations)
        if not questions:
            questions = self._generate_fallback_context(selected, all_translations)

        session = self.game_session_repo.create(
            user_id=user_id,
            game_type="word_context",
            max_score=len(questions),
        )

        return {
            "session_id": str(session.id),
            "questions": questions,
        }

    def _generate_ai_context(self, words, user_id, all_translations):
        """Try generating context via AI."""
        if not self.ai_provider or not self.ai_provider.is_available():
            return []

        native_lang = "Uzbek"
        proficiency = "B1"
        if self.user_repo:
            try:
                user_info = self.user_repo.get_user_language_info(user_id)
                native_lang = self.language_map.get(
                    user_info.get("native_language", "uz"), "Uzbek"
                )
                proficiency = user_info.get("proficiency_level", "B1")
            except Exception:
                pass

        words_list = ", ".join(w.original_word for w in words)

        try:
            if not self.prompt_template:
                return []
            prompt = self.prompt_template.format(
                native_language=native_lang,
                proficiency_level=proficiency,
                words_list=words_list,
            )
            result = self.ai_provider.generate_json(prompt=prompt, max_tokens=2000)
            if not isinstance(result, list):
                return []

            questions = []
            word_map = {w.original_word.lower(): w for w in words}
            for item in result[:5]:
                word_key = item.get("word", "").lower()
                word_entity = word_map.get(word_key, words[len(questions) % len(words)])
                questions.append({
                    "word_id": str(word_entity.id),
                    "context": item.get("context", ""),
                    "correct_answer": item.get("correct_answer", word_entity.original_word),
                    "options": item.get("options", []),
                })
            return questions
        except Exception as e:
            logger.warning(f"AI context generation failed: {e}")
            return []

    def _generate_fallback_context(self, words, all_translations):
        """Generate context questions from example sentences."""
        questions = []
        for word in words:
            if word.example_sentence:
                context = word.example_sentence.replace(
                    word.original_word, "___"
                ).replace(
                    word.original_word.capitalize(), "___"
                )
            else:
                context = f'"___" means "{word.translation}"'

            correct = word.original_word
            other_words = [w.original_word for w in words if w.id != word.id]
            random.shuffle(other_words)
            options = [correct] + other_words[:3]
            while len(options) < 4:
                options.append(f"word_{len(options)}")
            random.shuffle(options)

            questions.append({
                "word_id": str(word.id),
                "context": context,
                "correct_answer": correct,
                "options": options,
            })
        return questions


class SubmitWordContextUseCase:
    """Submit word context game results."""

    def __init__(self, word_repo, game_session_repo, sr_service, activity_repo,
                 challenge_repo=None, xp_service=None):
        self.word_repo = word_repo
        self.game_session_repo = game_session_repo
        self.sr_service = sr_service
        self.activity_repo = activity_repo
        self.challenge_repo = challenge_repo
        self.xp_service = xp_service

    def execute(self, session_id, user_id, answers):
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        correct = 0
        incorrect = 0
        current_combo = 0
        max_combo = 0
        total_combo_bonus = 0
        now = datetime.now(timezone.utc)

        for ans in answers:
            word_id = UUID(str(ans["word_id"]))
            try:
                word = self.word_repo.get_by_id(word_id=word_id, user_id=user_id)
                is_right = ans.get("selected_answer", "").strip().lower() == word.original_word.strip().lower()

                quality = 4 if is_right else 1
                self.sr_service.calculate_next_review(word, quality, now=now)
                word.review_count += 1
                if is_right:
                    word.correct_count += 1
                    correct += 1
                    current_combo += 1
                    if current_combo > max_combo:
                        max_combo = current_combo
                    from apps.words.domain.services import ComboService
                    combo_xp, _ = ComboService.calculate_combo_xp(10, current_combo)
                    total_combo_bonus += (combo_xp - 10)
                else:
                    word.incorrect_count += 1
                    incorrect += 1
                    current_combo = 0
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
                logger.warning(f"Word context answer failed: {e}")
                incorrect += 1
                current_combo = 0

        total = correct + incorrect
        xp = correct * 10
        if total > 0 and (correct / total) >= 0.8:
            xp *= 2

        session = self.game_session_repo.update(
            session_id=session_id,
            is_completed=True,
            completed_at=now,
            score=correct,
            correct_answers=correct,
            incorrect_answers=incorrect,
            xp_earned=xp,
            current_combo=current_combo,
            max_combo=max_combo,
            combo_xp_bonus=total_combo_bonus,
        )

        # Update daily activity
        try:
            activity = self.activity_repo.get_or_create_today(user_id=user_id)
            self.activity_repo.update(
                activity_id=activity.id,
                words_reviewed=activity.words_reviewed + total,
                correct_answers=activity.correct_answers + correct,
                incorrect_answers=activity.incorrect_answers + incorrect,
                xp_earned=activity.xp_earned + xp,
            )
        except Exception:
            pass

        # Update daily challenge progress
        if self.challenge_repo:
            try:
                from apps.words.application.use_cases.daily_challenges import UpdateChallengeProgressUseCase
                challenge_uc = UpdateChallengeProgressUseCase(
                    self.challenge_repo, self.xp_service
                )
                challenge_uc.execute(user_id, "play_game", amount=1)
            except Exception as e:
                logger.warning(f"Game challenge progress failed: {e}")

        return session


class GetGameHistoryUseCase:
    """Get game session history."""

    def __init__(self, game_session_repo):
        self.game_session_repo = game_session_repo

    def execute(self, user_id, page=1, page_size=20):
        user_id = UUID(str(user_id))
        return self.game_session_repo.get_by_user(
            user_id=user_id, page=page, page_size=page_size
        )


class GetGameStatsUseCase:
    """Get game stats for a user."""

    def __init__(self, game_session_repo):
        self.game_session_repo = game_session_repo

    def execute(self, user_id):
        user_id = UUID(str(user_id))
        return self.game_session_repo.get_stats(user_id=user_id)
