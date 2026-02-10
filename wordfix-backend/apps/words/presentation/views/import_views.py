"""
Import views — smart text analysis and word import.
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.helpers import build_success_response
from ..dependencies import (
    get_analyze_text_use_case,
    get_import_words_use_case,
)
from .word_views import (
    _award_xp,
    _increment_progress,
)


class AnalyzeTextView(APIView):
    """POST /api/v1/words/import/analyze/ — Analyze text for unknown words."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        from ..serializers import AnalyzeTextSerializer

        serializer = AnalyzeTextSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_analyze_text_use_case()
        suggestions = use_case.execute(
            user_id=request.user.id,
            text=serializer.validated_data["text"],
            max_words=serializer.validated_data.get("max_words", 20),
        )

        return Response(
            build_success_response(
                data={"suggestions": suggestions},
                message=f"Found {len(suggestions)} words for you.",
            )
        )


class ImportAddWordsView(APIView):
    """POST /api/v1/words/import/add/ — Add selected imported words."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        from ..serializers import ImportWordsSerializer

        serializer = ImportWordsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_import_words_use_case()
        result = use_case.execute(
            user_id=request.user.id,
            selected_words=serializer.validated_data["words"],
        )

        # Award XP for each added word
        if result["added"] > 0:
            xp_result = _award_xp(request.user.id, "word_added",
                                  f"Imported {result['added']} words")
            _increment_progress(request.user.id, words_learned_total=result["added"])
            result["xp_earned"] = xp_result

        return Response(
            build_success_response(data=result, message=f"{result['added']} words added."),
            status=status.HTTP_201_CREATED,
        )
