"""
Tests for custom exception classes.
"""

from apps.common.exceptions import (
    AIProviderError,
    AuthenticationError,
    EntityAlreadyExistsError,
    EntityNotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ValidationError,
    WordFixBaseException,
)


class TestWordFixBaseException:
    def test_default_message(self):
        exc = WordFixBaseException()
        assert str(exc) == "An unexpected error occurred."
        assert exc.status_code == 500

    def test_custom_message(self):
        exc = WordFixBaseException(message="Custom error")
        assert str(exc) == "Custom error"

    def test_with_errors_dict(self):
        exc = WordFixBaseException(errors={"field": "invalid"})
        assert exc.errors == {"field": "invalid"}

    def test_without_errors(self):
        exc = WordFixBaseException()
        assert exc.errors is None


class TestEntityNotFoundError:
    def test_default(self):
        exc = EntityNotFoundError()
        assert exc.status_code == 404
        assert "not found" in str(exc).lower()

    def test_custom_message(self):
        exc = EntityNotFoundError("User not found.")
        assert str(exc) == "User not found."


class TestEntityAlreadyExistsError:
    def test_default(self):
        exc = EntityAlreadyExistsError()
        assert exc.status_code == 409

    def test_custom_message(self):
        exc = EntityAlreadyExistsError("Duplicate email.")
        assert str(exc) == "Duplicate email."


class TestValidationError:
    def test_default(self):
        exc = ValidationError()
        assert exc.status_code == 400

    def test_with_errors(self):
        exc = ValidationError(errors={"email": "Required"})
        assert exc.errors == {"email": "Required"}


class TestAuthenticationError:
    def test_default(self):
        exc = AuthenticationError()
        assert exc.status_code == 401


class TestPermissionDeniedError:
    def test_default(self):
        exc = PermissionDeniedError()
        assert exc.status_code == 403


class TestAIProviderError:
    def test_default(self):
        exc = AIProviderError()
        assert exc.status_code == 503


class TestRateLimitError:
    def test_default(self):
        exc = RateLimitError()
        assert exc.status_code == 429
