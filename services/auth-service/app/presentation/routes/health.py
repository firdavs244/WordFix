"""
Health check route for the Auth Service.
"""

from fastapi import APIRouter

from ...config import settings
from ...database import engine

router = APIRouter(tags=["Health"])


@router.get("/health/")
async def health_check():
    """Health check endpoint for Docker/Swarm health probes."""
    services = {}

    # Check database
    try:
        from sqlalchemy import text
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        services["db"] = "up"
    except Exception:
        services["db"] = "down"

    db_up = services["db"] == "up"

    return {
        "status": "healthy" if db_up else "unhealthy",
        "service": settings.SERVICE_NAME,
        "version": settings.VERSION,
        "services": services,
    }
