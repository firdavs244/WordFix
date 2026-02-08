"""
Tests for User serializers.
"""

import pytest
from rest_framework.test import APIRequestFactory

from apps.users.presentation.serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserProfileSerializer,
)


class TestRegisterSerializer:
    def test_valid_data(self):
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass1",
            "password_confirm": "testpass1",
        }
        s = RegisterSerializer(data=data)
        assert s.is_valid(), s.errors

    def test_missing_email(self):
        data = {
            "username": "test",
            "password": "testpass1",
            "password_confirm": "testpass1",
        }
        s = RegisterSerializer(data=data)
        assert not s.is_valid()
        assert "email" in s.errors

    def test_missing_username(self):
        data = {
            "email": "t@t.com",
            "password": "testpass1",
            "password_confirm": "testpass1",
        }
        s = RegisterSerializer(data=data)
        assert not s.is_valid()
        assert "username" in s.errors

    def test_password_mismatch(self):
        data = {
            "email": "t@t.com",
            "username": "test",
            "password": "testpass1",
            "password_confirm": "different1",
        }
        s = RegisterSerializer(data=data)
        assert not s.is_valid()

    def test_password_too_short(self):
        data = {
            "email": "t@t.com",
            "username": "test",
            "password": "short1",
            "password_confirm": "short1",
        }
        s = RegisterSerializer(data=data)
        assert not s.is_valid()

    def test_password_no_digit(self):
        data = {
            "email": "t@t.com",
            "username": "test",
            "password": "nodigits",
            "password_confirm": "nodigits",
        }
        s = RegisterSerializer(data=data)
        assert not s.is_valid()

    def test_username_too_short(self):
        data = {
            "email": "t@t.com",
            "username": "ab",
            "password": "testpass1",
            "password_confirm": "testpass1",
        }
        s = RegisterSerializer(data=data)
        assert not s.is_valid()

    def test_username_too_long(self):
        data = {
            "email": "t@t.com",
            "username": "a" * 31,
            "password": "testpass1",
            "password_confirm": "testpass1",
        }
        s = RegisterSerializer(data=data)
        assert not s.is_valid()

    def test_optional_full_name(self):
        data = {
            "email": "t@t.com",
            "username": "test",
            "password": "testpass1",
            "password_confirm": "testpass1",
            "full_name": "Full Name",
        }
        s = RegisterSerializer(data=data)
        assert s.is_valid()
        assert s.validated_data.get("full_name") == "Full Name"


class TestLoginSerializer:
    def test_valid(self):
        s = LoginSerializer(data={"email": "t@t.com", "password": "pass1"})
        assert s.is_valid()

    def test_missing_email(self):
        s = LoginSerializer(data={"password": "pass1"})
        assert not s.is_valid()

    def test_missing_password(self):
        s = LoginSerializer(data={"email": "t@t.com"})
        assert not s.is_valid()


class TestUserProfileSerializer:
    def test_valid_partial(self):
        s = UserProfileSerializer(data={"full_name": "New"}, partial=True)
        assert s.is_valid()

    def test_proficiency_level(self):
        s = UserProfileSerializer(data={"proficiency_level": "B2"}, partial=True)
        assert s.is_valid()

    def test_daily_goal(self):
        s = UserProfileSerializer(data={"daily_goal": 15}, partial=True)
        assert s.is_valid()


class TestChangePasswordSerializer:
    def test_valid(self):
        data = {
            "old_password": "oldpass123",
            "new_password": "newpass456",
            "new_password_confirm": "newpass456",
        }
        s = ChangePasswordSerializer(data=data)
        assert s.is_valid(), s.errors

    def test_mismatch(self):
        data = {
            "old_password": "oldpass123",
            "new_password": "newpass456",
            "new_password_confirm": "different1",
        }
        s = ChangePasswordSerializer(data=data)
        assert not s.is_valid()

    def test_new_password_too_short(self):
        data = {
            "old_password": "oldpass123",
            "new_password": "short1",
            "new_password_confirm": "short1",
        }
        s = ChangePasswordSerializer(data=data)
        assert not s.is_valid()

    def test_new_password_no_digit(self):
        data = {
            "old_password": "oldpass123",
            "new_password": "nodigits",
            "new_password_confirm": "nodigits",
        }
        s = ChangePasswordSerializer(data=data)
        assert not s.is_valid()
