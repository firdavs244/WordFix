"""
Tests for RequestIDMiddleware.
"""

from unittest.mock import MagicMock

from django.test import RequestFactory

from apps.common.middleware.request_id import RequestIDMiddleware


class TestRequestIDMiddleware:
    def test_generates_request_id(self):
        factory = RequestFactory()
        request = factory.get("/")
        response = MagicMock()
        response.__setitem__ = MagicMock()

        def get_response(req):
            assert hasattr(req, "id")
            return response

        middleware = RequestIDMiddleware(get_response)
        middleware(request)

    def test_uses_existing_request_id(self):
        factory = RequestFactory()
        request = factory.get("/", HTTP_X_REQUEST_ID="my-custom-id")
        response = MagicMock()
        response.__setitem__ = MagicMock()

        def get_response(req):
            assert req.id == "my-custom-id"
            return response

        middleware = RequestIDMiddleware(get_response)
        middleware(request)

    def test_adds_header_to_response(self):
        factory = RequestFactory()
        request = factory.get("/")
        headers = {}

        class FakeResponse:
            def __setitem__(self, key, value):
                headers[key] = value

        def get_response(req):
            return FakeResponse()

        middleware = RequestIDMiddleware(get_response)
        middleware(request)
        assert "X-Request-ID" in headers
