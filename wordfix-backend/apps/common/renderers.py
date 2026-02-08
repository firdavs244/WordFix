"""
Custom JSON renderer for consistent API response format.

All API responses follow this structure:
{
    "success": true/false,
    "data": {...} or [...],
    "message": "Success message",
    "errors": null or {...},
    "meta": {
        "page": 1,
        "total_pages": 10,
        "total_count": 200
    }
}
"""

from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    """
    Custom renderer that wraps all responses in a consistent format.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response") if renderer_context else None

        # If data is already in our custom format, don't wrap it again
        if isinstance(data, dict) and "success" in data:
            return super().render(data, accepted_media_type, renderer_context)

        # Determine success based on status code
        status_code = response.status_code if response else 200
        is_success = 200 <= status_code < 300

        # Build the response envelope
        response_data = {
            "success": is_success,
            "data": data if is_success else None,
            "message": "Success" if is_success else "Error",
            "errors": data if not is_success else None,
            "meta": None,
        }

        return super().render(response_data, accepted_media_type, renderer_context)
