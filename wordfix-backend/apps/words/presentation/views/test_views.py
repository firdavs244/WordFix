"""
Test views — vocabulary test generation, submission, and history.
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.helpers import build_success_response
from ..dependencies import (
    get_generate_test_use_case,
    get_submit_test_answer_use_case,
    get_complete_test_session_use_case,
    get_test_history_use_case,
    get_test_detail_use_case,
)
from ..serializers import (
    TestAnswerSubmitSerializer,
    TestGenerateSerializer,
    TestQuestionSerializer,
    TestSessionSerializer,
)
from .word_views import (
    _award_xp,
    _check_badges,
    _increment_progress,
)


class TestGenerateView(APIView):
    """POST /api/v1/tests/generate/ — Generate a test."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = TestGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_generate_test_use_case()
        result = use_case.execute(
            user_id=request.user.id,
            test_type=serializer.validated_data["test_type"],
            question_count=serializer.validated_data["question_count"],
            difficulty=serializer.validated_data["difficulty"],
        )

        session_data = TestSessionSerializer(result["session"]).data
        questions_data = TestQuestionSerializer(result["questions"], many=True).data

        return Response(
            build_success_response(
                data={"session": session_data, "questions": questions_data},
                message="Test generated successfully.",
            ),
            status=status.HTTP_201_CREATED,
        )


class TestSubmitAnswerView(APIView):
    """POST /api/v1/tests/{session_id}/answer/ — Submit a test answer."""

    permission_classes = [IsAuthenticated]

    def post(self, request, session_id) -> Response:
        serializer = TestAnswerSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_submit_test_answer_use_case()
        result = use_case.execute(
            question_id=serializer.validated_data["question_id"],
            user_id=request.user.id,
            answer=serializer.validated_data["answer"],
            response_time_ms=serializer.validated_data.get("response_time_ms", 0),
        )

        return Response(build_success_response(data=result))


class TestCompleteView(APIView):
    """POST /api/v1/tests/{session_id}/complete/ — Complete a test."""

    permission_classes = [IsAuthenticated]

    def post(self, request, session_id) -> Response:
        use_case = get_complete_test_session_use_case()
        session = use_case.execute(session_id=session_id, user_id=request.user.id)

        # XP for completing test
        xp_result = _award_xp(request.user.id, "test_complete")
        _increment_progress(request.user.id, tests_completed=1)

        # Score bonuses
        score_pct = session.score_percentage if hasattr(session, 'score_percentage') else 0
        is_perfect = score_pct >= 99.9
        if is_perfect:
            _award_xp(request.user.id, "test_perfect")
            _increment_progress(request.user.id, perfect_scores=1)
        elif score_pct >= 80:
            _award_xp(request.user.id, "test_good")

        new_badges = _check_badges(request.user.id, context={"perfect_test": is_perfect})

        response_data = TestSessionSerializer(session).data
        if xp_result:
            response_data["xp_earned"] = xp_result
        if new_badges:
            response_data["new_badges"] = [{"code": b.code, "name": b.name, "icon": b.icon} for b in new_badges]

        return Response(
            build_success_response(
                data=response_data,
                message="Test completed.",
            )
        )


class TestHistoryView(APIView):
    """GET /api/v1/tests/history/ — Get test history."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))

        use_case = get_test_history_use_case()
        sessions, total = use_case.execute(
            user_id=request.user.id, page=page, page_size=page_size,
        )

        data = TestSessionSerializer(sessions, many=True).data
        meta = {
            "page": page,
            "page_size": page_size,
            "total_count": total,
            "total_pages": (total + page_size - 1) // page_size,
        }

        return Response(build_success_response(data=data, meta=meta))


class TestSessionDetailView(APIView):
    """GET /api/v1/tests/{session_id}/ — Get test session detail."""

    permission_classes = [IsAuthenticated]

    def get(self, request, session_id) -> Response:
        use_case = get_test_detail_use_case()
        result = use_case.execute(session_id=session_id, user_id=request.user.id)

        session_data = TestSessionSerializer(result["session"]).data
        questions_data = TestQuestionSerializer(result["questions"], many=True).data

        return Response(
            build_success_response(
                data={"session": session_data, "questions": questions_data},
            )
        )
