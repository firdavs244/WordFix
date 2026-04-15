"""
Abstract user repository interface.

Mirrors the monolith's AbstractUserRepository contract.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from .entities import UserEntity


class AbstractUserRepository(ABC):
    """Abstract repository interface for User entity."""

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> UserEntity:
        """Retrieve a user by ID. Raises EntityNotFoundError."""
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity:
        """Retrieve a user by email. Raises EntityNotFoundError."""
        ...

    @abstractmethod
    async def create(self, email: str, username: str, password: str, **kwargs) -> UserEntity:
        """Create a new user and return entity."""
        ...

    @abstractmethod
    async def update(self, user_id: UUID, **kwargs) -> UserEntity:
        """Update user fields and return updated entity."""
        ...

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """Check if a user with the given email exists."""
        ...

    @abstractmethod
    async def exists_by_username(self, username: str) -> bool:
        """Check if a user with the given username exists."""
        ...

    @abstractmethod
    async def set_password(self, user_id: UUID, password: str) -> None:
        """Set user's password (hashed)."""
        ...

    @abstractmethod
    async def check_password(self, user_id: UUID, password: str) -> bool:
        """Check if the raw password matches the stored hash."""
        ...
