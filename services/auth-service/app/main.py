"""
Auth Service — FastAPI application entry point.

Runs both HTTP (FastAPI) and gRPC servers.
"""

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from wordfix_shared.auth.middleware import JWTAuthMiddleware
from wordfix_shared.exceptions import WordFixBaseException
from wordfix_shared.response import build_error_response

from .config import settings
from .grpc.server import start_grpc_server
from .presentation.routes.auth import router as auth_router
from .presentation.routes.google import router as google_router
from .presentation.routes.health import router as health_router
from .presentation.routes.profile import router as profile_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# gRPC server reference for cleanup
_grpc_server = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — start/stop gRPC server."""
    global _grpc_server
    # Start gRPC server
    _grpc_server = await start_grpc_server()
    logger.info("Auth Service started (HTTP=%d, gRPC=%d)", settings.HTTP_PORT, settings.GRPC_PORT)
    yield
    # Shutdown
    if _grpc_server:
        await _grpc_server.stop(grace=5)
    logger.info("Auth Service stopped")


app = FastAPI(
    title="WordFix Auth Service",
    version=settings.VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    lifespan=lifespan,
)

# ── Middleware ────────────────────────────────────────────

# JWT middleware — skips public auth endpoints
AUTH_PUBLIC_PATHS = {
    "/health",
    "/auth/register",
    "/auth/login",
    "/auth/token/refresh",
    "/auth/google",
    "/auth/providers",
    "/docs",
    "/openapi.json",
}

app.add_middleware(
    JWTAuthMiddleware,
    secret_key=settings.JWT_SECRET,
    algorithm=settings.JWT_ALGORITHM,
    public_paths=AUTH_PUBLIC_PATHS,
)

# ── Exception Handler ────────────────────────────────────


@app.exception_handler(WordFixBaseException)
async def wordfix_exception_handler(request: Request, exc: WordFixBaseException):
    """Convert WordFix exceptions to standardized JSON responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content=build_error_response(
            message=exc.detail,
            errors=exc.errors,
        ),
    )


# ── Routes ───────────────────────────────────────────────

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(google_router)
