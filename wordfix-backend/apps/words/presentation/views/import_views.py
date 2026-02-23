"""
Import views — smart text analysis, word import, and CSV import.
"""

from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.helpers import build_success_response, build_error_response
from ..dependencies import (
    get_analyze_text_use_case,
    get_import_words_use_case,
    get_csv_validate_use_case,
    get_csv_import_use_case,
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
        result = use_case.execute(
            user_id=request.user.id,
            text=serializer.validated_data["text"],
            max_words=serializer.validated_data.get("max_words", 50),
        )

        return Response(
            build_success_response(
                data=result,
                message=f"Found {result.get('total_found', 0)} words for you.",
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
            if xp_result:
                result["xp_earned"] = xp_result.get("xp_gained", 0)
                result["xp_details"] = xp_result
            else:
                result["xp_earned"] = 0

        return Response(
            build_success_response(data=result, message=f"{result['added']} words added."),
            status=status.HTTP_201_CREATED,
        )


class CSVValidateView(APIView):
    """POST /api/v1/words/import/csv/validate/ — Validate CSV before import."""

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request) -> Response:
        from ..serializers import CSVUploadSerializer

        serializer = CSVUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded_file = serializer.validated_data["file"]
        try:
            file_content = uploaded_file.read().decode("utf-8")
        except UnicodeDecodeError:
            return Response(
                build_error_response(message="File encoding error. Use UTF-8."),
                status=status.HTTP_400_BAD_REQUEST,
            )

        use_case = get_csv_validate_use_case()
        result = use_case.execute(file_content)

        return Response(
            build_success_response(
                data=result,
                message="CSV validated.",
            ),
            status=status.HTTP_200_OK,
        )


class CSVImportView(APIView):
    """POST /api/v1/words/import/csv/ — Import words from CSV."""

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request) -> Response:
        from ..serializers import CSVUploadSerializer

        serializer = CSVUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded_file = serializer.validated_data["file"]
        try:
            file_content = uploaded_file.read().decode("utf-8")
        except UnicodeDecodeError:
            return Response(
                build_error_response(message="File encoding error. Use UTF-8."),
                status=status.HTTP_400_BAD_REQUEST,
            )

        use_case = get_csv_import_use_case()
        result = use_case.execute(
            user_id=request.user.id,
            file_content=file_content,
        )

        # Check for error (max rows exceeded)
        if result["imported"] == 0 and result["errors"]:
            return Response(
                build_error_response(
                    message=result["errors"][0] if result["errors"] else "Import failed.",
                    errors={"details": result["errors"]},
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Award XP for imported words
        if result["imported"] > 0:
            xp_result = _award_xp(request.user.id, "word_added",
                                  f"CSV imported {result['imported']} words")
            _increment_progress(request.user.id, words_learned_total=result["imported"])
            if xp_result:
                result["xp_earned"] = xp_result.get("xp_gained", 0)
            else:
                result["xp_earned"] = 0

        return Response(
            build_success_response(
                data=result,
                message=f"{result['imported']} words imported from CSV.",
            ),
            status=status.HTTP_201_CREATED,
        )
