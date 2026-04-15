"""
Concrete session repository implementation using Django ORM.
"""

from uuid import UUID

from django.utils import timezone

from apps.immersive.domain.entities import ConversationTurnEntity, ImmersiveSessionEntity
from apps.immersive.domain.repositories import AbstractSessionRepository
from apps.immersive.infrastructure.models import ConversationTurn, ImmersiveSession


class DjangoSessionRepository(AbstractSessionRepository):
    """Django ORM implementation of session repository."""

    def _to_session_entity(self, obj: ImmersiveSession) -> ImmersiveSessionEntity:
        return ImmersiveSessionEntity(
            id=obj.id,
            user_id=obj.user_id,
            scenario_id=obj.scenario_id,
            npc_id=obj.npc_id,
            status=obj.status,
            input_mode=obj.input_mode,
            score=obj.score,
            max_score=obj.max_score,
            turn_count=obj.turn_count,
            hints_used=obj.hints_used,
            started_at=obj.started_at,
            completed_at=obj.completed_at,
            duration_seconds=obj.duration_seconds,
            xp_earned=obj.xp_earned,
            fluency_score=obj.fluency_score,
            accuracy_score=obj.accuracy_score,
            vocabulary_score=obj.vocabulary_score,
            task_completion_score=obj.task_completion_score,
            conversation_context=obj.conversation_context,
            is_active=obj.is_active,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )

    def _to_turn_entity(self, obj: ConversationTurn) -> ConversationTurnEntity:
        return ConversationTurnEntity(
            id=obj.id,
            session_id=obj.session_id,
            turn_number=obj.turn_number,
            role=obj.role,
            content=obj.content,
            audio_url=obj.audio_url,
            input_type=obj.input_type,
            grammar_errors=obj.grammar_errors,
            vocabulary_feedback=obj.vocabulary_feedback,
            relevance_score=obj.relevance_score,
            grammar_score=obj.grammar_score,
            vocabulary_score_turn=obj.vocabulary_score_turn,
            score=obj.score,
            hint_level_used=obj.hint_level_used,
            response_time_ms=obj.response_time_ms,
            is_active=obj.is_active,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )

    def create(self, user_id: UUID, scenario_id: UUID, npc_id: UUID, input_mode: str = "text") -> ImmersiveSessionEntity:
        obj = ImmersiveSession.objects.create(
            user_id=user_id,
            scenario_id=scenario_id,
            npc_id=npc_id,
            input_mode=input_mode,
        )
        return self._to_session_entity(obj)

    def get_by_id(self, session_id: UUID, user_id: UUID) -> ImmersiveSessionEntity:
        obj = ImmersiveSession.objects.get(id=session_id, user_id=user_id, is_active=True)
        return self._to_session_entity(obj)

    def update(self, session_id: UUID, **kwargs) -> ImmersiveSessionEntity:
        ImmersiveSession.objects.filter(id=session_id).update(**kwargs)
        obj = ImmersiveSession.objects.get(id=session_id)
        return self._to_session_entity(obj)

    def get_active_session(self, user_id: UUID) -> ImmersiveSessionEntity | None:
        obj = ImmersiveSession.objects.filter(
            user_id=user_id, status="active", is_active=True
        ).first()
        return self._to_session_entity(obj) if obj else None

    def get_history(self, user_id: UUID, page: int = 1, page_size: int = 20) -> tuple[list[ImmersiveSessionEntity], int]:
        qs = ImmersiveSession.objects.filter(user_id=user_id, is_active=True).order_by("-started_at")
        total = qs.count()
        start = (page - 1) * page_size
        items = [self._to_session_entity(obj) for obj in qs[start:start + page_size]]
        return items, total

    def create_turn(self, session_id: UUID, **kwargs) -> ConversationTurnEntity:
        obj = ConversationTurn.objects.create(session_id=session_id, **kwargs)
        # Update session turn count
        ImmersiveSession.objects.filter(id=session_id).update(
            turn_count=ConversationTurn.objects.filter(session_id=session_id, role="user").count()
        )
        return self._to_turn_entity(obj)

    def get_turns(self, session_id: UUID) -> list[ConversationTurnEntity]:
        qs = ConversationTurn.objects.filter(session_id=session_id, is_active=True).order_by("turn_number")
        return [self._to_turn_entity(obj) for obj in qs]
