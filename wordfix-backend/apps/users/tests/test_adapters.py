"""
Tests for CustomSocialAccountAdapter.
"""

from unittest.mock import MagicMock, patch
import uuid

import pytest

from apps.users.infrastructure.adapters import CustomSocialAccountAdapter
from apps.users.infrastructure.models import CustomUser, UserProgress


@pytest.fixture
def adapter():
    return CustomSocialAccountAdapter()


@pytest.fixture
def existing_user(db):
    user = CustomUser.objects.create_user(
        email="existing@example.com",
        username="existinguser",
        password="testpass123",
    )
    return user


class TestCustomSocialAccountAdapter:
    """Tests for the custom social account adapter."""

    def test_pre_social_login_links_existing(self, adapter, existing_user):
        """pre_social_login links social account to existing user by email."""
        request = MagicMock()
        sociallogin = MagicMock()
        sociallogin.account.extra_data = {"email": "existing@example.com"}

        adapter.pre_social_login(request, sociallogin)

        sociallogin.connect.assert_called_once_with(request, existing_user)

    def test_pre_social_login_no_existing_user(self, adapter, db):
        """pre_social_login does nothing if no matching user."""
        request = MagicMock()
        sociallogin = MagicMock()
        sociallogin.account.extra_data = {"email": "nonexistent@example.com"}

        adapter.pre_social_login(request, sociallogin)

        sociallogin.connect.assert_not_called()

    def test_pre_social_login_empty_email(self, adapter, db):
        """pre_social_login does nothing if email is empty."""
        request = MagicMock()
        sociallogin = MagicMock()
        sociallogin.account.extra_data = {"email": ""}

        adapter.pre_social_login(request, sociallogin)

        sociallogin.connect.assert_not_called()

    def test_pre_social_login_case_insensitive(self, adapter, existing_user):
        """pre_social_login matches email case-insensitively."""
        request = MagicMock()
        sociallogin = MagicMock()
        sociallogin.account.extra_data = {"email": "EXISTING@EXAMPLE.COM"}

        adapter.pre_social_login(request, sociallogin)

        sociallogin.connect.assert_called_once_with(request, existing_user)

    def test_save_user_creates_progress(self, adapter, db):
        """save_user creates UserProgress for new user."""
        request = MagicMock()
        sociallogin = MagicMock()
        sociallogin.account.extra_data = {"name": "Test User"}

        # Create a real user to return from super().save_user()
        user = CustomUser.objects.create_user(
            email="social@example.com",
            username="socialtemp",
            password="testpass123",
        )
        user.username = ""
        user.save(update_fields=["username"])

        with patch.object(
            CustomSocialAccountAdapter.__bases__[0],
            "save_user",
            return_value=user,
        ):
            result = adapter.save_user(request, sociallogin)

        assert result.full_name == "Test User"
        assert result.username.startswith("user_")
        assert UserProgress.objects.filter(user=result).exists()

    def test_save_user_keeps_existing_username(self, adapter, db):
        """save_user doesn't overwrite existing username."""
        request = MagicMock()
        sociallogin = MagicMock()
        sociallogin.account.extra_data = {"name": "Named User"}

        user = CustomUser.objects.create_user(
            email="named@example.com",
            username="alreadyset",
            password="testpass123",
        )

        with patch.object(
            CustomSocialAccountAdapter.__bases__[0],
            "save_user",
            return_value=user,
        ):
            result = adapter.save_user(request, sociallogin)

        assert result.username == "alreadyset"
