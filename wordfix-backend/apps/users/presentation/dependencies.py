"""
User dependency injection — factory functions for use cases.
"""

from uuid import UUID

from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.application.use_cases import (
    ChangePasswordUseCase,
    GetUserProfileUseCase,
    LoginUserUseCase,
    RegisterUserUseCase,
    UpdateUserProfileUseCase,
)
from apps.users.infrastructure.models import CustomUser
from apps.users.infrastructure.repositories import DjangoUserRepository


def generate_tokens(user_id: UUID) -> dict:
    """Generate JWT tokens for a user. Infrastructure concern."""
    user = CustomUser.objects.get(id=user_id)
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def get_user_repository() -> DjangoUserRepository:
    return DjangoUserRepository()


def get_register_use_case() -> RegisterUserUseCase:
    return RegisterUserUseCase(get_user_repository(), token_generator=generate_tokens)


def get_login_use_case() -> LoginUserUseCase:
    return LoginUserUseCase(get_user_repository(), token_generator=generate_tokens)


def get_profile_use_case() -> GetUserProfileUseCase:
    return GetUserProfileUseCase(get_user_repository())


def get_update_profile_use_case() -> UpdateUserProfileUseCase:
    return UpdateUserProfileUseCase(get_user_repository())


def get_change_password_use_case() -> ChangePasswordUseCase:
    return ChangePasswordUseCase(get_user_repository())
