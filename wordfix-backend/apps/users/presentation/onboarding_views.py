"""
Onboarding views — level assessment test.
"""

import logging

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.helpers import build_success_response, build_error_response
from .onboarding_dependencies import (
    get_onboarding_questions_use_case,
    get_submit_onboarding_use_case,
    get_skip_onboarding_use_case,
)
from .serializers import OnboardingSubmitSerializer

logger = logging.getLogger(__name__)


class OnboardingQuestionsView(APIView):
    """GET /api/v1/auth/onboarding/questions/ — Get onboarding questions."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request) -> Response:
        use_case = get_onboarding_questions_use_case()
        questions = use_case.execute()
        return Response(
            build_success_response(
                data={"questions": questions},
                message=f"Found {len(questions)} questions.",
            ),
            status=status.HTTP_200_OK,
        )


class OnboardingSubmitView(APIView):
    """POST /api/v1/auth/onboarding/submit/ — Submit onboarding answers."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = OnboardingSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_submit_onboarding_use_case()
        result = use_case.execute(
            user_id=request.user.id,
            answers=[
                {"question_id": str(a["question_id"]), "answer": a["answer"]}
                for a in serializer.validated_data["answers"]
            ],
        )

        return Response(
            build_success_response(
                data=result,
                message=result.get("message", "Level determined."),
            ),
            status=status.HTTP_200_OK,
        )


class OnboardingSkipView(APIView):
    """POST /api/v1/auth/onboarding/skip/ — Skip onboarding test."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        use_case = get_skip_onboarding_use_case()
        result = use_case.execute(user_id=request.user.id)

        return Response(
            build_success_response(
                data=result,
                message=result.get("message", "Onboarding skipped."),
            ),
            status=status.HTTP_200_OK,
        )


class OnboardingStatusView(APIView):
    """GET /api/v1/auth/onboarding/status/ — Check onboarding status."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        from apps.users.infrastructure.models import OnboardingResult

        completed = OnboardingResult.objects.filter(user=request.user).exists()
        data = {
            "completed": completed,
            "has_completed_onboarding": request.user.has_completed_onboarding,
        }

        if completed:
            result = OnboardingResult.objects.get(user=request.user)
            data["determined_level"] = result.determined_level
            data["total_correct"] = result.total_correct
            data["total_questions"] = result.total_questions

        return Response(
            build_success_response(
                data=data,
                message="Onboarding status retrieved.",
            ),
            status=status.HTTP_200_OK,
        )
