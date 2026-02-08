"""
Request ID middleware for request tracing.

Adds a unique request ID to each request for logging and debugging purposes.
"""

import uuid
import logging

logger = logging.getLogger(__name__)


class RequestIDMiddleware:
    """
    Middleware that generates or extracts a unique request ID for each request.

    The request ID is:
    - Extracted from X-Request-ID header if present
    - Generated as a new UUID4 if not present
    - Added to the response as X-Request-ID header
    - Stored on the request object as request.id
    """

    HEADER_NAME = "X-Request-ID"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get or generate request ID
        request_id = request.META.get(
            f"HTTP_{self.HEADER_NAME.upper().replace('-', '_')}",
            str(uuid.uuid4()),
        )

        # Store on request object
        request.id = request_id

        # Log the request
        logger.info(
            "Request started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.path,
            },
        )

        response = self.get_response(request)

        # Add request ID to response headers
        response[self.HEADER_NAME] = request_id

        return response
