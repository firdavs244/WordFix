"""
Immersive game views — scenarios, sessions, conversation, hints.
"""

from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.helpers import build_success_response

from ..dependencies.immersive_deps import (
    get_complete_session_use_case,
    get_list_scenarios_use_case,
    get_request_hint_use_case,
    get_scenario_detail_use_case,
    get_start_session_use_case,
    get_submit_response_use_case,
    get_submit_voice_response_use_case,
)
from ..serializers.immersive_serializers import (
    ScenarioFilterSerializer,
    StartSessionSerializer,
    SubmitResponseSerializer,
)


# ─── Scenarios ───────────────────────────────────────────────────────────────

class ScenarioListView(APIView):
    """GET /api/v1/immersive/scenarios/ — List immersive scenarios."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        filters = ScenarioFilterSerializer(data=request.query_params)
        filters.is_valid(raise_exception=True)
        use_case = get_list_scenarios_use_case()
        result = use_case.execute(
            difficulty=filters.validated_data.get("difficulty"),
            location=filters.validated_data.get("location"),
        )
        return Response(build_success_response(data=result, message="Scenarios retrieved."))


class ScenarioDetailView(APIView):
    """GET /api/v1/immersive/scenarios/<id>/ — Get scenario detail."""

    permission_classes = [IsAuthenticated]

    def get(self, request, scenario_id) -> Response:
        use_case = get_scenario_detail_use_case()
        result = use_case.execute(scenario_id=scenario_id)
        return Response(build_success_response(data=result, message="Scenario detail retrieved."))


# ─── Sessions ────────────────────────────────────────────────────────────────

class SessionStartView(APIView):
    """POST /api/v1/immersive/sessions/start/ — Start immersive session."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = StartSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case = get_start_session_use_case()
        result = use_case.execute(
            user_id=request.user.id,
            scenario_id=serializer.validated_data["scenario_id"],
            npc_id=serializer.validated_data.get("npc_id"),
            input_mode=serializer.validated_data.get("input_mode", "text"),
        )
        return Response(
            build_success_response(data=result, message="Immersive session started!"),
            status=status.HTTP_201_CREATED,
        )


class SessionRespondView(APIView):
    """POST /api/v1/immersive/sessions/<id>/respond/ — Submit text response."""

    permission_classes = [IsAuthenticated]

    def post(self, request, session_id) -> Response:
        serializer = SubmitResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case = get_submit_response_use_case()
        result = use_case.execute(
            session_id=session_id,
            user_id=request.user.id,
            user_message=serializer.validated_data["message"],
            response_time_ms=serializer.validated_data.get("response_time_ms"),
        )
        return Response(build_success_response(data=result, message="Response submitted."))


class SessionRespondVoiceView(APIView):
    """POST /api/v1/immersive/sessions/<id>/respond-voice/ — Submit voice response."""

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, session_id) -> Response:
        audio_file = request.FILES.get("audio")
        if not audio_file:
            return Response(
                {"success": False, "message": "No audio file provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        language = request.data.get("language", "en")
        response_time_ms = request.data.get("response_time_ms")
        if response_time_ms:
            response_time_ms = int(response_time_ms)

        use_case = get_submit_voice_response_use_case()
        result = use_case.execute(
            session_id=session_id,
            user_id=request.user.id,
            audio_data=audio_file.read(),
            filename=audio_file.name or "audio.webm",
            language=language,
            response_time_ms=response_time_ms,
        )
        return Response(build_success_response(data=result, message="Voice response submitted."))


class SessionCompleteView(APIView):
    """POST /api/v1/immersive/sessions/<id>/complete/ — Complete session."""

    permission_classes = [IsAuthenticated]

    def post(self, request, session_id) -> Response:
        use_case = get_complete_session_use_case()
        result = use_case.execute(session_id=session_id, user_id=request.user.id)
        return Response(build_success_response(data=result, message="Session completed!"))


class SessionDetailView(APIView):
    """GET /api/v1/immersive/sessions/<id>/ — Get session with turns."""

    permission_classes = [IsAuthenticated]

    def get(self, request, session_id) -> Response:
        from apps.immersive.infrastructure.repositories.session_repo import DjangoSessionRepository
        repo = DjangoSessionRepository()
        session = repo.get_by_id(session_id, request.user.id)
        turns = repo.get_turns(session_id)
        return Response(build_success_response(data={
            "id": str(session.id),
            "status": session.status,
            "score": session.score,
            "turn_count": session.turn_count,
            "hints_used": session.hints_used,
            "fluency_score": session.fluency_score,
            "accuracy_score": session.accuracy_score,
            "vocabulary_score": session.vocabulary_score,
            "task_completion_score": session.task_completion_score,
            "xp_earned": session.xp_earned,
            "duration_seconds": session.duration_seconds,
            "turns": [
                {
                    "turn_number": t.turn_number,
                    "role": t.role,
                    "content": t.content,
                    "audio_url": t.audio_url,
                    "input_type": t.input_type,
                    "grammar_errors": t.grammar_errors,
                    "vocabulary_feedback": t.vocabulary_feedback,
                    "score": t.score,
                    "hint_level_used": t.hint_level_used,
                }
                for t in turns
            ],
        }, message="Session detail retrieved."))


class SessionHistoryView(APIView):
    """GET /api/v1/immersive/sessions/history/ — User history."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        page = int(request.query_params.get("page", 1))
        from apps.immersive.infrastructure.repositories.session_repo import DjangoSessionRepository
        repo = DjangoSessionRepository()
        sessions, total = repo.get_history(request.user.id, page=page)
        return Response(build_success_response(
            data=[
                {
                    "id": str(s.id),
                    "status": s.status,
                    "score": s.score,
                    "turn_count": s.turn_count,
                    "xp_earned": s.xp_earned,
                    "duration_seconds": s.duration_seconds,
                    "started_at": s.started_at.isoformat() if s.started_at else None,
                }
                for s in sessions
            ],
            message="Session history retrieved.",
            meta={"total": total, "page": page},
        ))


# ─── Hints ───────────────────────────────────────────────────────────────────

class SessionHintView(APIView):
    """POST /api/v1/immersive/sessions/<id>/hint/ — Request hint."""

    permission_classes = [IsAuthenticated]

    def post(self, request, session_id) -> Response:
        use_case = get_request_hint_use_case()
        result = use_case.execute(session_id=session_id, user_id=request.user.id)
        return Response(build_success_response(data=result, message="Hint generated."))
