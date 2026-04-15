"""
SQLAlchemy implementation of the User repository.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from wordfix_shared.exceptions import EntityAlreadyExistsError, EntityNotFoundError

from ..domain.entities import UserEntity
from ..domain.repositories import AbstractUserRepository
from .models import User
from .password import check_password, make_password


class SQLAlchemyUserRepository(AbstractUserRepository):
    """User repository backed by SQLAlchemy async sessions."""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, user: User) -> UserEntity:
        """Convert SQLAlchemy model to domain entity."""
        return UserEntity(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name or "",
            avatar=user.avatar or "",
            native_language=user.native_language,
            learning_language=user.learning_language,
            proficiency_level=user.proficiency_level,
            daily_goal=user.daily_goal,
            timezone=user.timezone,
            is_premium=user.is_premium,
            premium_until=user.premium_until,
            is_active=user.is_active,
            is_staff=user.is_staff,
            has_completed_onboarding=user.has_completed_onboarding,
            date_joined=user.date_joined,
            last_login=user.last_login,
        )

    async def _get_user(self, user_id: UUID) -> User:
        """Get raw User model by ID."""
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise EntityNotFoundError("User not found.")
        return user

    async def get_by_id(self, user_id: UUID) -> UserEntity:
        user = await self._get_user(user_id)
        return self._to_entity(user)

    async def get_by_email(self, email: str) -> UserEntity:
        result = await self.session.execute(
            select(User).where(User.email == email.strip().lower())
        )
        user = result.scalar_one_or_none()
        if not user:
            raise EntityNotFoundError("User not found.")
        return self._to_entity(user)

    async def create(self, email: str, username: str, password: str, **kwargs) -> UserEntity:
        user = User(
            email=email.strip().lower(),
            username=username,
            password=make_password(password),
            full_name=kwargs.get("full_name", ""),
            native_language=kwargs.get("native_language", "uz"),
            learning_language=kwargs.get("learning_language", "en"),
        )
        self.session.add(user)
        await self.session.flush()  # Get the generated ID
        return self._to_entity(user)

    async def update(self, user_id: UUID, **kwargs) -> UserEntity:
        user = await self._get_user(user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        await self.session.flush()
        return self._to_entity(user)

    async def exists_by_email(self, email: str) -> bool:
        result = await self.session.execute(
            select(User.id).where(User.email == email.strip().lower())
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_username(self, username: str) -> bool:
        result = await self.session.execute(
            select(User.id).where(User.username == username)
        )
        return result.scalar_one_or_none() is not None

    async def set_password(self, user_id: UUID, password: str) -> None:
        user = await self._get_user(user_id)
        user.password = make_password(password)
        await self.session.flush()

    async def check_password(self, user_id: UUID, password: str) -> bool:
        user = await self._get_user(user_id)
        return check_password(password, user.password)
