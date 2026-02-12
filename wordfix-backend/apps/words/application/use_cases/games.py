"""
Game use cases: Speed Round, Word Match, Word Context, Story Builder, Listening Challenge.
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


# =============================================================================
# STORY BUILDER
# =============================================================================


class StartStoryBuilderUseCase:
    """Start a Story Builder game."""

    def __init__(self, word_repo, game_repo, ai_provider, user_repo=None, language_map=None):
        self.word_repo = word_repo
        self.game_repo = game_repo
        self.ai_provider = ai_provider
        self.user_repo = user_repo
        self.language_map = language_map or {}

    def execute(self, user_id, genre=None) -> dict:
        user_id = UUID(str(user_id))

        words, _ = self.word_repo.get_all_by_user(user_id=user_id, page=1, page_size=200)
        eligible = [w for w in words if w.confidence_score < 80 and w.original_word]
        if len(eligible) < 5:
            eligible = [w for w in words if w.original_word]
        if len(eligible) < 5:
            raise ValidationError(
                "You need at least 5 words to play. Add more words first!"
            )

        random.shuffle(eligible)
        selected = eligible[:5]

        from core.services.ai.prompts import STORY_GENRES
        if not genre or genre not in STORY_GENRES:
            genre = random.choice(STORY_GENRES)

        # Get user language info
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

        # Try AI generation for story start
        first_target = selected[0].original_word
        ai_text = self._generate_story_start(first_target, genre, proficiency, native_lang)

        session = self.game_repo.create(
            user_id=user_id,
            game_type="story_builder",
            max_score=100,
        )

        # First round: AI wrote story using words[0], user must use words[1]
        next_target = selected[1].original_word
        self.game_repo.create_story_round(
            session_id=session.id,
            round_number=1,
            ai_text=ai_text,
            target_words=[next_target],
        )

        return {
            "session_id": str(session.id),
            "genre": genre,
            "ai_text": ai_text,
            "target_words": [next_target],
            "total_rounds": 5,
            "current_round": 1,
            "all_target_words": [w.original_word for w in selected],
        }

    def _generate_story_start(self, target_word, genre, proficiency, native_lang):
        """Generate story start via AI, with fallback."""
        if self.ai_provider and hasattr(self.ai_provider, "is_available"):
            if not self.ai_provider.is_available():
                return self._fallback_story_start(target_word, genre)
        elif not self.ai_provider:
            return self._fallback_story_start(target_word, genre)

        try:
            from core.services.ai.prompts import STORY_START_PROMPT
            prompt = STORY_START_PROMPT.format(
                proficiency_level=proficiency,
                native_language=native_lang,
                genre=genre,
                target_word=target_word,
            )
            result = self.ai_provider.generate_json(prompt=prompt, max_tokens=500)
            if isinstance(result, dict) and result.get("story_text"):
                return result["story_text"]
            return self._fallback_story_start(target_word, genre)
        except Exception as e:
            logger.warning(f"AI story start failed: {e}")
            return self._fallback_story_start(target_word, genre)

    @staticmethod
    def _fallback_story_start(target_word, genre):
        """Return a hardcoded story template."""
        from core.services.ai.prompts import STORY_FALLBACK_TEMPLATES
        templates = STORY_FALLBACK_TEMPLATES.get(genre)
        if not templates:
            templates = STORY_FALLBACK_TEMPLATES.get("adventure", [
                "One day, something unexpected happened related to {target_word}."
            ])
        template = random.choice(templates)
        return template.format(target_word=target_word, name="Alex")


class SubmitStoryRoundUseCase:
    """Submit a story round answer."""

    def __init__(self, word_repo, game_repo, ai_provider, sr_service,
                 xp_service=None, user_repo=None, language_map=None,
                 challenge_repo=None):
        self.word_repo = word_repo
        self.game_repo = game_repo
        self.ai_provider = ai_provider
        self.sr_service = sr_service
        self.xp_service = xp_service
        self.user_repo = user_repo
        self.language_map = language_map or {}
        self.challenge_repo = challenge_repo

    def execute(self, session_id, user_id, user_text) -> dict:
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        session = self.game_repo.get_by_id(session_id=session_id, user_id=user_id)
        if session.is_completed:
            raise ValidationError("This game session is already completed.")

        rounds = self.game_repo.get_story_rounds(session_id)
        if not rounds:
            raise ValidationError("No story rounds found for this session.")

        current_round = rounds[-1]
        target_words = current_round.target_words or []

        # Build story so far
        story_parts = []
        for r in rounds:
            story_parts.append(r.ai_text)
            if r.user_text:
                story_parts.append(r.user_text)
        story_so_far = " ".join(story_parts)

        round_number = current_round.round_number
        is_last_round = round_number >= 5

        # Determine next target word
        all_rounds = rounds
        used_targets = set()
        for r in all_rounds:
            used_targets.update(r.target_words)
        words, _ = self.word_repo.get_all_by_user(user_id=user_id, page=1, page_size=200)
        eligible = [w for w in words if w.original_word not in used_targets and w.confidence_score < 80]
        if not eligible:
            eligible = [w for w in words if w.original_word not in used_targets]
        next_target_word = eligible[0].original_word if eligible and not is_last_round else ""

        # Get user info
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

        # AI analysis + continuation
        ai_result = self._analyze_with_ai(
            story_so_far, user_text, target_words, next_target_word,
            proficiency, native_lang, is_last_round,
        )

        # Update current round
        words_used = ai_result.get("words_used_correctly", [])
        grammar_corrections = ai_result.get("grammar_corrections", [])
        score = ai_result.get("score", 0)
        is_correct = len(words_used) > 0

        self.game_repo.update_story_round(
            round_id=current_round.id,
            user_text=user_text,
            words_used=words_used,
            grammar_corrections=grammar_corrections,
            is_correct_usage=is_correct,
            score=score,
        )

        # SR update for used target words
        now = datetime.now(timezone.utc)
        for tw in target_words:
            word_entities = [w for w in words if w.original_word.lower() == tw.lower()]
            if word_entities:
                word_entity = word_entities[0]
                quality = 4 if tw.lower() in [wu.lower() for wu in words_used] else 2
                try:
                    self.sr_service.calculate_next_review(word_entity, quality, now=now)
                    word_entity.review_count += 1
                    if quality >= 4:
                        word_entity.correct_count += 1
                    word_entity.last_reviewed_at = now
                    self.word_repo.update(
                        word_id=word_entity.id, user_id=user_id,
                        confidence_score=word_entity.confidence_score,
                        next_review_at=word_entity.next_review_at,
                        review_count=word_entity.review_count,
                        correct_count=word_entity.correct_count,
                        last_reviewed_at=word_entity.last_reviewed_at,
                        is_mastered=word_entity.is_mastered,
                        easiness_factor=word_entity.easiness_factor,
                        repetition_number=word_entity.repetition_number,
                        interval_days=word_entity.interval_days,
                    )
                except Exception as e:
                    logger.warning(f"SR update failed for story word: {e}")

        # Combo
        current_combo = session.current_combo
        max_combo = session.max_combo
        combo_bonus = 0
        if is_correct:
            current_combo += 1
            if current_combo > max_combo:
                max_combo = current_combo
            from apps.words.domain.services import ComboService
            combo_xp, multiplier = ComboService.calculate_combo_xp(10, current_combo)
            combo_bonus = combo_xp - 10
        else:
            current_combo = 0
            multiplier = 1.0

        # XP proportional to score
        xp_earned = max(score // 2, 1)
        xp_earned += combo_bonus

        self.game_repo.update(
            session_id=session_id,
            score=session.score + score,
            current_combo=current_combo,
            max_combo=max_combo,
            combo_xp_bonus=session.combo_xp_bonus + combo_bonus,
        )

        # Create next round if not last
        next_round_data = None
        if not is_last_round:
            continuation = ai_result.get("continuation", "The story continues...")
            next_target = [next_target_word] if next_target_word else []
            new_round = self.game_repo.create_story_round(
                session_id=session_id,
                round_number=round_number + 1,
                ai_text=continuation,
                target_words=next_target,
            )
            next_round_data = {
                "ai_text": continuation,
                "target_words": next_target,
                "round_number": round_number + 1,
            }

        # Daily challenge
        if self.challenge_repo and self.xp_service:
            try:
                from apps.words.application.use_cases.daily_challenges import (
                    UpdateChallengeProgressUseCase,
                )
                uc = UpdateChallengeProgressUseCase(self.challenge_repo, self.xp_service)
                uc.execute(user_id, "play_game", amount=1)
            except Exception as e:
                logger.warning(f"Challenge progress failed: {e}")

        return {
            "round_result": {
                "score": score,
                "words_used": words_used,
                "grammar_corrections": grammar_corrections,
                "feedback": ai_result.get("feedback", ""),
                "is_correct_usage": is_correct,
            },
            "next_round": next_round_data,
            "session_stats": {
                "total_score": session.score + score,
                "rounds_completed": round_number,
            },
            "combo": current_combo,
            "multiplier": multiplier if is_correct else 1.0,
            "xp_earned": xp_earned,
        }

    def _analyze_with_ai(self, story_so_far, user_text, target_words,
                         next_target_word, proficiency, native_lang, is_last):
        """Analyze user text with AI, fallback if unavailable."""
        if not self.ai_provider:
            return self._fallback_analyze(user_text, target_words, is_last)

        if hasattr(self.ai_provider, "is_available") and not self.ai_provider.is_available():
            return self._fallback_analyze(user_text, target_words, is_last)

        try:
            from core.services.ai.prompts import STORY_CONTINUE_PROMPT
            prompt = STORY_CONTINUE_PROMPT.format(
                proficiency_level=proficiency,
                native_language=native_lang,
                story_so_far=story_so_far,
                user_text=user_text,
                target_words=", ".join(target_words),
                next_target_word=next_target_word or "continue",
            )
            result = self.ai_provider.generate_json(prompt=prompt, max_tokens=1000)
            if isinstance(result, dict):
                return result
            return self._fallback_analyze(user_text, target_words, is_last)
        except Exception as e:
            logger.warning(f"AI story continue failed: {e}")
            return self._fallback_analyze(user_text, target_words, is_last)

    @staticmethod
    def _fallback_analyze(user_text, target_words, is_last):
        """Simple check without AI."""
        text_lower = user_text.lower()
        used = [w for w in target_words if w.lower() in text_lower]
        not_used = [w for w in target_words if w.lower() not in text_lower]
        score = 0
        if used:
            score += 8
        if len(user_text) > 20:
            score += 7
        score += 5  # default creativity

        continuation = "The story continues..." if not is_last else ""

        return {
            "words_used_correctly": used,
            "words_not_used": not_used,
            "grammar_corrections": [],
            "is_grammar_good": True,
            "feedback": "Good job! Keep going!",
            "continuation": continuation,
            "score": min(score, 20),
        }


class CompleteStoryBuilderUseCase:
    """Complete a Story Builder game."""

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

        rounds = self.game_repo.get_story_rounds(session_id)
        total_score = sum(r.score for r in rounds)

        now = datetime.now(timezone.utc)
        self.game_repo.update(
            session_id=session_id,
            is_completed=True,
            completed_at=now,
            score=total_score,
        )

        # XP
        xp_earned = 0
        if self.xp_service:
            try:
                from apps.users.domain.services import XP_REWARDS
                xp_result = self.xp_service.award_xp(
                    user_id, XP_REWARDS.get("game_complete", 15),
                    "game_complete", "Completed Story Builder",
                )
                xp_earned = xp_result.get("xp_gained", 0)

                if total_score >= 80:
                    bonus = self.xp_service.award_xp(
                        user_id, XP_REWARDS.get("game_good", 10),
                        "game_good", "Good Story Builder score",
                    )
                    xp_earned += bonus.get("xp_gained", 0)
            except Exception as e:
                logger.warning(f"XP award failed: {e}")

        # Badges
        badges_earned = []
        if self.badge_service:
            try:
                badges_earned = self.badge_service.check_and_award_badges(
                    user_id, context={"story_builder_score": total_score}
                )
            except Exception as e:
                logger.warning(f"Badge check failed: {e}")

        # Build full story
        story_parts = []
        for r in rounds:
            story_parts.append(r.ai_text)
            if r.user_text:
                story_parts.append(r.user_text)
        full_story = " ".join(story_parts)

        return {
            "total_score": total_score,
            "max_score": 100,
            "rounds": [
                {
                    "round_number": r.round_number,
                    "score": r.score,
                    "words_used": r.words_used,
                    "grammar_corrections": r.grammar_corrections,
                }
                for r in rounds
            ],
            "full_story": full_story,
            "xp_earned": xp_earned,
            "badges_earned": [
                {"code": b.code, "name": b.name, "icon": b.icon}
                for b in badges_earned
            ],
        }


# =============================================================================
# LISTENING CHALLENGE
# =============================================================================


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
