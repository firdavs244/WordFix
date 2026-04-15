"""
Auth routes — proxies auth requests to the Auth Service.

Currently uses HTTP forwarding to the Auth Service's REST API.
When gRPC stubs are generated, this will switch to gRPC calls.
"""

import logging

import httpx
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from ..config import settings

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Auth"])

# Auth Service HTTP base URL (auth-service exposes HTTP on port 8001)
AUTH_SERVICE_URL = f"http://{settings.AUTH_SERVICE_GRPC.split(':')[0]}:8001"

# Long-lived client for auth service
_auth_client: httpx.AsyncClient | None = None


async def get_auth_client() -> httpx.AsyncClient:
    global _auth_client
    if _auth_client is None or _auth_client.is_closed:
        _auth_client = httpx.AsyncClient(
            base_url=AUTH_SERVICE_URL,
            timeout=httpx.Timeout(30.0, connect=5.0),
        )
    return _auth_client


# Auth endpoints that are handled by Auth Service
AUTH_PATHS = {
    "/api/v1/auth/register/",
    "/api/v1/auth/login/",
    "/api/v1/auth/logout/",
    "/api/v1/auth/token/refresh/",
    "/api/v1/auth/profile/",
    "/api/v1/auth/change-password/",
    "/api/v1/auth/google/",
    "/api/v1/auth/providers/",
}


def is_auth_path(path: str) -> bool:
    """Check if a path should be routed to the Auth Service."""
    normalized = path.rstrip("/") + "/"
    return normalized in AUTH_PATHS


@router.api_route(
    "/api/v1/auth/{path:path}",
    methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
)
async def auth_proxy(request: Request, path: str):
    """
    Route auth requests to the Auth Service or monolith.

    Auth Service handles: register, login, logout, token/refresh, profile,
    change-password, google, providers.

    Everything else (onboarding) goes to the monolith.
    """
    full_path = f"/api/v1/auth/{path}"
    if not full_path.endswith("/"):
        full_path += "/"

    if is_auth_path(full_path):
        # Forward to Auth Service
        return await _forward_to_auth_service(request, path)
    else:
        # Forward to monolith (onboarding, etc.)
        return await _forward_to_monolith(request, full_path)


async def _forward_to_auth_service(request: Request, path: str):
    """Forward request to Auth Service HTTP API."""
    client = await get_auth_client()

    # Auth Service routes don't have /api/v1 prefix
    auth_path = f"/auth/{path}"
    if not auth_path.endswith("/"):
        auth_path += "/"

    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ("host", "connection", "transfer-encoding")
    }

    # Forward user_id from JWT middleware if present
    user_id = getattr(request.state, "user_id", None)
    if user_id:
        headers["X-User-ID"] = str(user_id)

    body = await request.body()

    try:
        response = await client.request(
            method=request.method,
            url=auth_path,
            headers=headers,
            content=body,
        )

        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
            headers={
                "X-Routed-To": "auth-service",
                "X-Request-ID": getattr(request.state, "request_id", ""),
            },
        )
    except httpx.ConnectError:
        logger.error("Auth Service unavailable")
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "data": None,
                "message": "Auth service is temporarily unavailable.",
                "errors": None,
                "meta": None,
            },
        )


async def _forward_to_monolith(request: Request, path: str):
    """Forward non-auth requests to monolith."""
    from .monolith import monolith_proxy
    return await monolith_proxy(request)
