"""
User application use cases.

Orchestrate domain logic through repository interfaces.
All use cases receive repository via constructor (DI).

CLEAN ARCHITECTURE: No Django/DRF/infrastructure imports.
Token generation is injected via callable.
"""

from datetime import datetime, timezone
from typing import Callable
from uuid import UUID

from apps.common.exceptions import (
    AuthenticationError,
    EntityAlreadyExistsError,
    EntityNotFoundError,
    ValidationError,
)
from apps.users.domain.repositories import AbstractUserRepository


class RegisterUserUseCase:
    """Register a new user."""

    def __init__(self, repository: AbstractUserRepository, token_generator: Callable | None = None):
        self.repository = repository
        self.token_generator = token_generator

    def execute(self, data: dict) -> tuple:
        """
        Register a new user.

        Returns: (UserEntity, tokens_dict)
        """
        email = data["email"].strip().lower()
        username = data["username"]
        password = data["password"]
        full_name = data.get("full_name", "")
        native_language = data.get("native_language", "uz")
        learning_language = data.get("learning_language", "en")

        # Check duplicates
        if self.repository.exists_by_email(email):
            raise EntityAlreadyExistsError("A user with this email already exists.")

        if self.repository.exists_by_username(username):
            raise EntityAlreadyExistsError("A user with this username already exists.")

        # Create user
        user_entity = self.repository.create(
            email=email,
            username=username,
            password=password,
            full_name=full_name,
            native_language=native_language,
            learning_language=learning_language,
        )

        # Generate tokens
        tokens = self.token_generator(user_entity.id) if self.token_generator else {}

        return user_entity, tokens


class LoginUserUseCase:
    """Authenticate a user with email and password."""

    def __init__(self, repository: AbstractUserRepository, token_generator: Callable | None = None):
        self.repository = repository
        self.token_generator = token_generator

    def execute(self, email: str, password: str) -> tuple:
        """
        Login a user.

        Returns: (UserEntity, tokens_dict)
        """
        email = email.strip().lower()

        try:
            user_entity = self.repository.get_by_email(email)
        except EntityNotFoundError:
            raise AuthenticationError("Invalid email or password.")

        if not self.repository.check_password(user_entity.id, password):
            raise AuthenticationError("Invalid email or password.")

        if not user_entity.is_active:
            raise AuthenticationError("Your account has been deactivated.")

        # Update last_login
        self.repository.update(user_entity.id, last_login=datetime.now(timezone.utc))

        # Generate tokens
        tokens = self.token_generator(user_entity.id) if self.token_generator else {}

        return user_entity, tokens


class GetUserProfileUseCase:
    """Get user profile by ID."""

    def __init__(self, repository: AbstractUserRepository):
        self.repository = repository

    def execute(self, user_id: UUID):
        """Returns UserEntity."""
        return self.repository.get_by_id(user_id)


class UpdateUserProfileUseCase:
    """Update user profile."""

    ALLOWED_FIELDS = {
        "full_name",
        "native_language",
        "learning_language",
        "proficiency_level",
        "daily_goal",
        "timezone",
    }

    def __init__(self, repository: AbstractUserRepository):
        self.repository = repository

    def execute(self, user_id: UUID, data: dict):
        """Update allowed profile fields. Returns updated UserEntity."""
        filtered = {k: v for k, v in data.items() if k in self.ALLOWED_FIELDS}
        if not filtered:
            return self.repository.get_by_id(user_id)
        return self.repository.update(user_id, **filtered)


class ChangePasswordUseCase:
    """Change user password."""

    def __init__(self, repository: AbstractUserRepository):
        self.repository = repository

    def execute(self, user_id: UUID, old_password: str, new_password: str) -> bool:
        """Verify old password and set new one. Returns True on success."""
        if not self.repository.check_password(user_id, old_password):
            raise ValidationError("Current password is incorrect.")

        self.repository.set_password(user_id, new_password)
        return True
