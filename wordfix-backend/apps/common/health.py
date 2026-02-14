"""
Service Health Registry for WordFix.

Aggregates the health of all external services into a single view.
Uses ConfigValidator + Circuit Breaker data.
"""

import logging
import time
from dataclasses import dataclass
from datetime import datetime, timezone

from django.core.cache import cache

logger = logging.getLogger(__name__)

HEALTH_CACHE_KEY = "service_health_registry"
HEALTH_CACHE_TTL = 30  # seconds


@dataclass
class ServiceHealthStatus:
    """Health status for a single service."""

    name: str
    status: str  # 'healthy', 'degraded', 'unavailable'
    message: str
    last_check: str  # ISO timestamp
    circuit_state: str  # 'closed', 'open', 'half_open'
    response_time_ms: float


class HealthRegistry:
    """
    Aggregates health data from ConfigValidator and circuit breakers.

    Results are cached for 30 seconds to avoid overwhelming checks.
    """

    @classmethod
    def check_all(cls) -> dict:
        """
        Check all services and return health data.

        Returns:
            dict with 'services' list, 'overall_status', 'checked_at'.
        """
        cached = cls.get_cached()
        if cached is not None:
            return cached

        from apps.common.config import ConfigValidator
        from apps.common.circuit_breaker import CIRCUITS

        config_result = ConfigValidator.validate_all()
        now = datetime.now(timezone.utc).isoformat()

        services = []
        for svc in config_result["services"]:
            name = svc["name"]
            circuit = CIRCUITS.get(name)
            circuit_state = "closed"
            if circuit:
                circuit_state = circuit.get_state().value

            # Determine health status
            start = time.time()
            if svc["status"] == "ready" and circuit_state == "closed":
                health_status = "healthy"
                message = f"{name} is operational"
            elif svc["status"] == "fallback" or circuit_state in ("half_open",):
                health_status = "degraded"
                message = f"{name} is using fallback"
            elif circuit_state == "open":
                health_status = "unavailable"
                message = f"{name} circuit is open"
            else:
                health_status = "degraded"
                message = f"{name} is in {svc['status']} mode"
            elapsed = (time.time() - start) * 1000

            services.append(
                {
                    "name": name,
                    "status": health_status,
                    "message": message,
                    "last_check": now,
                    "circuit_state": circuit_state,
                    "response_time_ms": round(elapsed, 2),
                }
            )

        overall = cls._compute_overall(services)

        result = {
            "services": services,
            "overall_status": overall,
            "checked_at": now,
        }

        cache.set(HEALTH_CACHE_KEY, result, HEALTH_CACHE_TTL)
        return result

    @classmethod
    def get_cached(cls) -> dict | None:
        """Return cached health data, or None if expired."""
        return cache.get(HEALTH_CACHE_KEY)

    @classmethod
    def _compute_overall(cls, services: list[dict]) -> str:
        """
        Compute overall status from individual service statuses.

        Returns:
            'healthy'   — all services healthy.
            'degraded'  — at least one degraded, none unavailable critical.
            'unhealthy' — any critical service unavailable.
        """
        statuses = {s["status"] for s in services}

        if statuses == {"healthy"}:
            return "healthy"

        # Check if critical services (database) are unavailable
        critical_services = {"database"}
        for svc in services:
            if svc["name"] in critical_services and svc["status"] == "unavailable":
                return "unhealthy"

        if "unavailable" in statuses or "degraded" in statuses:
            return "degraded"

        return "healthy"

    @classmethod
    def get_overall_status(cls) -> str:
        """Quick shortcut for the overall status string."""
        data = cls.check_all()
        return data["overall_status"]
