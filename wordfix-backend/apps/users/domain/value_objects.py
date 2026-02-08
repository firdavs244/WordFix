"""
User domain value objects.

Immutable objects that represent values without identity.
"""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """
    Email value object with built-in validation.
    """

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Email is required.")
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, self.value):
            raise ValueError(f"Invalid email format: {self.value}")

    @property
    def normalized(self) -> str:
        """Return lowercase normalized email."""
        return self.value.strip().lower()

    def __str__(self) -> str:
        return self.normalized

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Email):
            return self.normalized == other.normalized
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.normalized)

    @property
    def domain(self) -> str:
        """Extract the domain part of the email."""
        return self.normalized.split("@")[1]


@dataclass(frozen=True)
class Password:
    """
    Password value object with validation rules.

    Requirements: min 8 chars + at least 1 digit.
    """

    value: str

    MIN_LENGTH = 8

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Password is required.")
        if len(self.value) < self.MIN_LENGTH:
            raise ValueError(
                f"Password must be at least {self.MIN_LENGTH} characters long."
            )
        if not re.search(r"\d", self.value):
            raise ValueError("Password must contain at least one digit.")

    def __str__(self) -> str:
        return "********"
