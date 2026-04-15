"""
Common gRPC interceptors for WordFix microservices.
"""

import logging
import time
import uuid

import grpc

logger = logging.getLogger(__name__)


class LoggingInterceptor(grpc.aio.ServerInterceptor):
    """Server interceptor that logs all gRPC calls."""

    async def intercept_service(self, continuation, handler_call_details):
        method = handler_call_details.method
        start = time.perf_counter()
        request_id = str(uuid.uuid4())[:8]

        logger.info("[%s] gRPC call: %s", request_id, method)

        handler = await continuation(handler_call_details)

        elapsed = (time.perf_counter() - start) * 1000
        logger.info("[%s] gRPC completed: %s (%.1fms)", request_id, method, elapsed)

        return handler
