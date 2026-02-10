"""
Word views — core word CRUD and category management.
"""

import logging
import math
from dataclasses import asdict

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.helpers import build_success_response
from apps.users.domain.services import XP_REWARDS
from ..dependencies import (
    get_add_word_use_case,
    get_bulk_add_words_use_case,
    get_category_repository,
    get_delete_word_use_case,
    get_word_detail_use_case,
    get_word_repository,
    get_word_stats_use_case,
    get_words_use_case,
    get_update_word_use_case,
)
from ..serializers import (
    BulkWordCreateSerializer,
    WordCategorySerializer,
    WordCreateSerializer,
    WordUpdateSerializer,
)


logger = logging.getLogger(__name__)


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

        # Update daily challenge progress
        try:
            from apps.words.presentation.dependencies.challenge_deps import get_challenge_repository
            from apps.words.application.use_cases.daily_challenges import UpdateChallengeProgressUseCase
            challenge_repo = get_challenge_repository()
            challenge_uc = UpdateChallengeProgressUseCase(challenge_repo)
            challenge_uc.execute(request.user.id, "add_words", amount=1)
        except Exception as e:
            logger.warning(f"Challenge progress on word add failed: {e}")

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
