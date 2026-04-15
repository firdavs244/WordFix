"""
Monolith proxy — catch-all route that forwards to Django.

All non-auth API requests are transparently proxied to the monolith.
"""

import logging

from fastapi import APIRouter, Request
from fastapi.responses import Response

from ..services.proxy import proxy_request

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Monolith Proxy"])


@router.api_route(
    "/api/v1/{path:path}",
    methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
)
async def monolith_proxy(request: Request):
    """
    Catch-all route — proxy everything to the Django monolith.

    This handles all non-auth endpoints:
    - /api/v1/words/*
    - /api/v1/review/*
    - /api/v1/tests/*
    - /api/v1/games/*
    - /api/v1/chat/*
    - /api/v1/analytics/*
    - /api/v1/challenges/*
    - /api/v1/notifications/*
    - /api/v1/users/*
    - /api/v1/badges/*
    - /api/v1/learning-profile/*
    - /api/v1/system/*
    """
    path = request.url.path
    query_string = request.url.query or ""

    headers = dict(request.headers)

    # Inject user info from JWT middleware
    user_id = getattr(request.state, "user_id", None)
    if user_id:
        headers["X-User-ID"] = str(user_id)

    user_email = getattr(request.state, "user_email", None)
    if user_email:
        headers["X-User-Email"] = str(user_email)

    request_id = getattr(request.state, "request_id", "")
    if request_id:
        headers["X-Request-ID"] = request_id

    body = await request.body()

    try:
        response = await proxy_request(
            method=request.method,
            path=path,
            headers=headers,
            body=body if body else None,
            query_string=query_string,
        )

        # Build response headers (filter out hop-by-hop)
        resp_headers = {
            k: v for k, v in response.headers.items()
            if k.lower() not in ("transfer-encoding", "connection", "content-encoding", "content-length")
        }
        resp_headers["X-Routed-To"] = "monolith"
        if request_id:
            resp_headers["X-Request-ID"] = request_id

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=resp_headers,
            media_type=response.headers.get("content-type", "application/json"),
        )
    except Exception:
        logger.exception("Monolith proxy error")
        return Response(
            content=b'{"success":false,"data":null,"message":"Service temporarily unavailable.","errors":null,"meta":null}',
            status_code=503,
            media_type="application/json",
        )
