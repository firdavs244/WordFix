"""
Word and category entities.

Pure Python classes representing core word-related business objects.
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
    # Archive fields
    is_archived: bool = False
    archived_at: datetime | None = None
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
