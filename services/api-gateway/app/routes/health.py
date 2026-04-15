"""
Health check — aggregated health from all services.
"""

import logging

import httpx
from fastapi import APIRouter

from ..config import settings

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])


@router.get("/api/v1/health/")
async def health_check():
    """
    Aggregated health check — queries all backend services.
    """
    services = {
        "gateway": "up",
        "auth_service": await _check_service(
            f"http://{settings.AUTH_SERVICE_GRPC.split(':')[0]}:8001/health/"
        ),
        "monolith": await _check_service(f"{settings.MONOLITH_URL}/api/v1/health/"),
    }

    all_up = all(s == "up" for s in services.values())

    return {
        "status": "healthy" if all_up else "degraded",
        "service": settings.SERVICE_NAME,
        "version": settings.VERSION,
        "services": services,
    }


async def _check_service(url: str) -> str:
    """Check if a service is healthy."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                return "up"
            return "degraded"
    except Exception:
        return "down"


@router.get("/api/v1/system/gateway-status/")
async def gateway_status():
    """Gateway-specific status endpoint."""
    return {
        "success": True,
        "data": {
            "service": settings.SERVICE_NAME,
            "version": settings.VERSION,
            "auth_service_target": settings.AUTH_SERVICE_GRPC,
            "monolith_target": settings.MONOLITH_URL,
        },
        "message": "Gateway status.",
        "errors": None,
        "meta": None,
    }
