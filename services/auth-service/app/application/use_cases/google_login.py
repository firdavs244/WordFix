"""
Google OAuth login use case.

Port of monolith's GoogleLoginUseCase with async support.
"""

import uuid
from datetime import datetime, timezone

from wordfix_shared.exceptions import EntityNotFoundError, ValidationError

from ...domain.repositories import AbstractUserRepository
from ...infrastructure.jwt_service import JWTService


class GoogleLoginUseCase:
    """Google OAuth login use case."""

    def __init__(self, repository: AbstractUserRepository, jwt_service: JWTService):
        self.repository = repository
        self.jwt_service = jwt_service

    async def execute(self, google_user_info: dict) -> tuple:
        """
        Process Google login.

        Args:
            google_user_info: Dict with email, name, google_id keys.

        Returns: (UserEntity, tokens_dict, is_new_user)
        """
        email = google_user_info.get("email", "").strip().lower()
        name = google_user_info.get("name", "")

        if not email:
            raise ValidationError("Email is required from Google.")

        is_new_user = False

        try:
            user_entity = await self.repository.get_by_email(email)
        except EntityNotFoundError:
            username = f"user_{uuid.uuid4().hex[:8]}"
            user_entity = await self.repository.create(
                email=email,
                username=username,
                password=uuid.uuid4().hex,
                full_name=name,
            )
            is_new_user = True

        # Update last_login
        await self.repository.update(user_entity.id, last_login=datetime.now(timezone.utc))

        # Generate tokens
        tokens = self.jwt_service.generate_tokens(user_entity.id)

        return user_entity, tokens, is_new_user
