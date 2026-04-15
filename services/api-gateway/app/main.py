"""
API Gateway — FastAPI application entry point.

Routes:
  /api/v1/auth/*  → Auth Service (register, login, etc.)
  /api/v1/*       → Django monolith (everything else)
  /api/v1/health/ → Aggregated health check
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from wordfix_shared.auth.middleware import JWTAuthMiddleware

from .config import settings
from .middleware.request_id import RequestIDMiddleware
from .routes.auth import router as auth_router
from .routes.health import router as health_router
from .routes.monolith import router as monolith_router
from .services.proxy import close_proxy_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — cleanup on shutdown."""
    logger.info("API Gateway started on port %d", settings.HTTP_PORT)
    yield
    await close_proxy_client()
    logger.info("API Gateway stopped")


app = FastAPI(
    title="WordFix API Gateway",
    version=settings.VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    lifespan=lifespan,
)

# ── Middleware (order matters — outermost first) ─────────

# 1. Request ID
app.add_middleware(RequestIDMiddleware)

# 2. CORS
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. JWT Auth — validates tokens, injects user_id into request.state
# Public paths that don't require auth
GATEWAY_PUBLIC_PATHS = {
    "/api/v1/health",
    "/api/v1/auth/register",
    "/api/v1/auth/login",
    "/api/v1/auth/token/refresh",
    "/api/v1/auth/google",
    "/api/v1/auth/providers",
    "/api/v1/auth/onboarding",
    "/api/v1/system",
    "/docs",
    "/openapi.json",
}

app.add_middleware(
    JWTAuthMiddleware,
    secret_key=settings.JWT_SECRET,
    algorithm=settings.JWT_ALGORITHM,
    public_paths=GATEWAY_PUBLIC_PATHS,
)

# ── Routes (order matters — specific before catch-all) ───

# Health first (most specific)
app.include_router(health_router)

# Auth routes (handles /api/v1/auth/*)
app.include_router(auth_router)

# Monolith proxy (catch-all for /api/v1/*)
app.include_router(monolith_router)
