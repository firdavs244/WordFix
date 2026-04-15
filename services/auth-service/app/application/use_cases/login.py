"""
Login user use case.

Port of monolith's LoginUserUseCase with async support.
"""

from datetime import datetime, timezone

from wordfix_shared.exceptions import AuthenticationError, EntityNotFoundError

from ...domain.repositories import AbstractUserRepository
from ...infrastructure.jwt_service import JWTService


class LoginUserUseCase:
    """Authenticate a user with email and password."""

    def __init__(self, repository: AbstractUserRepository, jwt_service: JWTService):
        self.repository = repository
        self.jwt_service = jwt_service

    async def execute(self, email: str, password: str) -> tuple:
        """
        Login a user.

        Returns: (UserEntity, tokens_dict)
        """
        email = email.strip().lower()

        try:
            user_entity = await self.repository.get_by_email(email)
        except EntityNotFoundError:
            raise AuthenticationError("Invalid email or password.")

        if not await self.repository.check_password(user_entity.id, password):
            raise AuthenticationError("Invalid email or password.")

        if not user_entity.is_active:
            raise AuthenticationError("Your account has been deactivated.")

        # Update last_login
        await self.repository.update(user_entity.id, last_login=datetime.now(timezone.utc))

        # Generate tokens
        tokens = self.jwt_service.generate_tokens(user_entity.id)

        return user_entity, tokens
