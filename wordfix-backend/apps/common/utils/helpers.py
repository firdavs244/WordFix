"""
Common utility functions for WordFix project.
"""

from typing import Any


def build_success_response(
    data: Any = None,
    message: str = "Success",
    meta: dict | None = None,
) -> dict:
    """
    Build a standardized success response dictionary.

    Args:
        data: The response data payload.
        message: Human-readable success message.
        meta: Optional metadata (pagination, etc.).

    Returns:
        Formatted response dictionary.
    """
    return {
        "success": True,
        "data": data,
        "message": message,
        "errors": None,
        "meta": meta,
    }


def build_error_response(
    message: str = "An error occurred.",
    errors: dict | None = None,
) -> dict:
    """
    Build a standardized error response dictionary.

    Args:
        message: Human-readable error message.
        errors: Optional error details dictionary.

    Returns:
        Formatted error response dictionary.
    """
    return {
        "success": False,
        "data": None,
        "message": message,
        "errors": errors,
        "meta": None,
    }


def get_client_ip(request) -> str:
    """
    Extract the client IP address from a Django request.

    Handles X-Forwarded-For header for proxied requests.

    Args:
        request: Django HTTP request object.

    Returns:
        Client IP address string.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")
