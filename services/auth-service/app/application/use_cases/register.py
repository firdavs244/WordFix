"""
Register user use case.

Port of monolith's RegisterUserUseCase with async support
and event publishing.
"""

from wordfix_shared.exceptions import EntityAlreadyExistsError

from ...domain.repositories import AbstractUserRepository
from ...infrastructure.jwt_service import JWTService


class RegisterUserUseCase:
    """Register a new user."""

    def __init__(self, repository: AbstractUserRepository, jwt_service: JWTService):
        self.repository = repository
        self.jwt_service = jwt_service

    async def execute(self, data: dict) -> tuple:
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
        if await self.repository.exists_by_email(email):
            raise EntityAlreadyExistsError("A user with this email already exists.")

        if await self.repository.exists_by_username(username):
            raise EntityAlreadyExistsError("A user with this username already exists.")

        # Create user
        user_entity = await self.repository.create(
            email=email,
            username=username,
            password=password,
            full_name=full_name,
            native_language=native_language,
            learning_language=learning_language,
        )

        # Generate tokens
        tokens = self.jwt_service.generate_tokens(user_entity.id)

        return user_entity, tokens
