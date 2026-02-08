"""
Tests for custom exception handler.
"""

from unittest.mock import MagicMock

from django.test import override_settings
from rest_framework.test import APIRequestFactory

from apps.common.exception_handler import custom_exception_handler
from apps.common.exceptions import (
    AuthenticationError,
    EntityAlreadyExistsError,
    EntityNotFoundError,
    ValidationError,
)


class TestCustomExceptionHandler:
    """Tests for custom_exception_handler."""

    def _get_context(self):
        factory = APIRequestFactory()
        request = factory.get("/")
        view = MagicMock()
        view.__class__.__name__ = "TestView"
        return {"request": request, "view": view}

    def test_handles_entity_not_found(self):
        exc = EntityNotFoundError("Not found")
        response = custom_exception_handler(exc, self._get_context())
        assert response.status_code == 404
        assert response.data["success"] is False
        assert response.data["message"] == "Not found"

    def test_handles_entity_already_exists(self):
        exc = EntityAlreadyExistsError("Duplicate")
        response = custom_exception_handler(exc, self._get_context())
        assert response.status_code == 409

    def test_handles_validation_error(self):
        exc = ValidationError("Bad data", errors={"name": "required"})
        response = custom_exception_handler(exc, self._get_context())
        assert response.status_code == 400
        assert response.data["errors"] == {"name": "required"}

    def test_handles_authentication_error(self):
        exc = AuthenticationError("Invalid credentials")
        response = custom_exception_handler(exc, self._get_context())
        assert response.status_code == 401

    def test_handles_drf_exception(self):
        from rest_framework.exceptions import NotFound

        exc = NotFound("DRF not found")
        response = custom_exception_handler(exc, self._get_context())
        assert response.status_code == 404
        assert response.data["success"] is False

    def test_handles_drf_validation_error(self):
        from rest_framework.exceptions import ValidationError as DRFValidation

        exc = DRFValidation({"field": ["This field is required."]})
        response = custom_exception_handler(exc, self._get_context())
        assert response.status_code == 400
        assert response.data["errors"] is not None

    @override_settings(DEBUG=True)
    def test_unhandled_exception_debug(self):
        exc = RuntimeError("Something broke")
        response = custom_exception_handler(exc, self._get_context())
        assert response.status_code == 500
        assert "RuntimeError" in response.data["message"]

    @override_settings(DEBUG=False)
    def test_unhandled_exception_production(self):
        exc = RuntimeError("Something broke")
        response = custom_exception_handler(exc, self._get_context())
        assert response.status_code == 500
        assert "unexpected" in response.data["message"].lower()

    def test_response_format(self):
        exc = EntityNotFoundError()
        response = custom_exception_handler(exc, self._get_context())
        assert "success" in response.data
        assert "data" in response.data
        assert "message" in response.data
        assert "errors" in response.data
        assert "meta" in response.data
