"""
Tests for UserEntity domain entity.
"""

from datetime import timedelta

import pytest
from django.utils import timezone

from apps.users.domain.entities import UserEntity


class TestUserEntity:
    def test_default_values(self):
        user = UserEntity()
        assert user.email == ""
        assert user.username == ""
        assert user.native_language == "uz"
        assert user.learning_language == "en"
        assert user.proficiency_level == "A1"
        assert user.daily_goal == 10
        assert user.timezone == "Asia/Tashkent"
        assert user.is_premium is False
        assert user.is_active is True

    def test_validate_email_valid(self):
        user = UserEntity(email="test@example.com")
        user.validate_email()

    def test_validate_email_invalid(self):
        user = UserEntity(email="bad-email")
        with pytest.raises(ValueError, match="Invalid email"):
            user.validate_email()

    def test_validate_email_empty(self):
        user = UserEntity(email="")
        with pytest.raises(ValueError):
            user.validate_email()

    def test_validate_username_valid(self):
        user = UserEntity(username="john_doe")
        user.validate_username()

    def test_validate_username_empty(self):
        user = UserEntity(username="")
        with pytest.raises(ValueError, match="required"):
            user.validate_username()

    def test_validate_username_too_short(self):
        user = UserEntity(username="ab")
        with pytest.raises(ValueError, match="at least 3"):
            user.validate_username()

    def test_validate_username_too_long(self):
        user = UserEntity(username="a" * 31)
        with pytest.raises(ValueError, match="at most 30"):
            user.validate_username()

    def test_validate_username_invalid_chars(self):
        user = UserEntity(username="user@name")
        with pytest.raises(ValueError, match="letters, numbers, and underscores"):
            user.validate_username()

    def test_is_premium_active_not_premium(self):
        user = UserEntity(is_premium=False)
        assert user.is_premium_active is False

    def test_is_premium_active_no_expiry(self):
        user = UserEntity(is_premium=True, premium_until=None)
        assert user.is_premium_active is True

    def test_is_premium_active_future(self):
        user = UserEntity(
            is_premium=True,
            premium_until=timezone.now() + timedelta(days=30),
        )
        assert user.is_premium_active is True

    def test_is_premium_active_expired(self):
        user = UserEntity(
            is_premium=True,
            premium_until=timezone.now() - timedelta(days=1),
        )
        assert user.is_premium_active is False

    def test_full_name(self):
        user = UserEntity(full_name="Test User")
        assert user.full_name == "Test User"
