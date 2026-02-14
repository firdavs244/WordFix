"""
Authentication use cases — register, login, Google OAuth.

CLEAN ARCHITECTURE: No Django/DRF/infrastructure imports.
Token generation is injected via callable.
"""

from datetime import datetime, timezone
from typing import Callable

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


class GoogleLoginUseCase:
    """Google OAuth login use case."""

    def __init__(self, repository: AbstractUserRepository, token_generator: Callable | None = None):
        self.repository = repository
        self.token_generator = token_generator

    def execute(self, google_user_info: dict) -> tuple:
        """
        Process Google login.

        Args:
            google_user_info: Dict with email, name, google_id keys.

        Returns: (UserEntity, tokens_dict, is_new_user)
        """
        import uuid

        email = google_user_info.get("email", "").strip().lower()
        name = google_user_info.get("name", "")

        if not email:
            raise ValidationError("Email is required from Google.")

        is_new_user = False

        try:
            user_entity = self.repository.get_by_email(email)
        except EntityNotFoundError:
            # Create new user
            username = f"user_{uuid.uuid4().hex[:8]}"
            user_entity = self.repository.create(
                email=email,
                username=username,
                password=uuid.uuid4().hex,  # Random password for OAuth users
                full_name=name,
            )
            is_new_user = True

        # Update last_login
        self.repository.update(user_entity.id, last_login=datetime.now(timezone.utc))

        # Generate tokens
        tokens = self.token_generator(user_entity.id) if self.token_generator else {}

        return user_entity, tokens, is_new_user
