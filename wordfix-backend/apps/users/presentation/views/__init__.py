"""
User presentation views package.

Re-exports all view classes for backward compatibility.
Import from here: ``from apps.users.presentation.views import RegisterView``
"""

from .auth_views import (  # noqa: F401
    GoogleAuthStatusView,
    GoogleLoginView,
    LoginView,
    LogoutView,
    RegisterView,
    TokenRefreshView,
)
from .profile_views import (  # noqa: F401
    ChangePasswordView,
    HealthCheckView,
    ProfileView,
)
from .helpers import _user_entity_to_dict  # noqa: F401

__all__ = [
    "RegisterView",
    "LoginView",
    "LogoutView",
    "TokenRefreshView",
    "GoogleLoginView",
    "GoogleAuthStatusView",
    "ProfileView",
    "ChangePasswordView",
    "HealthCheckView",
    "_user_entity_to_dict",
]
