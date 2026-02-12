"""
User repository implementation using Django ORM.
"""

from uuid import UUID

from apps.common.exceptions import EntityNotFoundError
from apps.users.domain.entities import UserEntity
from apps.users.domain.repositories import AbstractUserRepository
from apps.users.infrastructure.models import CustomUser


class DjangoUserRepository(AbstractUserRepository):
    """Concrete implementation of AbstractUserRepository using Django ORM."""

    def _to_entity(self, user: CustomUser) -> UserEntity:
        """Convert Django model instance to domain entity."""
        return UserEntity(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            avatar=str(user.avatar) if user.avatar else "",
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

    def get_by_id(self, user_id: UUID) -> UserEntity:
        try:
            user = CustomUser.objects.get(id=user_id)
            return self._to_entity(user)
        except CustomUser.DoesNotExist:
            raise EntityNotFoundError("User not found.")

    def get_by_email(self, email: str) -> UserEntity:
        try:
            user = CustomUser.objects.get(email=email.lower())
            return self._to_entity(user)
        except CustomUser.DoesNotExist:
            raise EntityNotFoundError("User not found.")

    def create(self, email: str, username: str, password: str, **kwargs) -> UserEntity:
        user = CustomUser.objects.create_user(
            email=email,
            username=username,
            password=password,
            **kwargs,
        )
        return self._to_entity(user)

    def update(self, user_id: UUID, **kwargs) -> UserEntity:
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise EntityNotFoundError("User not found.")

        for field, value in kwargs.items():
            setattr(user, field, value)
        user.save()
        return self._to_entity(user)

    def exists_by_email(self, email: str) -> bool:
        return CustomUser.objects.filter(email=email.lower()).exists()

    def exists_by_username(self, username: str) -> bool:
        return CustomUser.objects.filter(username=username).exists()

    def set_password(self, user_id: UUID, password: str) -> None:
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise EntityNotFoundError("User not found.")
        user.set_password(password)
        user.save(update_fields=["password"])

    def check_password(self, user_id: UUID, password: str) -> bool:
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise EntityNotFoundError("User not found.")
        return user.check_password(password)

    def get_user_language_info(self, user_id: UUID) -> dict:
        try:
            user = CustomUser.objects.get(id=user_id)
            return {
                "native_language": user.native_language,
                "proficiency_level": user.proficiency_level,
                "daily_goal": user.daily_goal,
            }
        except CustomUser.DoesNotExist:
            return {
                "native_language": "uz",
                "proficiency_level": "B1",
                "daily_goal": 10,
            }
