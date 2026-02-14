"""
Adaptive-intelligence API views.
"""

import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.helpers import build_success_response, build_error_response
from apps.users.presentation.learning_deps import (
    get_accept_recommendation_use_case,
    get_adaptive_difficulty_use_case,
    get_analyze_profile_use_case,
    get_domain_coverage_use_case,
    get_learning_profile_use_case,
    get_mistake_patterns_use_case,
    get_recommendations_use_case,
)
from apps.users.presentation.learning_serializers import (
    AcceptRecommendationSerializer,
)

logger = logging.getLogger(__name__)


class LearningProfileView(APIView):
    """GET /api/v1/learning-profile/ — Get user's learning profile."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        use_case = get_learning_profile_use_case()
        data = use_case.execute(request.user.id)
        return Response(
            build_success_response(data=data, message="Learning profile retrieved."),
        )


class AnalyzeLearningProfileView(APIView):
    """POST /api/v1/learning-profile/analyze/ — Run full analysis."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        use_case = get_analyze_profile_use_case()
        data = use_case.execute(request.user.id)
        return Response(
            build_success_response(data=data, message="Learning profile analyzed."),
        )


class MistakePatternsView(APIView):
    """GET /api/v1/learning-profile/mistake-patterns/ — List mistake patterns."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        include_resolved = request.query_params.get("include_resolved", "false").lower() == "true"
        use_case = get_mistake_patterns_use_case()
        data = use_case.execute(request.user.id, include_resolved=include_resolved)
        return Response(
            build_success_response(data=data, message="Mistake patterns retrieved."),
        )


class WordRecommendationsView(APIView):
    """
    GET  /api/v1/learning-profile/recommendations/ — Get recommendations.
    POST /api/v1/learning-profile/recommendations/ — Accept a recommendation.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        count = int(request.query_params.get("count", 10))
        use_case = get_recommendations_use_case()
        data = use_case.execute(request.user.id, count=count)
        return Response(
            build_success_response(data=data, message="Recommendations retrieved."),
        )

    def post(self, request) -> Response:
        serializer = AcceptRecommendationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case = get_accept_recommendation_use_case()
        data = use_case.execute(
            user_id=request.user.id,
            recommendation_id=serializer.validated_data["recommendation_id"],
        )
        return Response(
            build_success_response(data=data, message="Recommendation accepted."),
        )


class DomainCoverageView(APIView):
    """GET /api/v1/learning-profile/domain-coverage/ — Get domain coverage."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        use_case = get_domain_coverage_use_case()
        data = use_case.execute(request.user.id)
        return Response(
            build_success_response(data=data, message="Domain coverage retrieved."),
        )


class AdaptiveDifficultyView(APIView):
    """GET /api/v1/learning-profile/difficulty/ — Get adaptive difficulty."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        recent_accuracy = request.query_params.get("recent_accuracy")
        if recent_accuracy is not None:
            recent_accuracy = float(recent_accuracy)
        use_case = get_adaptive_difficulty_use_case()
        data = use_case.execute(request.user.id, recent_accuracy=recent_accuracy)
        return Response(
            build_success_response(data=data, message="Adaptive difficulty retrieved."),
        )
