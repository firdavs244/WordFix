"""
Tests for User use cases.
"""

import uuid
from unittest.mock import MagicMock, patch

import pytest
from django.utils import timezone

from apps.common.exceptions import (
    AuthenticationError,
    EntityAlreadyExistsError,
    EntityNotFoundError,
    ValidationError,
)
from apps.users.application.use_cases import (
    ChangePasswordUseCase,
    GetUserProfileUseCase,
    LoginUserUseCase,
    RegisterUserUseCase,
    UpdateUserProfileUseCase,
)
from apps.users.infrastructure.models import CustomUser
from apps.users.infrastructure.repositories import DjangoUserRepository
from apps.users.presentation.dependencies import generate_tokens


# =============================================================================
# REGISTER USE CASE TESTS
# =============================================================================


@pytest.mark.django_db
class TestRegisterUserUseCase:
    @pytest.fixture
    def use_case(self):
        return RegisterUserUseCase(repository=DjangoUserRepository(), token_generator=generate_tokens)

    def test_register_success(self, use_case):
        data = {
            "email": "new@example.com",
            "username": "newuser",
            "password": "testpass123",
        }
        entity, tokens = use_case.execute(data)
        assert entity.email == "new@example.com"
        assert "access" in tokens
        assert "refresh" in tokens

    def test_register_normalizes_email(self, use_case):
        data = {
            "email": "  New@EXAMPLE.com  ",
            "username": "user1",
            "password": "testpass123",
        }
        entity, _ = use_case.execute(data)
        assert entity.email == "new@example.com"

    def test_register_duplicate_email(self, use_case, user):
        data = {
            "email": user.email,
            "username": "otheruser",
            "password": "testpass123",
        }
        with pytest.raises(EntityAlreadyExistsError):
            use_case.execute(data)

    def test_register_duplicate_username(self, use_case, user):
        data = {
            "email": "unique@test.com",
            "username": user.username,
            "password": "testpass123",
        }
        with pytest.raises(EntityAlreadyExistsError):
            use_case.execute(data)

    def test_register_with_full_name(self, use_case):
        data = {
            "email": "a@b.com",
            "username": "abc",
            "password": "pass12345",
            "full_name": "Full Name",
        }
        entity, _ = use_case.execute(data)
        assert entity.full_name == "Full Name"

    def test_register_returns_tokens(self, use_case):
        data = {
            "email": "t@t.com",
            "username": "tok",
            "password": "pass12345",
        }
        _, tokens = use_case.execute(data)
        assert isinstance(tokens["access"], str)
        assert isinstance(tokens["refresh"], str)
        assert len(tokens["access"]) > 10


# =============================================================================
# LOGIN USE CASE TESTS
# =============================================================================


@pytest.mark.django_db
class TestLoginUserUseCase:
    @pytest.fixture
    def use_case(self):
        return LoginUserUseCase(repository=DjangoUserRepository(), token_generator=generate_tokens)

    def test_login_success(self, use_case, user):
        entity, tokens = use_case.execute(email=user.email, password="testpass123")
        assert entity.email == user.email
        assert "access" in tokens

    def test_login_wrong_password(self, use_case, user):
        with pytest.raises(AuthenticationError):
            use_case.execute(email=user.email, password="wrongpass")

    def test_login_nonexistent_email(self, use_case):
        with pytest.raises(AuthenticationError):
            use_case.execute(email="noone@test.com", password="pass123")

    def test_login_inactive_user(self, use_case, user):
        user.is_active = False
        user.save()
        with pytest.raises(AuthenticationError):
            use_case.execute(email=user.email, password="testpass123")

    def test_login_updates_last_login(self, use_case, user):
        entity, _ = use_case.execute(email=user.email, password="testpass123")
        user.refresh_from_db()
        assert user.last_login is not None

    def test_login_returns_tokens(self, use_case, user):
        _, tokens = use_case.execute(email=user.email, password="testpass123")
        assert isinstance(tokens["access"], str)
        assert isinstance(tokens["refresh"], str)


# =============================================================================
# PROFILE USE CASE TESTS
# =============================================================================


@pytest.mark.django_db
class TestGetUserProfileUseCase:
    @pytest.fixture
    def use_case(self):
        return GetUserProfileUseCase(repository=DjangoUserRepository())

    def test_get_profile(self, use_case, user):
        entity = use_case.execute(user.id)
        assert entity.email == user.email

    def test_get_profile_not_found(self, use_case):
        with pytest.raises(EntityNotFoundError):
            use_case.execute(uuid.uuid4())


@pytest.mark.django_db
class TestUpdateUserProfileUseCase:
    @pytest.fixture
    def use_case(self):
        return UpdateUserProfileUseCase(repository=DjangoUserRepository())

    def test_update_full_name(self, use_case, user):
        entity = use_case.execute(user.id, {"full_name": "New Name"})
        assert entity.full_name == "New Name"

    def test_update_timezone(self, use_case, user):
        entity = use_case.execute(user.id, {"timezone": "Europe/London"})
        assert entity.timezone == "Europe/London"

    def test_update_daily_goal(self, use_case, user):
        entity = use_case.execute(user.id, {"daily_goal": 25})
        assert entity.daily_goal == 25

    def test_update_proficiency(self, use_case, user):
        entity = use_case.execute(user.id, {"proficiency_level": "B2"})
        assert entity.proficiency_level == "B2"

    def test_update_ignores_disallowed_fields(self, use_case, user):
        # email and username should not be updatable through profile
        entity = use_case.execute(user.id, {"email": "hacked@t.com", "full_name": "OK"})
        assert entity.email == user.email
        assert entity.full_name == "OK"

    def test_update_not_found(self, use_case):
        with pytest.raises(EntityNotFoundError):
            use_case.execute(uuid.uuid4(), {"full_name": "X"})


# =============================================================================
# CHANGE PASSWORD USE CASE TESTS
# =============================================================================


@pytest.mark.django_db
class TestChangePasswordUseCase:
    @pytest.fixture
    def use_case(self):
        return ChangePasswordUseCase(repository=DjangoUserRepository())

    def test_change_password_success(self, use_case, user):
        use_case.execute(user.id, old_password="testpass123", new_password="newpass456")
        user.refresh_from_db()
        assert user.check_password("newpass456")

    def test_change_password_wrong_old(self, use_case, user):
        with pytest.raises(ValidationError):
            use_case.execute(user.id, old_password="wrong123", new_password="new123456")

    def test_change_password_not_found(self, use_case):
        with pytest.raises(EntityNotFoundError):
            use_case.execute(uuid.uuid4(), old_password="a1234567", new_password="b1234567")
