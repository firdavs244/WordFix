"""
FastAPI JWT authentication middleware for WordFix microservices.

Validates Bearer tokens and injects user_id into request state.
"""

import logging

import jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..response import build_error_response
from .jwt_utils import decode_token

logger = logging.getLogger(__name__)

# Routes that don't require authentication
PUBLIC_PATHS = frozenset({
    "/health",
    "/docs",
    "/openapi.json",
    "/redoc",
})


class JWTAuthMiddleware(BaseHTTPMiddleware):
    """Middleware that validates JWT tokens on protected routes."""

    def __init__(self, app, secret_key: str, algorithm: str = "HS256", public_paths: set | None = None):
        super().__init__(app)
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.public_paths = public_paths or PUBLIC_PATHS

    async def dispatch(self, request: Request, call_next):
        # Allow OPTIONS (CORS preflight)
        if request.method == "OPTIONS":
            return await call_next(request)

        # Allow public paths
        path = request.url.path.rstrip("/")
        if self._is_public(path):
            request.state.user_id = None
            request.state.user_email = None
            return await call_next(request)

        # Extract token
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            request.state.user_id = None
            request.state.user_email = None
            return await call_next(request)

        token = auth_header[7:]  # Remove "Bearer "

        try:
            payload = decode_token(token, self.secret_key, self.algorithm)
            if payload.get("token_type") != "access":
                return JSONResponse(
                    status_code=401,
                    content=build_error_response("Invalid token type."),
                )
            request.state.user_id = payload.get("user_id")
            request.state.user_email = payload.get("email")
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=401,
                content=build_error_response("Token has expired."),
            )
        except jwt.InvalidTokenError:
            return JSONResponse(
                status_code=401,
                content=build_error_response("Invalid token."),
            )

        return await call_next(request)

    def _is_public(self, path: str) -> bool:
        """Check if the path is public (no auth required)."""
        for public_path in self.public_paths:
            if path == public_path or path.startswith(public_path + "/"):
                return True
        return False
