"""
Immersive game domain entities.

Dataclasses for immersive scenarios, sessions, conversation turns, and PvP battles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class ImmersiveScenarioEntity:
    """Pre-defined immersive learning scenario."""

    id: UUID = field(default_factory=uuid4)
    name: str = ""
    name_uz: str = ""
    description: str = ""
    description_uz: str = ""
    location: str = "office"
    difficulty: str = "A1"
    scene_config: dict = field(default_factory=dict)
    target_vocabulary: list = field(default_factory=list)
    expected_phrases: list = field(default_factory=list)
    max_turns: int = 8
    time_limit_seconds: int = 600
    xp_reward: int = 50
    order: int = 0
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class NPCCharacterEntity:
    """NPC character in an immersive scenario."""

    id: UUID = field(default_factory=uuid4)
    scenario_id: UUID = field(default_factory=uuid4)
    name: str = ""
    role: str = ""
    role_uz: str = ""
    personality: str = ""
    avatar_config: dict = field(default_factory=dict)
    initial_greeting: str = ""
    system_prompt: str = ""
    voice_config: dict = field(default_factory=dict)
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class ImmersiveSessionEntity:
    """A user's immersive game session."""

    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    scenario_id: UUID = field(default_factory=uuid4)
    npc_id: UUID = field(default_factory=uuid4)
    status: str = "active"
    input_mode: str = "text"
    score: int = 0
    max_score: int = 100
    turn_count: int = 0
    hints_used: int = 0
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_seconds: int = 0
    xp_earned: int = 0
    fluency_score: float = 0.0
    accuracy_score: float = 0.0
    vocabulary_score: float = 0.0
    task_completion_score: float = 0.0
    conversation_context: list = field(default_factory=list)
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class ConversationTurnEntity:
    """A single conversation turn in an immersive session."""

    id: UUID = field(default_factory=uuid4)
    session_id: UUID = field(default_factory=uuid4)
    turn_number: int = 1
    role: str = "user"
    content: str = ""
    audio_url: str = ""
    input_type: str = "text"
    grammar_errors: list = field(default_factory=list)
    vocabulary_feedback: list = field(default_factory=list)
    relevance_score: float = 0.0
    grammar_score: float = 0.0
    vocabulary_score_turn: float = 0.0
    score: int = 0
    hint_level_used: int = 0
    response_time_ms: int | None = None
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
