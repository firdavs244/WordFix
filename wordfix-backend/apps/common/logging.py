"""
Structured Logging for WordFix.

JSONFormatter — formats log records as JSON.
RequestLoggingMiddleware — logs every API request with timing.
"""

import json
import logging
import time
import traceback

from django.utils.deprecation import MiddlewareMixin


class JSONFormatter(logging.Formatter):
    """
    Formats log records as a single-line JSON object.

    Fields: timestamp, level, logger, message, module, function, line.
    Extra fields (if present): user_id, duration_ms, action, service.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Attach extra fields if set on the record
        for key in ("user_id", "duration_ms", "action", "service"):
            value = getattr(record, key, None)
            if value is not None:
                log_data[key] = value

        # Include exception info
        if record.exc_info and record.exc_info[1]:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info),
            }

        return json.dumps(log_data, default=str)


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Logs every HTTP request with method, path, status code, and duration.

    Requests taking > 500 ms are logged at WARNING level as slow requests.
    """

    def process_request(self, request):
        request._log_start_time = time.time()
        return None

    def process_response(self, request, response):
        start = getattr(request, "_log_start_time", None)
        if start is None:
            return response

        duration_ms = (time.time() - start) * 1000

        user_id = None
        if hasattr(request, "user") and request.user and request.user.is_authenticated:
            user_id = str(request.user.pk)

        log_extra = {
            "duration_ms": round(duration_ms, 2),
            "user_id": user_id,
            "action": "http_request",
        }

        logger = logging.getLogger("apps.common.logging")
        method = request.method
        path = request.get_full_path()
        status = response.status_code

        msg = f"{method} {path} → {status} ({duration_ms:.0f}ms)"

        if duration_ms > 500:
            logger.warning(msg, extra=log_extra)
        else:
            logger.info(msg, extra=log_extra)

        return response
