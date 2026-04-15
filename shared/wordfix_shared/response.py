"""
Standardized response builders for WordFix microservices.

All services must return responses in this format to maintain
frontend compatibility: {success, data, message, errors, meta}
"""

from typing import Any


def build_success_response(
    data: Any = None,
    message: str = "Success",
    meta: dict | None = None,
) -> dict:
    """Build a standardized success response dictionary."""
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
    """Build a standardized error response dictionary."""
    return {
        "success": False,
        "data": None,
        "message": message,
        "errors": errors,
        "meta": None,
    }
