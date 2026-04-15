"""
Profile use cases — Get, Update, ChangePassword.

Port of monolith's profile_use_cases.py with async support.
"""

from uuid import UUID

from wordfix_shared.exceptions import ValidationError

from ...domain.repositories import AbstractUserRepository


class GetUserProfileUseCase:
    """Get user profile by ID."""

    def __init__(self, repository: AbstractUserRepository):
        self.repository = repository

    async def execute(self, user_id: UUID):
        return await self.repository.get_by_id(user_id)


class UpdateUserProfileUseCase:
    """Update user profile (allowed fields only)."""

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

    async def execute(self, user_id: UUID, data: dict):
        filtered = {k: v for k, v in data.items() if k in self.ALLOWED_FIELDS}
        if not filtered:
            return await self.repository.get_by_id(user_id)
        return await self.repository.update(user_id, **filtered)


class ChangePasswordUseCase:
    """Change user password."""

    def __init__(self, repository: AbstractUserRepository):
        self.repository = repository

    async def execute(self, user_id: UUID, old_password: str, new_password: str) -> bool:
        if not await self.repository.check_password(user_id, old_password):
            raise ValidationError("Current password is incorrect.")
        await self.repository.set_password(user_id, new_password)
        return True
