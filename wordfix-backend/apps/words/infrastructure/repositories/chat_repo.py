"""
Chat repository implementation using Django ORM.
"""

from uuid import UUID

from django.utils import timezone

from apps.common.exceptions import EntityNotFoundError
from apps.words.domain.entities import (
    ChatMessageEntity,
    ChatSessionEntity,
)
from apps.words.domain.repositories import AbstractChatRepository
from apps.words.infrastructure.models import (
    ChatMessage,
    ChatSession,
)


class DjangoChatRepository(AbstractChatRepository):
    """Concrete implementation of AbstractChatRepository using Django ORM."""

    def _session_to_entity(self, session) -> ChatSessionEntity:
        return ChatSessionEntity(
            id=session.id,
            user_id=session.user_id,
            topic=session.topic,
            started_at=session.started_at,
            ended_at=session.ended_at,
            message_count=session.message_count,
            target_words=session.target_words or [],
            words_practiced=[w.original_word for w in session.words_practiced.all()],
            is_active=session.is_active,
            created_at=session.created_at,
            updated_at=session.updated_at,
        )

    def _message_to_entity(self, message) -> ChatMessageEntity:
        return ChatMessageEntity(
            id=message.id,
            session_id=message.session_id,
            role=message.role,
            content=message.content,
            corrections=message.corrections or [],
            words_used=message.words_used or [],
            order=message.order,
            is_active=message.is_active,
            created_at=message.created_at,
            updated_at=message.updated_at,
        )

    def create_session(self, user_id: UUID, topic: str = "", target_words: list | None = None) -> ChatSessionEntity:
        session = ChatSession.objects.create(
            user_id=user_id,
            topic=topic,
            target_words=target_words or [],
        )
        return self._session_to_entity(session)

    def get_session(self, session_id: UUID, user_id: UUID) -> ChatSessionEntity:
        try:
            session = ChatSession.objects.get(id=session_id, user_id=user_id)
            return self._session_to_entity(session)
        except ChatSession.DoesNotExist:
            raise EntityNotFoundError("Chat session not found.")

    def update_session(self, session_id: UUID, **kwargs) -> ChatSessionEntity:
        try:
            session = ChatSession.objects.get(id=session_id)
        except ChatSession.DoesNotExist:
            raise EntityNotFoundError("Chat session not found.")
        for field, value in kwargs.items():
            setattr(session, field, value)
        session.save()
        return self._session_to_entity(session)

    def end_session(self, session_id: UUID) -> ChatSessionEntity:
        try:
            session = ChatSession.objects.get(id=session_id)
        except ChatSession.DoesNotExist:
            raise EntityNotFoundError("Chat session not found.")
        session.is_active = False
        session.ended_at = timezone.now()
        session.save()
        return self._session_to_entity(session)

    def get_sessions_by_user(self, user_id: UUID, page: int = 1, page_size: int = 20) -> tuple[list[ChatSessionEntity], int]:
        qs = ChatSession.objects.filter(user_id=user_id).prefetch_related("words_practiced").order_by("-started_at")
        total = qs.count()
        offset = (page - 1) * page_size
        sessions = qs[offset:offset + page_size]
        return [self._session_to_entity(s) for s in sessions], total

    def add_message(self, session_id: UUID, role: str, content: str, corrections: list | None = None,
                    words_used: list | None = None, order: int = 0) -> ChatMessageEntity:
        message = ChatMessage.objects.create(
            session_id=session_id,
            role=role,
            content=content,
            corrections=corrections or [],
            words_used=words_used or [],
            order=order,
        )
        return self._message_to_entity(message)

    def get_messages(self, session_id: UUID, limit: int | None = None) -> list[ChatMessageEntity]:
        qs = ChatMessage.objects.filter(session_id=session_id).order_by("order")
        if limit:
            qs = qs[:limit]
        return [self._message_to_entity(m) for m in qs]

    def add_words_practiced(self, session_id: UUID, words: list[str]) -> None:
        try:
            session = ChatSession.objects.get(id=session_id)
            from apps.words.infrastructure.models import Word
            for word_str in words:
                word_objs = Word.objects.filter(
                    user_id=session.user_id,
                    original_word__iexact=word_str,
                )
                session.words_practiced.add(*word_objs)
        except ChatSession.DoesNotExist:
            pass
