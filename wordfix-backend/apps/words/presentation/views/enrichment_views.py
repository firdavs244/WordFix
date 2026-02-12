"""
Enrichment views — AI-powered word enrichment.
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.helpers import build_success_response
from ..dependencies import (
    get_batch_enrich_task,
    get_enrich_word_task,
    get_pending_enrichment_word_ids,
    get_word_repository,
)


class EnrichWordView(APIView):
    """POST /api/v1/words/{word_id}/enrich/ — Enrich one word."""

    permission_classes = [IsAuthenticated]

    def post(self, request, word_id) -> Response:
        # Verify word belongs to user
        word_repo = get_word_repository()
        word_repo.get_by_id(word_id=word_id, user_id=request.user.id)

        enrich_task = get_enrich_word_task()
        if enrich_task:
            enrich_task(str(word_id), str(request.user.id))

        return Response(
            build_success_response(message="Enrichment started."),
            status=status.HTTP_202_ACCEPTED,
        )


class EnrichAllView(APIView):
    """POST /api/v1/words/enrich-all/ — Enrich all pending words."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        pending_ids = get_pending_enrichment_word_ids(request.user.id)

        if not pending_ids:
            return Response(
                build_success_response(data={"count": 0}, message="No words to enrich."),
            )

        batch_task = get_batch_enrich_task()
        if batch_task:
            batch_task(str(request.user.id), [str(i) for i in pending_ids])

        return Response(
            build_success_response(
                data={"count": len(pending_ids)},
                message=f"Enrichment started for {len(pending_ids)} words.",
            ),
            status=status.HTTP_202_ACCEPTED,
        )


class EnrichmentStatusView(APIView):
    """GET /api/v1/words/{word_id}/enrichment-status/ — Check enrichment status."""

    permission_classes = [IsAuthenticated]

    def get(self, request, word_id) -> Response:
        word_repo = get_word_repository()
        word = word_repo.get_by_id(word_id=word_id, user_id=request.user.id)

        return Response(
            build_success_response(data={
                "enrichment_status": word.enrichment_status,
                "enrichment_error": word.enrichment_error or "",
                "is_enriched": word.is_enriched,
                "enriched_at": word.enriched_at.isoformat() if word.enriched_at else None,
            }),
        )


class EnrichmentRetryView(APIView):
    """POST /api/v1/words/{word_id}/enrichment-retry/ — Retry failed enrichment."""

    permission_classes = [IsAuthenticated]

    def post(self, request, word_id) -> Response:
        word_repo = get_word_repository()
        word = word_repo.get_by_id(word_id=word_id, user_id=request.user.id)

        if word.enrichment_status != "failed":
            return Response(
                build_success_response(
                    message="Word enrichment is not in failed state.",
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Reset to pending so the enrichment task picks it up
        word_repo.update(
            word_id=word_id, user_id=request.user.id,
            enrichment_status="pending", enrichment_error="",
        )

        # Trigger enrichment
        enrich_task = get_enrich_word_task()
        if enrich_task:
            enrich_task(str(word_id), str(request.user.id))

        return Response(
            build_success_response(message="Enrichment retry started."),
            status=status.HTTP_202_ACCEPTED,
        )
