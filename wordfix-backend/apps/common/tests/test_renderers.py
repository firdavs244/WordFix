"""
Tests for CustomJSONRenderer.
"""

import json
from unittest.mock import MagicMock

from apps.common.renderers import CustomJSONRenderer


class TestCustomJSONRenderer:
    def test_wraps_success_data(self):
        renderer = CustomJSONRenderer()
        response = MagicMock()
        response.status_code = 200
        context = {"response": response}
        data = {"key": "value"}
        result = renderer.render(data, renderer_context=context)
        parsed = json.loads(result)
        assert parsed["success"] is True
        assert parsed["data"] == {"key": "value"}

    def test_wraps_error_data(self):
        renderer = CustomJSONRenderer()
        response = MagicMock()
        response.status_code = 400
        context = {"response": response}
        data = {"field": "error"}
        result = renderer.render(data, renderer_context=context)
        parsed = json.loads(result)
        assert parsed["success"] is False

    def test_does_not_double_wrap(self):
        renderer = CustomJSONRenderer()
        response = MagicMock()
        response.status_code = 200
        context = {"response": response}
        data = {"success": True, "data": "already wrapped"}
        result = renderer.render(data, renderer_context=context)
        parsed = json.loads(result)
        assert parsed["data"] == "already wrapped"

    def test_no_context(self):
        renderer = CustomJSONRenderer()
        data = {"key": "val"}
        result = renderer.render(data, renderer_context=None)
        parsed = json.loads(result)
        assert parsed["success"] is True
