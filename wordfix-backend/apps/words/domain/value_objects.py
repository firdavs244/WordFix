"""
Word domain value objects.

Immutable objects representing values within the Words domain.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class WordText:
    """
    Value object representing the word text itself.

    Validates and normalizes the word text.
    """

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("Word text cannot be empty.")
        if len(self.value) > 100:
            raise ValueError("Word text cannot exceed 100 characters.")
        # Normalize: strip whitespace and convert to lowercase
        object.__setattr__(self, "value", self.value.strip().lower())

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Definition:
    """
    Value object representing a word definition.
    """

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("Definition cannot be empty.")
        object.__setattr__(self, "value", self.value.strip())

    def __str__(self) -> str:
        return self.value
