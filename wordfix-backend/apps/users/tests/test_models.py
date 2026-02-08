"""
Tests for CustomUser model and DjangoUserRepository.
"""

import uuid

import pytest
from django.utils import timezone

from apps.common.exceptions import EntityNotFoundError
from apps.users.infrastructure.models import CustomUser
from apps.users.infrastructure.repositories import DjangoUserRepository


# =============================================================================
# CUSTOM USER MODEL TESTS
# =============================================================================


@pytest.mark.django_db
class TestCustomUserModel:
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123",
        )
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.check_password("testpass123")
        assert user.is_active is True
        assert user.is_staff is False

    def test_create_user_normalizes_email(self):
        user = CustomUser.objects.create_user(
            email="  TEST@Example.COM  ",
            username="testuser",
            password="testpass123",
        )
        assert user.email == "test@example.com"

    def test_create_user_without_email_raises(self):
        with pytest.raises(ValueError, match="Email is required"):
            CustomUser.objects.create_user(email="", username="user", password="pass123")

    def test_create_user_without_username_raises(self):
        with pytest.raises(ValueError, match="Username is required"):
            CustomUser.objects.create_user(email="t@t.com", username="", password="pass123")

    def test_create_superuser(self):
        user = CustomUser.objects.create_superuser(
            email="admin@test.com",
            username="admin",
            password="adminpass123",
        )
        assert user.is_staff is True
        assert user.is_superuser is True

    def test_create_superuser_not_staff_raises(self):
        with pytest.raises(ValueError, match="is_staff=True"):
            CustomUser.objects.create_superuser(
                email="admin@test.com",
                username="admin",
                password="pass123",
                is_staff=False,
            )

    def test_create_superuser_not_superuser_raises(self):
        with pytest.raises(ValueError, match="is_superuser=True"):
            CustomUser.objects.create_superuser(
                email="admin@test.com",
                username="admin",
                password="pass123",
                is_superuser=False,
            )

    def test_uuid_primary_key(self, user):
        assert isinstance(user.id, uuid.UUID)

    def test_str(self, user):
        assert str(user) == user.email

    def test_default_values(self, user):
        assert user.native_language == "uz"
        assert user.learning_language == "en"
        assert user.proficiency_level == "A1"
        assert user.daily_goal == 10
        assert user.timezone == "Asia/Tashkent"
        assert user.is_premium is False

    def test_is_premium_active_false(self, user):
        assert user.is_premium_active is False

    def test_is_premium_active_true(self, user):
        user.is_premium = True
        user.premium_until = timezone.now() + timezone.timedelta(days=30)
        assert user.is_premium_active is True

    def test_username_field(self):
        assert CustomUser.USERNAME_FIELD == "email"

    def test_required_fields(self):
        assert "username" in CustomUser.REQUIRED_FIELDS

    def test_unique_email(self, user):
        with pytest.raises(Exception):
            CustomUser.objects.create_user(
                email=user.email,
                username="other",
                password="pass123",
            )

    def test_unique_username(self, user):
        with pytest.raises(Exception):
            CustomUser.objects.create_user(
                email="new@test.com",
                username=user.username,
                password="pass123",
            )

    def test_date_joined_auto_set(self, user):
        assert user.date_joined is not None

    def test_clean_lowercases_email(self):
        user = CustomUser(email="Upper@Test.com", username="test")
        user.clean()
        assert user.email == "upper@test.com"


# =============================================================================
# DJANGO USER REPOSITORY TESTS
# =============================================================================


@pytest.mark.django_db
class TestDjangoUserRepository:
    @pytest.fixture
    def repo(self):
        return DjangoUserRepository()

    def test_create(self, repo):
        entity = repo.create(
            email="new@example.com",
            username="newuser",
            password="newpass123",
        )
        assert entity.email == "new@example.com"
        assert entity.username == "newuser"

    def test_get_by_id(self, repo, user):
        entity = repo.get_by_id(user.id)
        assert entity.email == user.email

    def test_get_by_id_not_found(self, repo):
        with pytest.raises(EntityNotFoundError):
            repo.get_by_id(uuid.uuid4())

    def test_get_by_email(self, repo, user):
        entity = repo.get_by_email(user.email)
        assert entity.username == user.username

    def test_get_by_email_not_found(self, repo):
        with pytest.raises(EntityNotFoundError):
            repo.get_by_email("nonexistent@test.com")

    def test_exists_by_email(self, repo, user):
        assert repo.exists_by_email(user.email) is True
        assert repo.exists_by_email("nope@test.com") is False

    def test_exists_by_username(self, repo, user):
        assert repo.exists_by_username(user.username) is True
        assert repo.exists_by_username("nope") is False

    def test_update(self, repo, user):
        entity = repo.update(user.id, full_name="Updated Name")
        assert entity.full_name == "Updated Name"

    def test_update_not_found(self, repo):
        with pytest.raises(EntityNotFoundError):
            repo.update(uuid.uuid4(), full_name="X")

    def test_set_password(self, repo, user):
        repo.set_password(user.id, "newpassword1")
        user.refresh_from_db()
        assert user.check_password("newpassword1")

    def test_set_password_not_found(self, repo):
        with pytest.raises(EntityNotFoundError):
            repo.set_password(uuid.uuid4(), "pass123")

    def test_check_password_correct(self, repo, user):
        assert repo.check_password(user.id, "testpass123") is True

    def test_check_password_wrong(self, repo, user):
        assert repo.check_password(user.id, "wrongpass") is False

    def test_check_password_not_found(self, repo):
        with pytest.raises(EntityNotFoundError):
            repo.check_password(uuid.uuid4(), "pass123")

    def test_create_returns_entity(self, repo):
        entity = repo.create(email="e@t.com", username="u1", password="p123456789")
        assert entity.id is not None
        assert entity.is_active is True

    def test_entity_conversion(self, repo, user):
        entity = repo.get_by_id(user.id)
        assert entity.native_language == "uz"
        assert entity.learning_language == "en"
        assert entity.proficiency_level == "A1"
