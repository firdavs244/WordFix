"""
User domain repository interfaces.

Abstract base classes defining the contract for data access.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from .entities import UserEntity


class AbstractUserRepository(ABC):
    """
    Abstract repository interface for User entity.
    """

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> UserEntity:
        """Retrieve a user by their unique ID. Raises EntityNotFoundError."""
        ...

    @abstractmethod
    def get_by_email(self, email: str) -> UserEntity:
        """Retrieve a user by email. Raises EntityNotFoundError."""
        ...

    @abstractmethod
    def create(self, email: str, username: str, password: str, **kwargs) -> UserEntity:
        """Create a new user and return entity."""
        ...

    @abstractmethod
    def update(self, user_id: UUID, **kwargs) -> UserEntity:
        """Update user fields and return updated entity."""
        ...

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """Check if a user with the given email exists."""
        ...

    @abstractmethod
    def exists_by_username(self, username: str) -> bool:
        """Check if a user with the given username exists."""
        ...

    @abstractmethod
    def set_password(self, user_id: UUID, password: str) -> None:
        """Set user's password (hashed)."""
        ...

    @abstractmethod
    def check_password(self, user_id: UUID, password: str) -> bool:
        """Check if the raw password matches the stored hash."""
        ...

    @abstractmethod
    def get_user_language_info(self, user_id: UUID) -> dict:
        """Get user's language and proficiency info for enrichment.

        Returns dict with keys: native_language, proficiency_level, daily_goal
        """
        ...
