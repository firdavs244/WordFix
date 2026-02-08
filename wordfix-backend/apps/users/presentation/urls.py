"""
User presentation layer - URL routing.
"""

from django.urls import path

from .views import (
    HealthCheckView,
    RegisterView,
    LoginView,
    LogoutView,
    TokenRefreshView,
    ProfileView,
    ChangePasswordView,
)
from .progress_views import (
    UserProgressView,
    XPHistoryView,
    UserBadgesView,
    AllBadgesView,
)

app_name = "users"

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/profile/", ProfileView.as_view(), name="profile"),
    path("auth/change-password/", ChangePasswordView.as_view(), name="change-password"),
    # XP & Progress
    path("users/progress/", UserProgressView.as_view(), name="user-progress"),
    path("users/xp-history/", XPHistoryView.as_view(), name="xp-history"),
    # Badges
    path("users/badges/", UserBadgesView.as_view(), name="user-badges"),
    path("badges/", AllBadgesView.as_view(), name="all-badges"),
]
