"""
Word domain entities.

Pure Python classes representing core business objects for the Words domain.
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class WordCategoryEntity:
    """Word category entity."""

    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    name: str = ""
    color: str = "#6C5CE7"
    icon: str = "book"
    words_count: int = 0
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def validate(self) -> None:
        """Validate category data."""
        if not self.name or not self.name.strip():
            raise ValueError("Category name is required.")


@dataclass
class WordEntity:
    """
    Core Word entity - pure domain object.
    """

    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    original_word: str = ""
    translation: str = ""
    pronunciation: str = ""
    part_of_speech: str = ""
    definition: str = ""
    example_sentence: str = ""
    example_translation: str = ""
    synonyms: list = field(default_factory=list)
    antonyms: list = field(default_factory=list)
    collocations: list = field(default_factory=list)
    word_family: list = field(default_factory=list)
    image_url: str = ""
    audio_url: str = ""
    notes: str = ""
    mnemonic: str = ""
    usage_notes: str = ""
    category_id: UUID | None = None
    category: WordCategoryEntity | None = None
    tags: list = field(default_factory=list)
    difficulty_level: str = "medium"
    is_enriched: bool = False
    enrichment_status: str = "pending"
    enrichment_error: str = ""
    enriched_at: datetime | None = None
    confidence_score: float = 0.0
    next_review_at: datetime | None = None
    review_count: int = 0
    correct_count: int = 0
    incorrect_count: int = 0
    last_reviewed_at: datetime | None = None
    is_mastered: bool = False
    # SM-2 fields
    easiness_factor: float = 2.5
    repetition_number: int = 0
    interval_days: int = 0
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @property
    def accuracy_rate(self) -> float:
        """Calculate accuracy rate."""
        if self.review_count == 0:
            return 0.0
        return round((self.correct_count / self.review_count) * 100, 1)

    def validate(self) -> None:
        """Validate word data."""
        if not self.original_word or not self.original_word.strip():
            raise ValueError("Word is required.")
        if self.difficulty_level not in ("easy", "medium", "hard"):
            raise ValueError(f"Invalid difficulty level: {self.difficulty_level}")
        if self.confidence_score < 0:
            raise ValueError("Confidence score cannot be negative.")
        if self.confidence_score > 100:
            raise ValueError("Confidence score cannot exceed 100.")


@dataclass
class ReviewSessionEntity:
    """Review session entity."""

    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    total_words: int = 0
    correct_count: int = 0
    incorrect_count: int = 0
    average_quality: float = 0.0
    duration_seconds: int = 0
    session_type: str = "review"
    is_completed: bool = False
    current_combo: int = 0
    max_combo: int = 0
    combo_xp_bonus: int = 0
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class ReviewLogEntity:
    """Review log entity."""

    id: UUID = field(default_factory=uuid4)
    session_id: UUID | None = None
    user_id: UUID = field(default_factory=uuid4)
    word_id: UUID = field(default_factory=uuid4)
    quality: int = 0
    response_time_ms: int | None = None
    is_correct: bool = False
    reviewed_at: datetime | None = None
    previous_confidence: float = 0.0
    new_confidence: float = 0.0
    previous_interval: int = 0
    new_interval: int = 0
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class DailyStreakEntity:
    """Daily streak entity."""

    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    current_streak: int = 0
    longest_streak: int = 0
    last_activity_date: datetime | None = None
    streak_frozen_until: datetime | None = None
    total_review_days: int = 0
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class DailyActivityEntity:
    """Daily activity entity."""

    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    date: datetime | None = None
    words_reviewed: int = 0
    words_added: int = 0
    words_mastered: int = 0
    correct_answers: int = 0
    incorrect_answers: int = 0
    total_time_seconds: int = 0
    goal_completed: bool = False
    xp_earned: int = 0
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class TestSessionEntity:
    """Test session entity."""

    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    test_type: str = "mixed"
    difficulty: str = "adaptive"
    total_questions: int = 0
    correct_answers: int = 0
    incorrect_answers: int = 0
    score_percentage: float = 0.0
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_seconds: int = 0
    is_completed: bool = False
    current_combo: int = 0
    max_combo: int = 0
    combo_xp_bonus: int = 0
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class TestQuestionEntity:
    """Test question entity."""

    id: UUID = field(default_factory=uuid4)
    session_id: UUID = field(default_factory=uuid4)
    word_id: UUID = field(default_factory=uuid4)
    question_type: str = "multiple_choice"
    question_text: str = ""
    correct_answer: str = ""
    options: list = field(default_factory=list)
    user_answer: str = ""
    is_correct: bool | None = None
    response_time_ms: int | None = None
    explanation: str = ""
    order: int = 0
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class GameSessionEntity:
    """Game session entity."""

    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    game_type: str = "speed_round"
    score: int = 0
    max_score: int = 0
    correct_answers: int = 0
    incorrect_answers: int = 0
    duration_seconds: int = 0
    started_at: datetime | None = None
    completed_at: datetime | None = None
    is_completed: bool = False
    level: int = 1
    xp_earned: int = 0
    current_combo: int = 0
    max_combo: int = 0
    combo_xp_bonus: int = 0
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class ChatSessionEntity:
    """Chat session entity."""

    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    topic: str = ""
    started_at: datetime | None = None
    ended_at: datetime | None = None
    message_count: int = 0
    target_words: list = field(default_factory=list)
    words_practiced: list = field(default_factory=list)
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class ChatMessageEntity:
    """Chat message entity."""

    id: UUID = field(default_factory=uuid4)
    session_id: UUID = field(default_factory=uuid4)
    role: str = "user"
    content: str = ""
    corrections: list = field(default_factory=list)
    words_used: list = field(default_factory=list)
    order: int = 0
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class ConfusingPairEntity:
    """Confusing pair entity."""

    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    word_1_id: UUID = field(default_factory=uuid4)
    word_2_id: UUID = field(default_factory=uuid4)
    confusion_count: int = 1
    last_confused_at: datetime | None = None
    is_resolved: bool = False
    drill_data: dict = field(default_factory=dict)
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class DailyChallengeEntity:
    """Daily challenge entity."""

    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    date: datetime | None = None
    challenges: list = field(default_factory=list)
    all_completed: bool = False
    bonus_claimed: bool = False
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class WordDistractorEntity:
    """Word distractor entity."""

    id: UUID = field(default_factory=uuid4)
    word_id: UUID = field(default_factory=uuid4)
    distractors: list = field(default_factory=list)
    language: str = "uz"
    generated_by: str = "ai"
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
