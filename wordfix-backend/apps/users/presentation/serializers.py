"""
User serializers — using Serializer (not ModelSerializer).
"""

import re

from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    """Registration serializer with validation."""

    email = serializers.EmailField()
    username = serializers.CharField(min_length=3, max_length=30)
    full_name = serializers.CharField(required=False, default="", allow_blank=True)
    password = serializers.CharField(min_length=8, write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    native_language = serializers.CharField(required=False, default="uz")
    learning_language = serializers.CharField(required=False, default="en")

    def validate_email(self, value: str) -> str:
        return value.strip().lower()

    def validate_username(self, value: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise serializers.ValidationError(
                "Username can only contain letters, numbers, and underscores."
            )
        return value

    def validate_password(self, value: str) -> str:
        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "Password must contain at least one digit."
            )
        return value

    def validate(self, data: dict) -> dict:
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )
        return data


class LoginSerializer(serializers.Serializer):
    """Login serializer."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.Serializer):
    """User profile serializer for GET and PATCH."""

    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(read_only=True)
    full_name = serializers.CharField(required=False, allow_blank=True)
    avatar = serializers.CharField(read_only=True, default="")
    native_language = serializers.CharField(required=False)
    learning_language = serializers.CharField(required=False)
    proficiency_level = serializers.CharField(required=False)
    daily_goal = serializers.IntegerField(required=False, min_value=1, max_value=100)
    timezone = serializers.CharField(required=False)
    is_premium = serializers.BooleanField(read_only=True)
    is_premium_active = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    """Change password serializer."""

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(min_length=8, write_only=True)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate_new_password(self, value: str) -> str:
        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "Password must contain at least one digit."
            )
        return value

    def validate(self, data: dict) -> dict:
        if data["new_password"] != data["new_password_confirm"]:
            raise serializers.ValidationError(
                {"new_password_confirm": "Passwords do not match."}
            )
        return data
