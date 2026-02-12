"""
Review views — spaced repetition review sessions, streaks, daily progress.
"""

import math

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.helpers import build_success_response
from ..dependencies import (
    get_review_words_use_case,
    get_start_session_use_case,
    get_submit_answer_use_case,
    get_complete_session_use_case,
    get_review_summary_use_case,
    get_session_repository,
    get_sr_service,
    get_streak_repository,
    get_activity_repository,
    get_word_repository,
)
from ..serializers import (
    ReviewSubmitSerializer,
)
from .word_views import (
    _entity_to_dict,
    _session_to_dict,
    _award_xp,
    _check_badges,
    _increment_progress,
)


class ReviewWordsView(APIView):
    """GET /api/v1/review/words/ — Get words for review."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        session_type = request.query_params.get("type", "review")
        limit = int(request.query_params.get("limit", 20))
        limit = min(limit, 50)

        use_case = get_review_words_use_case()
        words = use_case.execute(
            user_id=request.user.id,
            limit=limit,
            session_type=session_type,
        )

        return Response(
            build_success_response(data=[_entity_to_dict(w) for w in words]),
        )


class ReviewSessionCreateView(APIView):
    """POST /api/v1/review/sessions/ — Start a review session."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        from ..serializers import ReviewSessionCreateSerializer

        serializer = ReviewSessionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_start_session_use_case()
        session = use_case.execute(
            user_id=request.user.id,
            session_type=serializer.validated_data.get("session_type", "review"),
        )

        return Response(
            build_success_response(data=_session_to_dict(session), message="Session started."),
            status=status.HTTP_201_CREATED,
        )


class ReviewSessionDetailView(APIView):
    """GET /api/v1/review/sessions/{id}/ — Get session details."""

    permission_classes = [IsAuthenticated]

    def get(self, request, session_id) -> Response:
        repo = get_session_repository()
        session = repo.get_by_id(session_id=session_id, user_id=request.user.id)
        return Response(
            build_success_response(data=_session_to_dict(session)),
        )


class SubmitAnswerView(APIView):
    """POST /api/v1/review/sessions/{id}/answer/ — Submit a review answer."""

    permission_classes = [IsAuthenticated]

    def post(self, request, session_id) -> Response:
        serializer = ReviewSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_submit_answer_use_case()
        result = use_case.execute(
            session_id=session_id,
            word_id=serializer.validated_data["word_id"],
            user_id=request.user.id,
            quality=serializer.validated_data["quality"],
            response_time_ms=serializer.validated_data.get("response_time_ms", 0),
        )

        # XP for review answer
        reason = "review_correct" if result["is_correct"] else "review_incorrect"
        xp_result = _award_xp(request.user.id, reason)

        # Check if word became mastered
        if result["word"].is_mastered:
            _award_xp(request.user.id, "word_mastered")
            _increment_progress(request.user.id, words_mastered_total=1)

        response_data = {
            "word": _entity_to_dict(result["word"]),
            "session": _session_to_dict(result["session"]),
            "is_correct": result["is_correct"],
        }
        if xp_result:
            response_data["xp_earned"] = xp_result.get("xp_gained", 0)
            response_data["xp_details"] = xp_result

        return Response(build_success_response(data=response_data))


class CompleteSessionView(APIView):
    """POST /api/v1/review/sessions/{id}/complete/ — Complete a session."""

    permission_classes = [IsAuthenticated]

    def post(self, request, session_id) -> Response:
        use_case = get_complete_session_use_case()
        session = use_case.execute(
            session_id=session_id,
            user_id=request.user.id,
        )

        # XP for completing review session
        xp_result = _award_xp(request.user.id, "review_complete")
        _increment_progress(request.user.id, reviews_completed=1)

        # Perfect review bonus
        is_perfect = session.total_words > 0 and session.incorrect_count == 0
        if is_perfect:
            _award_xp(request.user.id, "review_perfect")
            _increment_progress(request.user.id, perfect_scores=1)

        # Check badges (with streak context)
        try:
            streak_repo = get_streak_repository()
            streak = streak_repo.get_or_create(request.user.id)
            context = {
                "current_streak": streak.current_streak,
                "perfect_review": is_perfect,
            }
        except Exception:
            context = {"perfect_review": is_perfect}

        new_badges = _check_badges(request.user.id, context=context)

        response_data = _session_to_dict(session)
        if xp_result:
            response_data["xp_earned"] = xp_result.get("xp_gained", 0)
            response_data["xp_details"] = xp_result
        if new_badges:
            response_data["new_badges"] = [{"code": b.code, "name": b.name, "icon": b.icon} for b in new_badges]

        return Response(
            build_success_response(
                data=response_data,
                message="Session completed.",
            ),
        )


class ReviewSummaryView(APIView):
    """GET /api/v1/review/summary/ — Dashboard review summary."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        use_case = get_review_summary_use_case()
        summary = use_case.execute(user_id=request.user.id)
        return Response(build_success_response(data=summary))


class ReviewHistoryView(APIView):
    """GET /api/v1/review/history/ — Review session history."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 10))

        repo = get_session_repository()
        sessions, total = repo.get_by_user(
            user_id=request.user.id,
            page=page,
            page_size=page_size,
        )

        total_pages = math.ceil(total / page_size) if page_size > 0 else 1

        return Response({
            "success": True,
            "data": [_session_to_dict(s) for s in sessions],
            "message": "Success",
            "errors": None,
            "meta": {
                "page": page,
                "total_pages": total_pages,
                "total_count": total,
                "page_size": page_size,
            },
        })


class StreakView(APIView):
    """GET /api/v1/review/streak/ — Get streak info."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        repo = get_streak_repository()
        streak = repo.get_or_create(user_id=request.user.id)

        data = {
            "id": str(streak.id),
            "current_streak": streak.current_streak,
            "longest_streak": streak.longest_streak,
            "last_activity_date": str(streak.last_activity_date) if streak.last_activity_date else None,
            "streak_frozen_until": str(streak.streak_frozen_until) if streak.streak_frozen_until else None,
            "total_review_days": streak.total_review_days,
        }

        return Response(build_success_response(data=data))


class DailyProgressView(APIView):
    """GET /api/v1/review/daily-progress/ — Today's progress."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        repo = get_activity_repository()
        activity = repo.get_or_create_today(user_id=request.user.id)

        data = {
            "id": str(activity.id),
            "words_reviewed": activity.words_reviewed,
            "words_added": activity.words_added,
            "words_mastered": activity.words_mastered,
            "correct_answers": activity.correct_answers,
            "incorrect_answers": activity.incorrect_answers,
            "total_time_seconds": activity.total_time_seconds,
            "goal_completed": activity.goal_completed,
            "xp_earned": activity.xp_earned,
            "date": str(activity.date),
        }

        return Response(build_success_response(data=data))


class PredictedIntervalsView(APIView):
    """GET /api/v1/review/words/{word_id}/predict/ — Predicted intervals."""

    permission_classes = [IsAuthenticated]

    def get(self, request, word_id) -> Response:
        word_repo = get_word_repository()
        word = word_repo.get_by_id(word_id=word_id, user_id=request.user.id)

        sr_service = get_sr_service()
        predictions = sr_service.get_predicted_intervals(word)

        return Response(build_success_response(data=predictions))
