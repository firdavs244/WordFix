"""
System health and config status API views.
"""

import logging

from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.health import HealthRegistry
from apps.common.config import ConfigValidator
from apps.common.utils.helpers import build_success_response

logger = logging.getLogger(__name__)


class DetailedHealthCheckView(APIView):
    """
    GET /api/v1/system/health/detailed/

    Returns detailed health status of all services including
    circuit breaker states and response times.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request) -> Response:
        data = HealthRegistry.check_all()
        return Response(build_success_response(data=data, message="Health check complete."))


class ConfigStatusView(APIView):
    """
    GET /api/v1/system/config/status/

    Returns configuration status showing which services are configured,
    which are using fallback, and which defaults are in use.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request) -> Response:
        data = ConfigValidator.validate_all()
        return Response(build_success_response(data=data, message="Config status retrieved."))


class AIStatusView(APIView):
    """
    GET /api/v1/system/ai-status/

    Returns AI provider configuration and status.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request) -> Response:
        from core.services.ai.ai_factory import AIProviderFactory

        try:
            factory_data = AIProviderFactory.get_all_provider_status()
        except Exception as e:
            logger.error(f"Failed to get AI status: {e}")
            factory_data = {
                "active_provider": "fallback",
                "providers": {},
                "fallback_active": True,
            }

        data = {
            **factory_data,
            "configured_providers": {
                "groq": {
                    "has_api_key": bool(getattr(settings, "GROQ_API_KEY", "")),
                    "model": getattr(settings, "GROQ_MODEL", ""),
                },
                "gemini": {
                    "has_api_key": bool(getattr(settings, "GEMINI_API_KEY", "")),
                    "model": getattr(settings, "GEMINI_MODEL", ""),
                },
                "openai": {
                    "has_api_key": bool(getattr(settings, "OPENAI_API_KEY", "")),
                    "model": getattr(settings, "OPENAI_MODEL", ""),
                },
            },
            "settings_ai_provider": getattr(settings, "AI_PROVIDER", ""),
        }
        return Response(build_success_response(data=data, message="AI status retrieved."))


class AIPingView(APIView):
    """
    POST /api/v1/system/ai-ping/

    Makes an actual AI API call to verify the provider is working.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        from core.services.ai.ai_factory import AIProviderFactory

        AIProviderFactory.reset()
        provider = AIProviderFactory.get_provider()
        provider_name = provider.get_provider_name()

        try:
            result = provider.generate_text("Reply with exactly: WORKING")
            return Response(build_success_response(
                data={
                    "provider": provider_name,
                    "status": "working",
                    "response": result[:100],
                },
                message="AI provider is working.",
            ))
        except Exception as e:
            logger.error(f"AI Ping failed for {provider_name}: {e}")
            return Response(
                build_success_response(
                    data={
                        "provider": provider_name,
                        "status": "error",
                        "error": str(e),
                    },
                    message="AI provider failed.",
                ),
                status=503,
            )
