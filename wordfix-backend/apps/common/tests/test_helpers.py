"""
Tests for helper utility functions.
"""

from django.test import RequestFactory

from apps.common.utils.helpers import build_error_response, build_success_response, get_client_ip


class TestBuildSuccessResponse:
    def test_default(self):
        result = build_success_response()
        assert result["success"] is True
        assert result["message"] == "Success"
        assert result["data"] is None
        assert result["errors"] is None
        assert result["meta"] is None

    def test_with_data(self):
        result = build_success_response(data={"id": 1})
        assert result["data"] == {"id": 1}

    def test_with_message(self):
        result = build_success_response(message="Created")
        assert result["message"] == "Created"

    def test_with_meta(self):
        result = build_success_response(meta={"page": 1})
        assert result["meta"] == {"page": 1}


class TestBuildErrorResponse:
    def test_default(self):
        result = build_error_response()
        assert result["success"] is False
        assert result["data"] is None

    def test_with_message(self):
        result = build_error_response(message="Not found")
        assert result["message"] == "Not found"

    def test_with_errors(self):
        result = build_error_response(errors={"field": "bad"})
        assert result["errors"] == {"field": "bad"}


class TestGetClientIP:
    def test_forwarded_for(self):
        factory = RequestFactory()
        request = factory.get("/", HTTP_X_FORWARDED_FOR="1.2.3.4, 5.6.7.8")
        assert get_client_ip(request) == "1.2.3.4"

    def test_remote_addr(self):
        factory = RequestFactory()
        request = factory.get("/")
        ip = get_client_ip(request)
        assert ip  # Should return something
