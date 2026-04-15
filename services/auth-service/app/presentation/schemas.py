"""
Pydantic request/response schemas for the Auth Service API.

Mirrors the monolith's serializers to maintain frontend compatibility.
"""

import re
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator


# ── Request Schemas ──────────────────────────────────────


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str
    password_confirm: str
    full_name: str = ""
    native_language: str = "uz"
    learning_language: str = "en"

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters.")
        if len(v) > 30:
            raise ValueError("Username must be at most 30 characters.")
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username can only contain letters, numbers, and underscores.")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters.")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit.")
        return v

    @field_validator("password_confirm")
    @classmethod
    def validate_password_confirm(cls, v: str, info) -> str:
        password = info.data.get("password")
        if password and v != password:
            raise ValueError("Passwords do not match.")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class GoogleLoginRequest(BaseModel):
    access_token: str = ""
    id_token: str = ""

    @field_validator("id_token")
    @classmethod
    def validate_tokens(cls, v: str, info) -> str:
        access = info.data.get("access_token", "")
        if not access and not v:
            raise ValueError("access_token or id_token is required.")
        return v


class LogoutRequest(BaseModel):
    refresh: str


class TokenRefreshRequest(BaseModel):
    refresh: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    new_password_confirm: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters.")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit.")
        return v

    @field_validator("new_password_confirm")
    @classmethod
    def validate_confirm(cls, v: str, info) -> str:
        pw = info.data.get("new_password")
        if pw and v != pw:
            raise ValueError("Passwords do not match.")
        return v


class ProfileUpdateRequest(BaseModel):
    full_name: str | None = None
    native_language: str | None = None
    learning_language: str | None = None
    proficiency_level: str | None = None
    daily_goal: int | None = None
    timezone: str | None = None


# ── Response Schemas ─────────────────────────────────────


class UserProfileData(BaseModel):
    id: str
    email: str
    username: str
    full_name: str = ""
    avatar: str = ""
    native_language: str = "uz"
    learning_language: str = "en"
    proficiency_level: str = "A1"
    daily_goal: int = 10
    timezone: str = "Asia/Tashkent"
    is_premium: bool = False
    is_premium_active: bool = False
    has_completed_onboarding: bool = False
    date_joined: str | None = None
    last_login: str | None = None
    premium_until: str | None = None
