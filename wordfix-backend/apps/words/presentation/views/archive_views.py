"""
Archive views for word archiving endpoints.
"""

import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.helpers import build_success_response
from apps.words.presentation.dependencies.archive_deps import (
    get_archive_use_case,
    get_archived_words_use_case,
    get_bulk_archive_use_case,
    get_unarchive_use_case,
)
from apps.words.presentation.serializers.archive_serializers import (
    BulkArchiveSerializer,
)

logger = logging.getLogger(__name__)


class ArchiveWordView(APIView):
    """POST /api/v1/words/<word_id>/archive/ — Archive a word."""

    permission_classes = [IsAuthenticated]

    def post(self, request, word_id):
        use_case = get_archive_use_case()
        result = use_case.execute(request.user.id, word_id)
        return Response(
            build_success_response(data=result, message="Word archived."),
            status=status.HTTP_200_OK,
        )


class UnarchiveWordView(APIView):
    """POST /api/v1/words/<word_id>/unarchive/ — Unarchive a word."""

    permission_classes = [IsAuthenticated]

    def post(self, request, word_id):
        use_case = get_unarchive_use_case()
        result = use_case.execute(request.user.id, word_id)
        return Response(
            build_success_response(data=result, message="Word unarchived."),
            status=status.HTTP_200_OK,
        )


class ArchivedWordsListView(APIView):
    """GET /api/v1/words/archived/ — List archived words."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))
        use_case = get_archived_words_use_case()
        result = use_case.execute(request.user.id, page, page_size)

        words = result["words"]
        words_data = []
        for w in words:
            words_data.append({
                "id": str(w.id),
                "original_word": w.original_word,
                "translation": w.translation,
                "pronunciation": w.pronunciation,
                "part_of_speech": w.part_of_speech,
                "definition": w.definition,
                "difficulty_level": w.difficulty_level,
                "confidence_score": w.confidence_score,
                "is_mastered": w.is_mastered,
                "is_archived": w.is_archived,
                "archived_at": w.archived_at.isoformat() if w.archived_at else None,
                "created_at": w.created_at.isoformat() if w.created_at else None,
            })

        return Response(
            build_success_response(
                data=words_data,
                message="Archived words retrieved.",
                meta={
                    "total": result["total"],
                    "page": result["page"],
                    "page_size": result["page_size"],
                    "total_pages": (result["total"] + result["page_size"] - 1) // max(result["page_size"], 1),
                },
            )
        )


class BulkArchiveView(APIView):
    """POST /api/v1/words/archive/bulk/ — Bulk archive words."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BulkArchiveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case = get_bulk_archive_use_case()
        result = use_case.execute(request.user.id, serializer.validated_data["word_ids"])
        return Response(
            build_success_response(data=result, message="Words archived."),
            status=status.HTTP_200_OK,
        )
