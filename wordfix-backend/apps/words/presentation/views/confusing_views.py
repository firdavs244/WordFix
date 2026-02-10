"""
Confusing pairs views — list, detail, drill, resolve, count.
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.helpers import build_success_response
from ..dependencies import (
    get_confusing_pair_count_use_case,
    get_confusing_pair_detail_use_case,
    get_confusing_pairs_use_case,
    get_generate_drill_use_case,
    get_resolve_pair_use_case,
)


class ConfusingPairsListView(APIView):
    """GET /api/v1/words/confusing-pairs/ — List confusing pairs."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        include_resolved = request.query_params.get("include_resolved", "false").lower() == "true"
        use_case = get_confusing_pairs_use_case()
        pairs = use_case.execute(
            user_id=request.user.id,
            include_resolved=include_resolved,
        )

        return Response(
            build_success_response(
                data=pairs,
                message=f"Found {len(pairs)} confusing pairs.",
            )
        )


class ConfusingPairDetailView(APIView):
    """GET /api/v1/words/confusing-pairs/{id}/ — Pair detail."""

    permission_classes = [IsAuthenticated]

    def get(self, request, pair_id) -> Response:
        use_case = get_confusing_pair_detail_use_case()
        pair = use_case.execute(user_id=request.user.id, pair_id=pair_id)

        return Response(build_success_response(data=pair))


class ConfusingPairDrillView(APIView):
    """POST /api/v1/words/confusing-pairs/{id}/drill/ — Generate/get drill."""

    permission_classes = [IsAuthenticated]

    def post(self, request, pair_id) -> Response:
        use_case = get_generate_drill_use_case()
        drill = use_case.execute(user_id=request.user.id, pair_id=pair_id)

        return Response(
            build_success_response(
                data=drill,
                message="Drill generated.",
            )
        )


class ConfusingPairResolveView(APIView):
    """POST /api/v1/words/confusing-pairs/{id}/resolve/ — Resolve pair."""

    permission_classes = [IsAuthenticated]

    def post(self, request, pair_id) -> Response:
        use_case = get_resolve_pair_use_case()
        use_case.execute(user_id=request.user.id, pair_id=pair_id)

        return Response(
            build_success_response(
                data={"resolved": True},
                message="Confusing pair marked as resolved.",
            )
        )


class ConfusingPairCountView(APIView):
    """GET /api/v1/words/confusing-pairs/count/ — Unresolved count."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        use_case = get_confusing_pair_count_use_case()
        count = use_case.execute(user_id=request.user.id)

        return Response(
            build_success_response(data={"count": count})
        )
