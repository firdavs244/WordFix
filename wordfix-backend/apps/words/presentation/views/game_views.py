"""
Game views — speed round, word match, word context games.
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.helpers import build_success_response
from ..dependencies import (
    get_start_speed_round_use_case,
    get_submit_speed_round_use_case,
    get_start_word_match_use_case,
    get_submit_word_match_use_case,
    get_start_word_context_use_case,
    get_submit_word_context_use_case,
    get_game_history_use_case,
    get_game_stats_use_case,
)
from ..serializers import (
    GameSessionSerializer,
    GameStatsSerializer,
    SpeedRoundSubmitSerializer,
    WordContextSubmitSerializer,
    WordMatchSubmitSerializer,
)
from .word_views import (
    _award_xp,
    _check_badges,
    _increment_progress,
)


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
            response_data["xp_earned"] = xp_result.get("xp_gained", response_data.get("xp_earned", 0))
            response_data["xp_details"] = xp_result
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
            response_data["xp_earned"] = xp_result.get("xp_gained", response_data.get("xp_earned", 0))
            response_data["xp_details"] = xp_result
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
            response_data["xp_earned"] = xp_result.get("xp_gained", response_data.get("xp_earned", 0))
            response_data["xp_details"] = xp_result
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
