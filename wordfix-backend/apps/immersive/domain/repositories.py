"""
Immersive game abstract repository interfaces.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from .entities import (
    ConversationTurnEntity,
    ImmersiveScenarioEntity,
    ImmersiveSessionEntity,
    NPCCharacterEntity,
)


class AbstractScenarioRepository(ABC):
    """Abstract repository for ImmersiveScenario."""

    @abstractmethod
    def list_all(self, difficulty: str | None = None, location: str | None = None) -> list[ImmersiveScenarioEntity]:
        ...

    @abstractmethod
    def get_by_id(self, scenario_id: UUID) -> ImmersiveScenarioEntity:
        ...

    @abstractmethod
    def get_npcs(self, scenario_id: UUID) -> list[NPCCharacterEntity]:
        ...

    @abstractmethod
    def get_npc_by_id(self, npc_id: UUID) -> NPCCharacterEntity:
        ...


class AbstractSessionRepository(ABC):
    """Abstract repository for ImmersiveSession."""

    @abstractmethod
    def create(self, user_id: UUID, scenario_id: UUID, npc_id: UUID, input_mode: str = "text") -> ImmersiveSessionEntity:
        ...

    @abstractmethod
    def get_by_id(self, session_id: UUID, user_id: UUID) -> ImmersiveSessionEntity:
        ...

    @abstractmethod
    def update(self, session_id: UUID, **kwargs) -> ImmersiveSessionEntity:
        ...

    @abstractmethod
    def get_active_session(self, user_id: UUID) -> ImmersiveSessionEntity | None:
        ...

    @abstractmethod
    def get_history(self, user_id: UUID, page: int = 1, page_size: int = 20) -> tuple[list[ImmersiveSessionEntity], int]:
        ...

    @abstractmethod
    def create_turn(self, session_id: UUID, **kwargs) -> ConversationTurnEntity:
        ...

    @abstractmethod
    def get_turns(self, session_id: UUID) -> list[ConversationTurnEntity]:
        ...
