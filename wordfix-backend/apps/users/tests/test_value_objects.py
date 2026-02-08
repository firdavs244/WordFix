"""
Tests for User value objects — Email, Password.
"""

import pytest

from apps.users.domain.value_objects import Email, Password


class TestEmailValueObject:
    def test_valid_email(self):
        email = Email(value="test@example.com")
        assert email.value == "test@example.com"

    def test_empty_email_raises(self):
        with pytest.raises(ValueError, match="required"):
            Email(value="")

    def test_invalid_format_raises(self):
        with pytest.raises(ValueError, match="Invalid email"):
            Email(value="not-an-email")

    def test_no_domain_raises(self):
        with pytest.raises(ValueError):
            Email(value="user@")

    def test_normalized(self):
        email = Email(value="USER@Example.COM")
        assert email.normalized == "user@example.com"

    def test_domain_property(self):
        email = Email(value="user@example.com")
        assert email.domain == "example.com"

    def test_str(self):
        email = Email(value="User@Test.com")
        assert str(email) == "user@test.com"

    def test_equality(self):
        e1 = Email(value="user@test.com")
        e2 = Email(value="USER@test.com")
        assert e1 == e2

    def test_inequality(self):
        e1 = Email(value="a@test.com")
        e2 = Email(value="b@test.com")
        assert e1 != e2

    def test_hash(self):
        e1 = Email(value="user@test.com")
        e2 = Email(value="USER@test.com")
        assert hash(e1) == hash(e2)

    def test_frozen(self):
        email = Email(value="test@example.com")
        with pytest.raises(AttributeError):
            email.value = "other@example.com"

    def test_not_equal_to_string(self):
        email = Email(value="test@example.com")
        assert email.__eq__("test@example.com") is NotImplemented


class TestPasswordValueObject:
    def test_valid_password(self):
        pwd = Password(value="securepass1")
        assert pwd.value == "securepass1"

    def test_empty_password_raises(self):
        with pytest.raises(ValueError, match="required"):
            Password(value="")

    def test_too_short_raises(self):
        with pytest.raises(ValueError, match="at least 8"):
            Password(value="short1")

    def test_no_digit_raises(self):
        with pytest.raises(ValueError, match="digit"):
            Password(value="nodigitshere")

    def test_str_masks_value(self):
        pwd = Password(value="securepass1")
        assert str(pwd) == "********"

    def test_min_length_boundary(self):
        pwd = Password(value="12345678")
        assert pwd.value == "12345678"

    def test_frozen(self):
        pwd = Password(value="securepass1")
        with pytest.raises(AttributeError):
            pwd.value = "other123"
