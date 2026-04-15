"""Conversation use cases — Submit text/voice responses, request hints."""

import logging
from datetime import datetime, timezone
from uuid import UUID

from apps.common.exceptions import ValidationError
from apps.immersive.infrastructure.services.tts_audio import save_npc_audio

logger = logging.getLogger(__name__)


class SubmitResponseUseCase:
    """Submit a text response in an immersive conversation."""

    def __init__(self, session_repo, scenario_repo, ai_provider, scoring_service, tts_provider=None, user_repo=None, language_map=None):
        self.session_repo = session_repo
        self.scenario_repo = scenario_repo
        self.ai_provider = ai_provider
        self.scoring_service = scoring_service
        self.tts_provider = tts_provider
        self.user_repo = user_repo
        self.language_map = language_map or {}

    def execute(self, session_id, user_id, user_message, input_type="text", response_time_ms=None) -> dict:
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        session = self.session_repo.get_by_id(session_id, user_id)
        if session.status != "active":
            raise ValidationError("Session is not active.")

        scenario = self.scenario_repo.get_by_id(session.scenario_id)
        npc = self.scenario_repo.get_npc_by_id(session.npc_id)

        # Check session timeout
        if session.started_at and scenario.time_limit_seconds:
            elapsed = (datetime.now(timezone.utc) - session.started_at).total_seconds()
            if elapsed > scenario.time_limit_seconds:
                self.session_repo.update(session_id, status="timeout")
                raise ValidationError("Session has timed out.")

        # Get user info
        native_lang = "Uzbek"
        proficiency = scenario.difficulty
        if self.user_repo:
            try:
                user_info = self.user_repo.get_user_language_info(user_id)
                native_lang = self.language_map.get(
                    user_info.get("native_language", "uz"), "Uzbek"
                )
                proficiency = user_info.get("proficiency_level", proficiency)
            except Exception:
                pass

        # Get last NPC message from context
        context = session.conversation_context or []
        last_npc_msg = ""
        for msg in reversed(context):
            if msg.get("role") == "assistant":
                last_npc_msg = msg.get("content", "")
                break

        # Analyze user's response with AI
        analysis = self._analyze_response(user_message, last_npc_msg, scenario, proficiency, native_lang)

        # Calculate turn score
        turn_score = self.scoring_service.calculate_turn_score(
            grammar_score=analysis.get("grammar_score", 0.5),
            vocabulary_score=analysis.get("vocabulary_score", 0.5),
            relevance_score=analysis.get("relevance_score", 0.5),
        )

        # Determine turn number
        turns = self.session_repo.get_turns(session_id)
        next_turn = len(turns) + 1

        # Save user turn
        user_turn = self.session_repo.create_turn(
            session_id=session_id,
            turn_number=next_turn,
            role="user",
            content=user_message,
            input_type=input_type,
            grammar_errors=analysis.get("grammar_errors", []),
            vocabulary_feedback=analysis.get("vocabulary_feedback", []),
            relevance_score=analysis.get("relevance_score", 0.0),
            grammar_score=analysis.get("grammar_score", 0.0),
            vocabulary_score_turn=analysis.get("vocabulary_score", 0.0),
            score=turn_score,
            response_time_ms=response_time_ms,
        )

        # Update conversation context
        context.append({"role": "user", "content": user_message})

        # Check if max turns reached
        user_turn_count = sum(1 for t in turns if t.role == "user") + 1
        is_last_turn = user_turn_count >= scenario.max_turns

        # Generate NPC response
        npc_response = ""
        npc_audio_url = ""
        if not is_last_turn:
            npc_response = self._generate_npc_response(npc, scenario, context, user_message, proficiency, native_lang)
            context.append({"role": "assistant", "content": npc_response})

            # TTS for NPC response — save to disk and get URL
            voice_lang = npc.voice_config.get("language", "en") if npc.voice_config else "en"
            npc_audio_url = save_npc_audio(self.tts_provider, npc_response, session_id, next_turn + 1, voice_lang)

            # Save NPC turn
            self.session_repo.create_turn(
                session_id=session_id,
                turn_number=next_turn + 1,
                role="npc",
                content=npc_response,
                audio_url=npc_audio_url,
            )

        # Update session context
        self.session_repo.update(session_id, conversation_context=context)

        return {
            "user_analysis": {
                "grammar_errors": analysis.get("grammar_errors", []),
                "vocabulary_feedback": analysis.get("vocabulary_feedback", []),
                "relevance_score": analysis.get("relevance_score", 0.0),
                "grammar_score": analysis.get("grammar_score", 0.0),
                "vocabulary_score": analysis.get("vocabulary_score", 0.0),
                "score": turn_score,
            },
            "npc_response": {
                "content": npc_response,
                "audio_url": npc_audio_url,
            } if not is_last_turn else None,
            "session_stats": {
                "turn_count": user_turn_count,
                "max_turns": scenario.max_turns,
                "is_last_turn": is_last_turn,
            },
        }

    def _analyze_response(self, user_message, npc_message, scenario, proficiency, native_lang):
        """Analyze user's response with AI."""
        if not self.ai_provider or (hasattr(self.ai_provider, "is_available") and not self.ai_provider.is_available()):
            return self._fallback_analysis(user_message)

        try:
            from core.services.ai.prompts.immersive_prompts import IMMERSIVE_ANALYZE_RESPONSE_PROMPT
            prompt = IMMERSIVE_ANALYZE_RESPONSE_PROMPT.format(
                proficiency_level=proficiency,
                native_language=native_lang,
                scenario_description=scenario.description,
                npc_message=npc_message,
                user_message=user_message,
            )
            result = self.ai_provider.generate_json(prompt=prompt, max_tokens=800)
            if isinstance(result, dict):
                return result
            return self._fallback_analysis(user_message)
        except Exception as e:
            logger.warning("AI analysis failed: %s", e)
            return self._fallback_analysis(user_message)

    @staticmethod
    def _fallback_analysis(user_message):
        """Basic fallback analysis without AI."""
        word_count = len(user_message.split())
        base_score = min(word_count / 10.0, 1.0)
        return {
            "grammar_errors": [],
            "vocabulary_feedback": [],
            "relevance_score": 0.7 if word_count >= 3 else 0.3,
            "grammar_score": base_score,
            "vocabulary_score": base_score,
        }

    def _generate_npc_response(self, npc, scenario, context, user_message, proficiency, native_lang):
        """Generate NPC's response via AI."""
        if not self.ai_provider or (hasattr(self.ai_provider, "is_available") and not self.ai_provider.is_available()):
            return self._fallback_npc_response(npc)

        try:
            from core.services.ai.prompts.immersive_prompts import IMMERSIVE_NPC_CONTINUE_PROMPT
            history = "\n".join(
                f"{'NPC' if m['role'] == 'assistant' else 'Student'}: {m['content']}"
                for m in context
            )
            prompt = IMMERSIVE_NPC_CONTINUE_PROMPT.format(
                npc_name=npc.name,
                npc_role=npc.role,
                conversation_history=history,
                user_message=user_message,
                proficiency_level=proficiency,
            )
            result = self.ai_provider.generate_text(prompt=prompt, max_tokens=200, temperature=0.8)
            return result.strip() if result else self._fallback_npc_response(npc)
        except Exception as e:
            logger.warning("AI NPC response failed: %s", e)
            return self._fallback_npc_response(npc)

    @staticmethod
    def _fallback_npc_response(npc):
        """Simple fallback NPC response."""
        return f"That's interesting! Please tell me more about that."


class SubmitVoiceResponseUseCase:
    """Submit a voice response — transcribe then delegate to SubmitResponseUseCase."""

    def __init__(self, stt_service, submit_response_use_case):
        self.stt_service = stt_service
        self.submit_response_use_case = submit_response_use_case

    def execute(self, session_id, user_id, audio_data, filename="audio.webm", language="en", response_time_ms=None) -> dict:
        # Transcribe audio
        transcribed_text = self.stt_service.transcribe(
            audio_data=audio_data,
            language=language,
            filename=filename,
        )

        if not transcribed_text.strip():
            raise ValidationError("Could not transcribe audio. Please try again or type your response.")

        # Delegate to text response handler
        result = self.submit_response_use_case.execute(
            session_id=session_id,
            user_id=user_id,
            user_message=transcribed_text,
            input_type="voice",
            response_time_ms=response_time_ms,
        )

        result["transcribed_text"] = transcribed_text
        return result


class RequestHintUseCase:
    """Request a hint for the current conversation turn."""

    def __init__(self, session_repo, scenario_repo, ai_provider, user_repo=None, language_map=None):
        self.session_repo = session_repo
        self.scenario_repo = scenario_repo
        self.ai_provider = ai_provider
        self.user_repo = user_repo
        self.language_map = language_map or {}

    MAX_HINTS_PER_SESSION = 3

    def execute(self, session_id, user_id) -> dict:
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        session = self.session_repo.get_by_id(session_id, user_id)
        if session.status != "active":
            raise ValidationError("Session is not active.")

        scenario = self.scenario_repo.get_by_id(session.scenario_id)

        # Check session timeout
        if session.started_at and scenario.time_limit_seconds:
            elapsed = (datetime.now(timezone.utc) - session.started_at).total_seconds()
            if elapsed > scenario.time_limit_seconds:
                self.session_repo.update(session_id, status="timeout")
                raise ValidationError("Session has timed out.")

        hint_level = session.hints_used + 1
        if hint_level > self.MAX_HINTS_PER_SESSION:
            raise ValidationError("Maximum hints reached for this session.")

        # Get user info
        native_lang = "Uzbek"
        proficiency = scenario.difficulty
        if self.user_repo:
            try:
                user_info = self.user_repo.get_user_language_info(user_id)
                native_lang = self.language_map.get(
                    user_info.get("native_language", "uz"), "Uzbek"
                )
                proficiency = user_info.get("proficiency_level", proficiency)
            except Exception:
                pass

        # Get last NPC message
        context = session.conversation_context or []
        last_npc_msg = ""
        for msg in reversed(context):
            if msg.get("role") == "assistant":
                last_npc_msg = msg.get("content", "")
                break

        hint = self._generate_hint(
            last_npc_msg, scenario, hint_level, proficiency, native_lang
        )

        # Update hints used
        self.session_repo.update(session_id, hints_used=hint_level)

        # Score penalty
        penalty = {1: 5, 2: 10, 3: 15}.get(hint_level, 0)

        return {
            "level": hint_level,
            "hint": hint.get("hint", "Try to respond naturally to what the NPC said."),
            "hint_uz": hint.get("hint_uz", "NPC aytganiga tabiiy javob berishga harakat qiling."),
            "score_penalty": penalty,
            "hints_remaining": self.MAX_HINTS_PER_SESSION - hint_level,
        }

    def _generate_hint(self, npc_message, scenario, hint_level, proficiency, native_lang):
        """Generate hint via AI."""
        if not self.ai_provider or (hasattr(self.ai_provider, "is_available") and not self.ai_provider.is_available()):
            return self._fallback_hint(hint_level)

        try:
            from core.services.ai.prompts.immersive_prompts import IMMERSIVE_HINT_PROMPT
            prompt = IMMERSIVE_HINT_PROMPT.format(
                proficiency_level=proficiency,
                native_language=native_lang,
                scenario_description=scenario.description,
                npc_message=npc_message,
                hint_level=hint_level,
                expected_phrases=", ".join(scenario.expected_phrases[:3]),
            )
            result = self.ai_provider.generate_json(prompt=prompt, max_tokens=300)
            if isinstance(result, dict):
                return result
            return self._fallback_hint(hint_level)
        except Exception as e:
            logger.warning("AI hint failed: %s", e)
            return self._fallback_hint(hint_level)

    @staticmethod
    def _fallback_hint(level):
        """Fallback hints."""
        hints = {
            1: {"hint": "Think about the context and respond naturally.", "hint_uz": "Kontekst haqida o'ylang va tabiiy javob bering."},
            2: {"hint": "Try using a greeting or introduction appropriate for this situation.", "hint_uz": "Bu vaziyatga mos salomlashish yoki tanishtirish ishlating."},
            3: {"hint": "Start with 'Hello, I would like to...' and explain your purpose.", "hint_uz": "'Hello, I would like to...' bilan boshlang va maqsadingizni tushuntiring."},
        }
        return hints.get(level, hints[1])
