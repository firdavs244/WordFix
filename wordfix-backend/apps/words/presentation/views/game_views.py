"""
Game views — speed round, word match, word context, story builder,
listening challenge, synonym & antonym, irregular verbs.
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
    get_story_builder_start_use_case,
    get_story_builder_submit_use_case,
    get_story_builder_complete_use_case,
    get_listening_start_use_case,
    get_listening_answer_use_case,
    get_listening_complete_use_case,
    get_synonym_antonym_start_use_case,
    get_synonym_antonym_answer_use_case,
    get_synonym_antonym_complete_use_case,
    get_irregular_verbs_start_use_case,
    get_irregular_verbs_answer_use_case,
    get_irregular_verbs_complete_use_case,
)
from ..serializers import (
    GameSessionSerializer,
    GameStatsSerializer,
    SpeedRoundSubmitSerializer,
    WordContextSubmitSerializer,
    WordMatchSubmitSerializer,
    StoryBuilderStartSerializer,
    StoryRoundSubmitSerializer,
    StoryBuilderCompleteSerializer,
    ListeningAnswerSerializer,
    ListeningCompleteSerializer,
    SynonymAntonymAnswerSerializer,
    SynonymAntonymCompleteSerializer,
    IrregularVerbsStartSerializer,
    IrregularVerbAnswerSerializer,
    IrregularVerbsCompleteSerializer,
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


# =============================================================================
# Story Builder Views
# =============================================================================


class StoryBuilderStartView(APIView):
    """POST /api/v1/games/story-builder/start/ — Start Story Builder."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = StoryBuilderStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_story_builder_start_use_case()
        result = use_case.execute(
            user_id=request.user.id,
            genre=serializer.validated_data.get("genre", ""),
        )

        _increment_progress(request.user.id, games_played=1)

        return Response(
            build_success_response(data=result, message="Story Builder started!"),
            status=status.HTTP_201_CREATED,
        )


class StoryBuilderSubmitView(APIView):
    """POST /api/v1/games/story-builder/submit/ — Submit story round."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = StoryRoundSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_story_builder_submit_use_case()
        result = use_case.execute(
            session_id=serializer.validated_data["session_id"],
            user_id=request.user.id,
            user_text=serializer.validated_data["user_text"],
        )

        return Response(
            build_success_response(data=result, message="Round submitted!"),
        )


class StoryBuilderCompleteView(APIView):
    """POST /api/v1/games/story-builder/complete/ — Complete Story Builder."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = StoryBuilderCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_story_builder_complete_use_case()
        result = use_case.execute(
            session_id=serializer.validated_data["session_id"],
            user_id=request.user.id,
        )

        new_badges = _check_badges(request.user.id)
        if new_badges:
            result["new_badges"] = [
                {"code": b.code, "name": b.name, "icon": b.icon}
                for b in new_badges
            ]

        return Response(
            build_success_response(data=result, message="Story Builder completed!"),
        )


# =============================================================================
# Listening Challenge Views
# =============================================================================


class ListeningStartView(APIView):
    """POST /api/v1/games/listening/start/ — Start Listening Challenge."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        use_case = get_listening_start_use_case()
        result = use_case.execute(user_id=request.user.id)

        _increment_progress(request.user.id, games_played=1)

        return Response(
            build_success_response(data=result, message="Listening Challenge started!"),
            status=status.HTTP_201_CREATED,
        )


class ListeningAnswerView(APIView):
    """POST /api/v1/games/listening/answer/ — Submit listening answer."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = ListeningAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_listening_answer_use_case()
        result = use_case.execute(
            session_id=serializer.validated_data["session_id"],
            user_id=request.user.id,
            round_number=serializer.validated_data["round_number"],
            answer=serializer.validated_data["answer"],
        )

        return Response(
            build_success_response(data=result, message="Answer submitted!"),
        )


class ListeningCompleteView(APIView):
    """POST /api/v1/games/listening/complete/ — Complete Listening Challenge."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = ListeningCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_listening_complete_use_case()
        result = use_case.execute(
            session_id=serializer.validated_data["session_id"],
            user_id=request.user.id,
        )

        new_badges = _check_badges(request.user.id)
        if new_badges:
            result["new_badges"] = [
                {"code": b.code, "name": b.name, "icon": b.icon}
                for b in new_badges
            ]

        return Response(
            build_success_response(data=result, message="Listening Challenge completed!"),
        )


# =============================================================================
# Synonym & Antonym Views
# =============================================================================


class SynonymAntonymStartView(APIView):
    """POST /api/v1/games/synonym-antonym/start/ — Start Synonym & Antonym game."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        use_case = get_synonym_antonym_start_use_case()
        result = use_case.execute(user_id=request.user.id)

        _increment_progress(request.user.id, games_played=1)

        return Response(
            build_success_response(data=result, message="Synonym & Antonym game started!"),
            status=status.HTTP_201_CREATED,
        )


class SynonymAntonymAnswerView(APIView):
    """POST /api/v1/games/synonym-antonym/answer/ — Submit SA answer."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = SynonymAntonymAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_synonym_antonym_answer_use_case()
        result = use_case.execute(
            session_id=serializer.validated_data["session_id"],
            user_id=request.user.id,
            round_number=serializer.validated_data["round_number"],
            answer=serializer.validated_data["answer"],
        )

        return Response(
            build_success_response(data=result, message="Answer submitted!"),
        )


class SynonymAntonymCompleteView(APIView):
    """POST /api/v1/games/synonym-antonym/complete/ — Complete SA game."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = SynonymAntonymCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_synonym_antonym_complete_use_case()
        result = use_case.execute(
            session_id=serializer.validated_data["session_id"],
            user_id=request.user.id,
        )

        new_badges = _check_badges(request.user.id)
        if new_badges:
            result["new_badges"] = [
                {"code": b.code, "name": b.name, "icon": b.icon}
                for b in new_badges
            ]

        return Response(
            build_success_response(data=result, message="Synonym & Antonym completed!"),
        )


# =============================================================================
# Irregular Verbs Views
# =============================================================================


class IrregularVerbsStartView(APIView):
    """POST /api/v1/games/irregular-verbs/start/ — Start Irregular Verbs game."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = IrregularVerbsStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_irregular_verbs_start_use_case()
        result = use_case.execute(
            user_id=request.user.id,
            word_count=serializer.validated_data.get("word_count", 10),
            tier=serializer.validated_data.get("tier", ""),
        )

        _increment_progress(request.user.id, games_played=1)

        return Response(
            build_success_response(data=result, message="Irregular Verbs game started!"),
            status=status.HTTP_201_CREATED,
        )


class IrregularVerbsAnswerView(APIView):
    """POST /api/v1/games/irregular-verbs/answer/ — Submit IV answer."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = IrregularVerbAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_irregular_verbs_answer_use_case()
        result = use_case.execute(
            session_id=serializer.validated_data["session_id"],
            user_id=request.user.id,
            round_number=serializer.validated_data["round_number"],
            past_simple=serializer.validated_data["past_simple"],
            past_participle=serializer.validated_data["past_participle"],
        )

        return Response(
            build_success_response(data=result, message="Answer submitted!"),
        )


class IrregularVerbsCompleteView(APIView):
    """POST /api/v1/games/irregular-verbs/complete/ — Complete IV game."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = IrregularVerbsCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_irregular_verbs_complete_use_case()
        result = use_case.execute(
            session_id=serializer.validated_data["session_id"],
            user_id=request.user.id,
        )

        new_badges = _check_badges(request.user.id)
        if new_badges:
            result["new_badges"] = [
                {"code": b.code, "name": b.name, "icon": b.icon}
                for b in new_badges
            ]

        return Response(
            build_success_response(data=result, message="Irregular Verbs completed!"),
        )
