"""
Word presentation layer - API views.
"""

import logging
from dataclasses import asdict

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.helpers import build_success_response
from apps.users.domain.services import XP_REWARDS
from .dependencies import (
    get_add_word_use_case,
    get_batch_enrich_task,
    get_bulk_add_words_use_case,
    get_category_repository,
    get_delete_word_use_case,
    get_enrich_word_task,
    get_pending_enrichment_word_ids,
    get_search_words_use_case,
    get_word_detail_use_case,
    get_word_repository,
    get_word_stats_use_case,
    get_words_use_case,
    get_update_word_use_case,
    get_enrich_use_case,
    get_review_words_use_case,
    get_start_session_use_case,
    get_submit_answer_use_case,
    get_complete_session_use_case,
    get_review_summary_use_case,
    get_session_repository,
    get_sr_service,
    get_streak_repository,
    get_activity_repository,
    get_log_repository,
    get_generate_test_use_case,
    get_submit_test_answer_use_case,
    get_complete_test_session_use_case,
    get_test_history_use_case,
    get_test_detail_use_case,
    get_start_speed_round_use_case,
    get_submit_speed_round_use_case,
    get_start_word_match_use_case,
    get_submit_word_match_use_case,
    get_start_word_context_use_case,
    get_submit_word_context_use_case,
    get_game_history_use_case,
    get_game_stats_use_case,
)
from .serializers import (
    BulkWordCreateSerializer,
    GameSessionSerializer,
    GameStatsSerializer,
    ReviewSubmitSerializer,
    SpeedRoundSubmitSerializer,
    TestAnswerSubmitSerializer,
    TestGenerateSerializer,
    TestQuestionSerializer,
    TestSessionSerializer,
    WordCategorySerializer,
    WordContextSubmitSerializer,
    WordCreateSerializer,
    WordDetailSerializer,
    WordListSerializer,
    WordMatchSubmitSerializer,
    WordStatsSerializer,
    WordUpdateSerializer,
)


def _entity_to_dict(entity):
    """Convert entity dataclass to dict with string UUIDs and datetimes."""
    data = asdict(entity)
    # Convert UUIDs
    for key in ("id", "user_id", "category_id"):
        if key in data and data[key] is not None:
            data[key] = str(data[key])
    # Handle nested category
    if data.get("category") and isinstance(data["category"], dict):
        for k in ("id", "user_id"):
            if k in data["category"] and data["category"][k] is not None:
                data["category"][k] = str(data["category"][k])
    # Handle datetimes
    for key in ("created_at", "updated_at", "next_review_at", "last_reviewed_at", "enriched_at"):
        val = getattr(entity, key, None)
        if val is not None:
            data[key] = val.isoformat()
    # Add computed property
    data["accuracy_rate"] = entity.accuracy_rate
    return data


def _session_to_dict(entity):
    """Convert session entity to dict."""
    data = asdict(entity)
    for key in ("id", "user_id"):
        if key in data and data[key] is not None:
            data[key] = str(data[key])
    for key in ("started_at", "completed_at", "created_at", "updated_at"):
        val = getattr(entity, key, None)
        if val is not None:
            data[key] = val.isoformat()
    return data


logger = logging.getLogger(__name__)


def _award_xp(user_id, reason: str, description: str = "") -> dict | None:
    """Award XP to user. Returns XP result or None on error."""
    try:
        from apps.users.presentation.progress_dependencies import get_xp_service
        xp_service = get_xp_service()
        amount = XP_REWARDS.get(reason, 0)
        if amount > 0:
            return xp_service.award_xp(user_id, amount, reason, description)
    except Exception as e:
        logger.warning(f"Failed to award XP: {e}")
    return None


def _check_badges(user_id, context: dict | None = None) -> list:
    """Check and award badges. Returns list of new badges."""
    try:
        from apps.users.presentation.progress_dependencies import get_badge_service
        badge_service = get_badge_service()
        return badge_service.check_and_award_badges(user_id, context=context)
    except Exception as e:
        logger.warning(f"Failed to check badges: {e}")
    return []


def _increment_progress(user_id, **kwargs):
    """Increment progress counters."""
    try:
        from apps.users.infrastructure.repositories import DjangoProgressRepository
        repo = DjangoProgressRepository()
        repo.increment(user_id, **kwargs)
    except Exception as e:
        logger.warning(f"Failed to increment progress: {e}")


class WordListCreateView(APIView):
    """
    GET /api/v1/words/ — List words with filters
    POST /api/v1/words/ — Create a word
    """

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        # Parse query params
        filters = {}
        if request.query_params.get("category_id"):
            filters["category_id"] = request.query_params["category_id"]
        if request.query_params.get("difficulty_level"):
            filters["difficulty_level"] = request.query_params["difficulty_level"]
        if request.query_params.get("is_mastered") is not None:
            val = request.query_params.get("is_mastered", "").lower()
            if val in ("true", "false"):
                filters["is_mastered"] = val == "true"
        if request.query_params.get("part_of_speech"):
            filters["part_of_speech"] = request.query_params["part_of_speech"]
        if request.query_params.get("search"):
            filters["search"] = request.query_params["search"]

        ordering = request.query_params.get("ordering", "-created_at")
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))
        page_size = min(page_size, 100)

        use_case = get_words_use_case()
        words, total = use_case.execute(
            user_id=request.user.id,
            filters=filters if filters else None,
            ordering=ordering,
            page=page,
            page_size=page_size,
        )

        import math
        total_pages = math.ceil(total / page_size) if page_size > 0 else 1

        words_data = [_entity_to_dict(w) for w in words]

        return Response({
            "success": True,
            "data": words_data,
            "message": "Success",
            "errors": None,
            "meta": {
                "page": page,
                "total_pages": total_pages,
                "total_count": total,
                "page_size": page_size,
            },
        })

    def post(self, request) -> Response:
        serializer = WordCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_add_word_use_case()
        word_entity = use_case.execute(
            user_id=request.user.id,
            data=serializer.validated_data,
        )

        # XP & Progress integration
        xp_result = _award_xp(request.user.id, "word_added")
        _increment_progress(request.user.id, words_learned_total=1)
        new_badges = _check_badges(request.user.id)

        response_data = _entity_to_dict(word_entity)
        if xp_result:
            response_data["xp_earned"] = xp_result
        if new_badges:
            response_data["new_badges"] = [{"code": b.code, "name": b.name, "icon": b.icon} for b in new_badges]

        return Response(
            build_success_response(
                data=response_data,
                message="Word added successfully.",
            ),
            status=status.HTTP_201_CREATED,
        )


class WordDetailView(APIView):
    """
    GET /api/v1/words/{id}/ — Detail
    PATCH /api/v1/words/{id}/ — Update
    DELETE /api/v1/words/{id}/ — Delete
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, word_id) -> Response:
        use_case = get_word_detail_use_case()
        word_entity = use_case.execute(word_id=word_id, user_id=request.user.id)
        return Response(
            build_success_response(data=_entity_to_dict(word_entity)),
        )

    def patch(self, request, word_id) -> Response:
        serializer = WordUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        use_case = get_update_word_use_case()
        word_entity = use_case.execute(
            word_id=word_id,
            user_id=request.user.id,
            data=serializer.validated_data,
        )

        return Response(
            build_success_response(
                data=_entity_to_dict(word_entity),
                message="Word updated successfully.",
            ),
        )

    def delete(self, request, word_id) -> Response:
        use_case = get_delete_word_use_case()
        use_case.execute(word_id=word_id, user_id=request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class WordBulkCreateView(APIView):
    """POST /api/v1/words/bulk/ — Bulk create words."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = BulkWordCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_bulk_add_words_use_case()
        result = use_case.execute(
            user_id=request.user.id,
            words_data=serializer.validated_data["words"],
        )

        return Response(
            build_success_response(data=result, message="Bulk create completed."),
            status=status.HTTP_201_CREATED,
        )


class WordStatsView(APIView):
    """GET /api/v1/words/stats/ — Word statistics."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        use_case = get_word_stats_use_case()
        stats = use_case.execute(user_id=request.user.id)
        return Response(build_success_response(data=stats))


class WordReviewView(APIView):
    """GET /api/v1/words/review/ — Words for review."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        repo = get_word_repository()
        words = repo.get_words_for_review(user_id=request.user.id)
        return Response(
            build_success_response(
                data=[_entity_to_dict(w) for w in words],
            ),
        )


class WordCategoryListCreateView(APIView):
    """
    GET /api/v1/words/categories/ — List categories
    POST /api/v1/words/categories/ — Create category
    """

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        repo = get_category_repository()
        categories = repo.get_all_by_user(user_id=request.user.id)
        data = [asdict(c) for c in categories]
        for item in data:
            item["id"] = str(item["id"])
            item["user_id"] = str(item["user_id"])
            if item.get("created_at"):
                item["created_at"] = item["created_at"].isoformat()
            if item.get("updated_at"):
                item["updated_at"] = item["updated_at"].isoformat()
        return Response(build_success_response(data=data))

    def post(self, request) -> Response:
        serializer = WordCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repo = get_category_repository()
        category = repo.create(user_id=request.user.id, **serializer.validated_data)

        data = asdict(category)
        data["id"] = str(data["id"])
        data["user_id"] = str(data["user_id"])
        if data.get("created_at"):
            data["created_at"] = data["created_at"].isoformat()
        if data.get("updated_at"):
            data["updated_at"] = data["updated_at"].isoformat()

        return Response(
            build_success_response(data=data, message="Category created."),
            status=status.HTTP_201_CREATED,
        )


class WordCategoryDeleteView(APIView):
    """DELETE /api/v1/words/categories/{id}/ — Delete category."""

    permission_classes = [IsAuthenticated]

    def delete(self, request, category_id) -> Response:
        repo = get_category_repository()
        repo.delete(category_id=category_id, user_id=request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


# =============================================================================
# ENRICHMENT VIEWS
# =============================================================================


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


# =============================================================================
# REVIEW VIEWS
# =============================================================================


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
        from .serializers import ReviewSessionCreateSerializer

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
            response_data["xp_earned"] = xp_result

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
            response_data["xp_earned"] = xp_result
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

        import math
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


# =============================================================================
# TEST VIEWS
# =============================================================================


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


# =============================================================================
# GAME VIEWS
# =============================================================================


class SpeedRoundStartView(APIView):
    """POST /api/v1/games/speed-round/start/ — Start speed round."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        use_case = get_start_speed_round_use_case()
        result = use_case.execute(user_id=request.user.id)
        return Response(
            build_success_response(data=result, message="Speed round started!"),
            status=status.HTTP_201_CREATED,
        )


class SpeedRoundSubmitView(APIView):
    """POST /api/v1/games/speed-round/submit/ — Submit speed round."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = SpeedRoundSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_submit_speed_round_use_case()
        session = use_case.execute(
            session_id=serializer.validated_data["session_id"],
            user_id=request.user.id,
            answers=serializer.validated_data["answers"],
            duration_seconds=serializer.validated_data.get("duration_seconds", 60),
        )

        # XP for game
        xp_result = _award_xp(request.user.id, "game_complete")
        _increment_progress(request.user.id, games_played=1)
        total = session.correct_answers + session.incorrect_answers
        if total > 0 and (session.correct_answers / total) >= 0.8:
            _award_xp(request.user.id, "game_good")

        context = {"speed_round_correct": session.correct_answers}
        new_badges = _check_badges(request.user.id, context=context)

        response_data = GameSessionSerializer(session).data
        if xp_result:
            response_data["xp_earned"] = xp_result
        if new_badges:
            response_data["new_badges"] = [{"code": b.code, "name": b.name, "icon": b.icon} for b in new_badges]

        return Response(
            build_success_response(
                data=response_data,
                message="Speed round completed!",
            )
        )


class WordMatchStartView(APIView):
    """POST /api/v1/games/word-match/start/ — Start word match."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        pair_count = request.data.get("pair_count", 8)
        use_case = get_start_word_match_use_case()
        result = use_case.execute(user_id=request.user.id, pair_count=pair_count)
        return Response(
            build_success_response(data=result, message="Word match started!"),
            status=status.HTTP_201_CREATED,
        )


class WordMatchSubmitView(APIView):
    """POST /api/v1/games/word-match/submit/ — Submit word match."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = WordMatchSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_submit_word_match_use_case()
        session = use_case.execute(
            session_id=serializer.validated_data["session_id"],
            user_id=request.user.id,
            pairs=serializer.validated_data["pairs"],
            time_seconds=serializer.validated_data["time_seconds"],
        )

        # XP for game
        xp_result = _award_xp(request.user.id, "game_complete")
        _increment_progress(request.user.id, games_played=1)
        total = session.correct_answers + session.incorrect_answers
        if total > 0 and (session.correct_answers / total) >= 0.8:
            _award_xp(request.user.id, "game_good")

        new_badges = _check_badges(request.user.id)

        response_data = GameSessionSerializer(session).data
        if xp_result:
            response_data["xp_earned"] = xp_result
        if new_badges:
            response_data["new_badges"] = [{"code": b.code, "name": b.name, "icon": b.icon} for b in new_badges]

        return Response(
            build_success_response(
                data=response_data,
                message="Word match completed!",
            )
        )


class WordContextStartView(APIView):
    """POST /api/v1/games/word-context/start/ — Start word context game."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        use_case = get_start_word_context_use_case()
        result = use_case.execute(user_id=request.user.id)
        return Response(
            build_success_response(data=result, message="Word context game started!"),
            status=status.HTTP_201_CREATED,
        )


class WordContextSubmitView(APIView):
    """POST /api/v1/games/word-context/submit/ — Submit word context game."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = WordContextSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_submit_word_context_use_case()
        session = use_case.execute(
            session_id=serializer.validated_data["session_id"],
            user_id=request.user.id,
            answers=serializer.validated_data["answers"],
        )

        # XP for game
        xp_result = _award_xp(request.user.id, "game_complete")
        _increment_progress(request.user.id, games_played=1)
        total = session.correct_answers + session.incorrect_answers
        if total > 0 and (session.correct_answers / total) >= 0.8:
            _award_xp(request.user.id, "game_good")

        new_badges = _check_badges(request.user.id)

        response_data = GameSessionSerializer(session).data
        if xp_result:
            response_data["xp_earned"] = xp_result
        if new_badges:
            response_data["new_badges"] = [{"code": b.code, "name": b.name, "icon": b.icon} for b in new_badges]

        return Response(
            build_success_response(
                data=response_data,
                message="Word context game completed!",
            )
        )


class GameHistoryView(APIView):
    """GET /api/v1/games/history/ — Game history."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))

        use_case = get_game_history_use_case()
        sessions, total = use_case.execute(
            user_id=request.user.id, page=page, page_size=page_size,
        )

        data = GameSessionSerializer(sessions, many=True).data
        meta = {
            "page": page,
            "page_size": page_size,
            "total_count": total,
            "total_pages": (total + page_size - 1) // page_size,
        }

        return Response(build_success_response(data=data, meta=meta))


class GameStatsView(APIView):
    """GET /api/v1/games/stats/ — Game statistics."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        use_case = get_game_stats_use_case()
        stats = use_case.execute(user_id=request.user.id)

        return Response(build_success_response(data=stats))
