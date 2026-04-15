"""
Custom exception classes for WordFix microservices.

Domain-driven exceptions that are independent of any framework.
Pure Python - safe to import from any layer.
"""


class WordFixBaseException(Exception):
    """Base exception for all WordFix custom exceptions."""

    status_code = 500
    default_message = "An unexpected error occurred."

    def __init__(self, message: str | None = None, errors: dict | None = None):
        self.detail = message or self.default_message
        self.errors = errors
        super().__init__(self.detail)


class EntityNotFoundError(WordFixBaseException):
    """Raised when a requested entity does not exist (404)."""

    status_code = 404
    default_message = "Resource not found."


class EntityAlreadyExistsError(WordFixBaseException):
    """Raised when trying to create a duplicate entity (409)."""

    status_code = 409
    default_message = "Resource already exists."


class ValidationError(WordFixBaseException):
    """Raised for domain-level validation errors (400)."""

    status_code = 400
    default_message = "Validation error."


class AuthenticationError(WordFixBaseException):
    """Raised for authentication failures (401)."""

    status_code = 401
    default_message = "Authentication failed."


class PermissionDeniedError(WordFixBaseException):
    """Raised when user lacks permission (403)."""

    status_code = 403
    default_message = "You do not have permission to perform this action."


class AIProviderError(WordFixBaseException):
    """Raised when AI service is unavailable (503)."""

    status_code = 503
    default_message = "AI service is temporarily unavailable."


class RateLimitError(WordFixBaseException):
    """Raised when rate limit is exceeded (429)."""

    status_code = 429
    default_message = "Too many requests. Please try again later."
