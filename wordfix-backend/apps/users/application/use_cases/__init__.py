"""
User application use cases package.

Re-exports all use case classes for backward compatibility.
Import from here: ``from apps.users.application.use_cases import RegisterUserUseCase``
"""

from .auth_use_cases import (  # noqa: F401
    GoogleLoginUseCase,
    LoginUserUseCase,
    RegisterUserUseCase,
)
from .profile_use_cases import (  # noqa: F401
    ChangePasswordUseCase,
    GetOnboardingQuestionsUseCase,
    GetUserProfileUseCase,
    SkipOnboardingUseCase,
    SubmitOnboardingResultUseCase,
    UpdateUserProfileUseCase,
)

__all__ = [
    "RegisterUserUseCase",
    "LoginUserUseCase",
    "GoogleLoginUseCase",
    "GetUserProfileUseCase",
    "UpdateUserProfileUseCase",
    "ChangePasswordUseCase",
    "GetOnboardingQuestionsUseCase",
    "SubmitOnboardingResultUseCase",
    "SkipOnboardingUseCase",
]
