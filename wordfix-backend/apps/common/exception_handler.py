"""
Custom DRF exception handler for consistent JSON error responses.

All API error responses follow this format:
{
    "success": false,
    "data": null,
    "message": "Error description",
    "errors": {...} or null,
    "meta": null
}
"""

import logging
import traceback

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .exceptions import WordFixBaseException

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context) -> Response:
    """
    Custom exception handler that returns consistent JSON error responses.

    Handles:
    - WordFix custom exceptions → proper HTTP status + consistent format
    - DRF built-in exceptions → same format
    - 500 errors: production=generic msg, development=traceback
    """
    # Let DRF handle its own exceptions first
    response = exception_handler(exc, context)

    # Handle WordFix custom exceptions
    if isinstance(exc, WordFixBaseException):
        return Response(
            {
                "success": False,
                "data": None,
                "message": str(exc.detail) if hasattr(exc, "detail") else str(exc),
                "errors": exc.errors if hasattr(exc, "errors") else None,
                "meta": None,
            },
            status=exc.status_code,
        )

    # Handle DRF exceptions
    if response is not None:
        errors = None
        message = "An error occurred."

        if isinstance(response.data, dict):
            if "detail" in response.data:
                message = str(response.data["detail"])
            else:
                errors = response.data
                message = "Validation error."
        elif isinstance(response.data, list):
            message = str(response.data[0]) if response.data else "An error occurred."

        response.data = {
            "success": False,
            "data": None,
            "message": message,
            "errors": errors,
            "meta": None,
        }
        return response

    # Unhandled exception — 500
    logger.error(
        "Unhandled exception: %s",
        str(exc),
        exc_info=True,
        extra={
            "view": context.get("view", None).__class__.__name__
            if context.get("view")
            else "Unknown",
        },
    )

    if settings.DEBUG:
        message = f"{exc.__class__.__name__}: {str(exc)}"
        errors = {"traceback": traceback.format_exc().split("\n")}
    else:
        message = "An unexpected error occurred. Please try again later."
        errors = None

    return Response(
        {
            "success": False,
            "data": None,
            "message": message,
            "errors": errors,
            "meta": None,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
