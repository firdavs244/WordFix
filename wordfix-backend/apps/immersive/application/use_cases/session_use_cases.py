"""Immersive session use cases — Start and Complete."""

import logging
from datetime import datetime, timezone
from uuid import UUID

from apps.common.exceptions import ValidationError
from apps.immersive.infrastructure.services.tts_audio import save_npc_audio

logger = logging.getLogger(__name__)


class StartImmersiveSessionUseCase:
    """Start a new immersive conversation session."""

    def __init__(self, session_repo, scenario_repo, ai_provider, tts_provider=None, user_repo=None, language_map=None):
        self.session_repo = session_repo
        self.scenario_repo = scenario_repo
        self.ai_provider = ai_provider
        self.tts_provider = tts_provider
        self.user_repo = user_repo
        self.language_map = language_map or {}

    def execute(self, user_id, scenario_id, npc_id=None, input_mode="text") -> dict:
        user_id = UUID(str(user_id))
        scenario_id = UUID(str(scenario_id))

        # Check for active session
        active = self.session_repo.get_active_session(user_id)
        if active:
            self.session_repo.update(active.id, status="abandoned")

        scenario = self.scenario_repo.get_by_id(scenario_id)
        npcs = self.scenario_repo.get_npcs(scenario_id)
        if not npcs:
            raise ValidationError("No NPCs found for this scenario.")

        if npc_id:
            npc = self.scenario_repo.get_npc_by_id(UUID(str(npc_id)))
        else:
            npc = npcs[0]

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

        # Create session
        session = self.session_repo.create(
            user_id=user_id,
            scenario_id=scenario_id,
            npc_id=npc.id,
            input_mode=input_mode,
        )

        # Generate NPC greeting (use initial_greeting or AI)
        greeting_text = npc.initial_greeting or self._generate_greeting(npc, scenario, proficiency, native_lang)

        # Generate TTS audio for greeting
        voice_lang = npc.voice_config.get("language", "en") if npc.voice_config else "en"
        audio_url = save_npc_audio(self.tts_provider, greeting_text, session.id, 1, voice_lang)

        # Save first turn (NPC greeting)
        turn = self.session_repo.create_turn(
            session_id=session.id,
            turn_number=1,
            role="npc",
            content=greeting_text,
            audio_url=audio_url,
        )

        # Initialize conversation context
        context = [{"role": "assistant", "content": greeting_text}]
        self.session_repo.update(session.id, conversation_context=context)

        return {
            "session_id": str(session.id),
            "scenario": {
                "id": str(scenario.id),
                "name": scenario.name,
                "name_uz": scenario.name_uz,
                "location": scenario.location,
                "difficulty": scenario.difficulty,
                "scene_config": scenario.scene_config,
                "max_turns": scenario.max_turns,
                "time_limit_seconds": scenario.time_limit_seconds,
            },
            "npc": {
                "id": str(npc.id),
                "name": npc.name,
                "role": npc.role,
                "role_uz": npc.role_uz,
                "avatar_config": npc.avatar_config,
            },
            "first_turn": {
                "turn_number": turn.turn_number,
                "role": turn.role,
                "content": turn.content,
                "audio_url": turn.audio_url,
            },
        }

    def _generate_greeting(self, npc, scenario, proficiency, native_lang):
        """Generate NPC greeting via AI, with fallback."""
        if not self.ai_provider or (hasattr(self.ai_provider, "is_available") and not self.ai_provider.is_available()):
            return f"Hello! I'm {npc.name}. How can I help you today?"

        try:
            from core.services.ai.prompts.immersive_prompts import IMMERSIVE_NPC_SYSTEM_PROMPT
            system_prompt = IMMERSIVE_NPC_SYSTEM_PROMPT.format(
                npc_name=npc.name,
                npc_role=npc.role,
                scenario_location=scenario.location,
                npc_personality=npc.personality,
                native_language=native_lang,
                proficiency_level=proficiency,
                scenario_description=scenario.description,
                target_vocabulary=", ".join(scenario.target_vocabulary),
            )
            result = self.ai_provider.generate_text(
                prompt=f"{system_prompt}\n\nGenerate your opening greeting to the student who just arrived.",
                max_tokens=150,
                temperature=0.8,
            )
            return result.strip() if result else f"Hello! I'm {npc.name}. How can I help you today?"
        except Exception as e:
            logger.warning("AI greeting generation failed: %s", e)
            return f"Hello! I'm {npc.name}. How can I help you today?"


class CompleteImmersiveSessionUseCase:
    """Complete an immersive session and award XP."""

    def __init__(self, session_repo, scoring_service, xp_service=None, badge_service=None):
        self.session_repo = session_repo
        self.scoring_service = scoring_service
        self.xp_service = xp_service
        self.badge_service = badge_service

    def execute(self, session_id, user_id) -> dict:
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        session = self.session_repo.get_by_id(session_id, user_id)
        if session.status != "active":
            raise ValidationError("Session is not active.")

        turns = self.session_repo.get_turns(session_id)
        user_turns = [
            {
                "grammar_score": t.grammar_score,
                "vocabulary_score_turn": t.vocabulary_score_turn,
                "relevance_score": t.relevance_score,
                "score": t.score,
            }
            for t in turns if t.role == "user"
        ]

        scores = self.scoring_service.calculate_session_scores(
            turns=user_turns,
            hints_used=session.hints_used,
            max_turns=8,
        )

        now = datetime.now(timezone.utc)
        duration = int((now - session.started_at).total_seconds()) if session.started_at else 0

        # Calculate XP
        xp_earned = 0
        base_xp = max(scores["total_score"] // 2, 5)

        if self.xp_service:
            try:
                from apps.users.domain.services import XP_REWARDS
                xp_result = self.xp_service.award_xp(
                    user_id, base_xp,
                    "immersive_complete", "Completed Immersive Session",
                )
                xp_earned = xp_result.get("xp_gained", 0)

                if scores["total_score"] >= 80:
                    bonus = self.xp_service.award_xp(
                        user_id, XP_REWARDS.get("game_good", 10),
                        "immersive_good", "High score in Immersive Session",
                    )
                    xp_earned += bonus.get("xp_gained", 0)
            except Exception as e:
                logger.warning("XP award failed: %s", e)

        # Update session
        self.session_repo.update(
            session_id,
            status="completed",
            completed_at=now,
            duration_seconds=duration,
            score=scores["total_score"],
            fluency_score=scores["fluency_score"],
            accuracy_score=scores["accuracy_score"],
            vocabulary_score=scores["vocabulary_score"],
            task_completion_score=scores["task_completion_score"],
            xp_earned=xp_earned,
        )

        # Badges
        badges_earned = []
        if self.badge_service:
            try:
                badges_earned = self.badge_service.check_and_award_badges(
                    user_id, context={"immersive_score": scores["total_score"]}
                )
            except Exception as e:
                logger.warning("Badge check failed: %s", e)

        return {
            "session_id": str(session_id),
            "status": "completed",
            "total_score": scores["total_score"],
            "fluency_score": scores["fluency_score"],
            "accuracy_score": scores["accuracy_score"],
            "vocabulary_score": scores["vocabulary_score"],
            "task_completion_score": scores["task_completion_score"],
            "duration_seconds": duration,
            "turn_count": len(user_turns),
            "hints_used": session.hints_used,
            "xp_earned": xp_earned,
            "badges_earned": [
                {"code": b.code, "name": b.name, "icon": b.icon}
                for b in badges_earned
            ],
        }
