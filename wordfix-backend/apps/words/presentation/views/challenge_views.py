"""
Daily challenge views — today's challenges, claim bonus.
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.helpers import build_success_response
from ..dependencies import (
    get_claim_daily_bonus_use_case,
    get_daily_challenges_use_case,
)


class DailyChallengesView(APIView):
    """GET /api/v1/challenges/today/ — Get today's challenges."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        use_case = get_daily_challenges_use_case()
        result = use_case.execute(user_id=request.user.id)

        return Response(
            build_success_response(
                data=result,
                message="Today's challenges.",
            )
        )


class ClaimDailyBonusView(APIView):
    """POST /api/v1/challenges/claim/ — Claim daily bonus."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        use_case = get_claim_daily_bonus_use_case()
        result = use_case.execute(user_id=request.user.id)

        return Response(
            build_success_response(
                data=result,
                message="Daily bonus claimed!",
            )
        )
