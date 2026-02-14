"""
System health and config status API views.
"""

import logging

from rest_framework.permissions import AllowAny
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
