"""Story Builder game use cases."""

import logging
import random
from datetime import datetime, timezone
from uuid import UUID

from apps.common.exceptions import ValidationError

logger = logging.getLogger(__name__)


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

        # Count actual words in user text
        word_count = len(text_lower.split())

        score = 0

        # If text has fewer than 3 words, it's too short / meaningless
        if word_count < 3:
            score = 0
        else:
            # Target word usage: +8
            if used:
                score += 8
            # Reasonable length (>20 chars): +7
            if len(user_text) > 20:
                score += 7
            # Creativity: only if text has 5+ words and target word is used
            if word_count >= 5 and used:
                score += 5

        continuation = "The story continues..." if not is_last else ""

        feedback = "Good job! Keep going!" if score >= 10 else (
            "Try using the target word and write longer sentences." if score > 0
            else "Please write a meaningful sentence using the target word."
        )

        return {
            "words_used_correctly": used,
            "words_not_used": not_used,
            "grammar_corrections": [],
            "is_grammar_good": word_count >= 3,
            "feedback": feedback,
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
