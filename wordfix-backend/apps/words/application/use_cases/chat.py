"""
AI Chat use cases.
"""

import json
import logging
import random
from datetime import datetime, timezone
from uuid import UUID

logger = logging.getLogger(__name__)


class StartChatUseCase:
    """Start a new chat session with AI tutor."""

    def __init__(self, chat_repo, word_repo, ai_provider, user_repo, prompt_template: str, language_map: dict):
        self.chat_repo = chat_repo
        self.word_repo = word_repo
        self.ai_provider = ai_provider
        self.user_repo = user_repo
        self.prompt_template = prompt_template
        self.language_map = language_map

    def execute(self, user_id, topic: str | None = None) -> dict:
        user_id = UUID(str(user_id))

        # 1. Get user's words with low confidence (5-10 random)
        words, _ = self.word_repo.get_all_by_user(
            user_id=user_id, page=1, page_size=10000,
        )
        low_confidence = [w for w in words if w.confidence_score < 80]
        if not low_confidence:
            low_confidence = words[:10] if words else []
        target_words = random.sample(low_confidence, min(len(low_confidence), 7))
        target_word_list = [w.original_word for w in target_words]

        # 2. Get topic
        topics = ["daily life", "travel", "technology", "movies", "food", "sports", "nature", "education"]
        if not topic:
            topic = random.choice(topics)

        # 3. Get user language info
        lang_info = self.user_repo.get_user_language_info(user_id)
        native_lang = self.language_map.get(
            lang_info.get("native_language", "uz"), "Uzbek"
        )
        proficiency = lang_info.get("proficiency_level", "A2")

        # 4. Create session
        session = self.chat_repo.create_session(
            user_id=user_id,
            topic=topic,
            target_words=target_word_list,
        )

        # 5. Get first AI message
        system_prompt = self.prompt_template.format(
            proficiency_level=proficiency,
            native_language=native_lang,
            topic=topic,
            words_list=", ".join(target_word_list) if target_word_list else "general vocabulary",
        )

        first_message_content = f"Hi! Let's talk about {topic}. "
        if target_word_list:
            first_message_content += f"I'd love to help you practice some words like '{target_word_list[0]}'. What do you think about {topic}?"

        if self.ai_provider:
            try:
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Start the conversation about {topic}. Use one of these words naturally: {', '.join(target_word_list)}"},
                ]
                ai_response = self.ai_provider.generate_chat(messages, max_tokens=500, temperature=0.7)
                try:
                    parsed = json.loads(ai_response)
                    first_message_content = parsed.get("message", first_message_content)
                except (json.JSONDecodeError, AttributeError):
                    first_message_content = ai_response if isinstance(ai_response, str) else first_message_content
            except Exception as e:
                logger.warning(f"AI failed for first chat message: {e}")

        # 6. Save first message
        self.chat_repo.add_message(
            session_id=session.id,
            role="assistant",
            content=first_message_content,
            order=1,
        )
        self.chat_repo.update_session(session.id, message_count=1)

        return {
            "session_id": str(session.id),
            "topic": topic,
            "target_words": target_word_list,
            "first_message": {
                "role": "assistant",
                "content": first_message_content,
                "corrections": [],
                "words_used": [],
            },
        }


class SendChatMessageUseCase:
    """Send a message in a chat session and get AI response."""

    def __init__(self, chat_repo, ai_provider, word_repo, user_repo,
                 sr_service, prompt_template: str, language_map: dict):
        self.chat_repo = chat_repo
        self.ai_provider = ai_provider
        self.word_repo = word_repo
        self.user_repo = user_repo
        self.sr_service = sr_service
        self.prompt_template = prompt_template
        self.language_map = language_map

    def execute(self, session_id, user_id, message_text: str) -> dict:
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        # 1. Get session
        session = self.chat_repo.get_session(session_id, user_id)

        # 2. Get previous messages (last 10 for context)
        messages = self.chat_repo.get_messages(session_id, limit=10)

        # 3. Save user message
        user_msg_order = session.message_count + 1
        self.chat_repo.add_message(
            session_id=session_id,
            role="user",
            content=message_text,
            order=user_msg_order,
        )

        # 4. Build conversation history for AI
        lang_info = self.user_repo.get_user_language_info(user_id)
        native_lang = self.language_map.get(
            lang_info.get("native_language", "uz"), "Uzbek"
        )
        proficiency = lang_info.get("proficiency_level", "A2")

        target_words = session.target_words if hasattr(session, 'target_words') else []

        system_prompt = self.prompt_template.format(
            proficiency_level=proficiency,
            native_language=native_lang,
            topic=session.topic or "general",
            words_list=", ".join(target_words) if target_words else "general vocabulary",
        )

        chat_history = [{"role": "system", "content": system_prompt}]
        for msg in messages:
            chat_history.append({"role": msg.role, "content": msg.content})
        chat_history.append({"role": "user", "content": message_text})

        # 5. Get AI response
        ai_message = "That's interesting! Tell me more."
        corrections = []
        words_used = []
        encouragement = ""

        if self.ai_provider:
            try:
                ai_raw = self.ai_provider.generate_chat(chat_history, max_tokens=800, temperature=0.7)
                try:
                    parsed = json.loads(ai_raw)
                    ai_message = parsed.get("message", ai_raw)
                    corrections = parsed.get("corrections", [])
                    words_used = parsed.get("words_used_by_student", [])
                    encouragement = parsed.get("encouragement", "")
                except (json.JSONDecodeError, AttributeError):
                    ai_message = ai_raw if isinstance(ai_raw, str) else ai_message
            except Exception as e:
                logger.warning(f"AI chat response failed: {e}")

        # 6. Save AI message
        ai_msg_order = user_msg_order + 1
        self.chat_repo.add_message(
            session_id=session_id,
            role="assistant",
            content=ai_message,
            corrections=corrections,
            words_used=words_used,
            order=ai_msg_order,
        )

        # 7. Update session
        self.chat_repo.update_session(session_id, message_count=ai_msg_order)

        # 8. If user used target words, update SR
        xp_earned = 0
        if words_used and target_words:
            for word_str in words_used:
                if word_str.lower() in [tw.lower() for tw in target_words]:
                    try:
                        words_all, _ = self.word_repo.get_all_by_user(user_id=user_id, page=1, page_size=10000)
                        for w in words_all:
                            if w.original_word.lower() == word_str.lower():
                                now = datetime.now(timezone.utc)
                                self.sr_service.calculate_next_review(w, quality=4, now=now)
                                self.word_repo.update(
                                    word_id=w.id,
                                    user_id=user_id,
                                    confidence_score=w.confidence_score,
                                    easiness_factor=w.easiness_factor,
                                    repetition_number=w.repetition_number,
                                    interval_days=w.interval_days,
                                    next_review_at=w.next_review_at,
                                    review_count=w.review_count + 1,
                                    correct_count=w.correct_count + 1,
                                    last_reviewed_at=now,
                                )
                                xp_earned += 10
                                break
                    except Exception as e:
                        logger.warning(f"Failed to update SR for word '{word_str}': {e}")

            # Update words practiced
            self.chat_repo.add_words_practiced(session_id, words_used)

        return {
            "ai_message": ai_message,
            "corrections": corrections,
            "words_used": words_used,
            "encouragement": encouragement,
            "xp_earned": xp_earned,
        }


class EndChatUseCase:
    """End a chat session."""

    def __init__(self, chat_repo):
        self.chat_repo = chat_repo

    def execute(self, session_id, user_id) -> dict:
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        session = self.chat_repo.get_session(session_id, user_id)
        self.chat_repo.end_session(session_id)

        return {
            "session_id": str(session.id),
            "topic": session.topic,
            "message_count": session.message_count,
            "words_practiced": session.words_practiced if hasattr(session, 'words_practiced') else [],
        }


class GetChatHistoryUseCase:
    """Get paginated chat history for a user."""

    def __init__(self, chat_repo):
        self.chat_repo = chat_repo

    def execute(self, user_id, page: int = 1, page_size: int = 20) -> tuple:
        user_id = UUID(str(user_id))
        return self.chat_repo.get_sessions_by_user(user_id, page=page, page_size=page_size)


class GetChatSessionDetailUseCase:
    """Get a chat session with all messages."""

    def __init__(self, chat_repo):
        self.chat_repo = chat_repo

    def execute(self, session_id, user_id) -> dict:
        session_id = UUID(str(session_id))
        user_id = UUID(str(user_id))

        session = self.chat_repo.get_session(session_id, user_id)
        messages = self.chat_repo.get_messages(session_id)

        return {
            "session": session,
            "messages": messages,
        }
