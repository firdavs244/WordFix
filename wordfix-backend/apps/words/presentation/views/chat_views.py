"""
Chat views — AI conversation practice.
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.helpers import build_success_response
from ..dependencies import (
    get_chat_history_use_case,
    get_chat_session_detail_use_case,
    get_end_chat_use_case,
    get_send_chat_message_use_case,
    get_start_chat_use_case,
)
from .word_views import (
    _award_xp,
)


class ChatStartView(APIView):
    """POST /api/v1/chat/start/ — Start a new chat session."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        from ..serializers import StartChatSerializer

        serializer = StartChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_start_chat_use_case()
        result = use_case.execute(
            user_id=request.user.id,
            topic=serializer.validated_data.get("topic") or None,
        )

        return Response(
            build_success_response(data=result, message="Chat started."),
            status=status.HTTP_201_CREATED,
        )


class ChatSendMessageView(APIView):
    """POST /api/v1/chat/sessions/{id}/message/ — Send a message."""

    permission_classes = [IsAuthenticated]

    def post(self, request, session_id) -> Response:
        from ..serializers import ChatMessageSerializer

        serializer = ChatMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_send_chat_message_use_case()
        result = use_case.execute(
            session_id=session_id,
            user_id=request.user.id,
            message_text=serializer.validated_data["message"],
        )

        # Award XP if words were used
        if result.get("xp_earned", 0) > 0:
            xp_result = _award_xp(request.user.id, "review_correct",
                                  "Used target word in chat")
            result["xp_result"] = xp_result

        return Response(build_success_response(data=result))


class ChatEndView(APIView):
    """POST /api/v1/chat/sessions/{id}/end/ — End a chat session."""

    permission_classes = [IsAuthenticated]

    def post(self, request, session_id) -> Response:
        use_case = get_end_chat_use_case()
        result = use_case.execute(
            session_id=session_id,
            user_id=request.user.id,
        )

        return Response(build_success_response(data=result, message="Chat ended."))


class ChatHistoryView(APIView):
    """GET /api/v1/chat/history/ — List past chat sessions."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))

        use_case = get_chat_history_use_case()
        sessions, total = use_case.execute(
            user_id=request.user.id,
            page=page,
            page_size=page_size,
        )

        sessions_data = []
        for s in sessions:
            sessions_data.append({
                "id": str(s.id),
                "topic": s.topic,
                "message_count": s.message_count,
                "target_words": s.target_words,
                "is_active": s.is_active,
                "started_at": s.started_at.isoformat() if s.started_at else None,
                "ended_at": s.ended_at.isoformat() if s.ended_at else None,
                "created_at": s.created_at.isoformat() if s.created_at else None,
            })

        meta = {
            "page": page,
            "page_size": page_size,
            "total_count": total,
            "total_pages": (total + page_size - 1) // page_size,
        }

        return Response(build_success_response(data=sessions_data, meta=meta))


class ChatSessionDetailView(APIView):
    """GET /api/v1/chat/sessions/{id}/ — Get chat session with messages."""

    permission_classes = [IsAuthenticated]

    def get(self, request, session_id) -> Response:
        use_case = get_chat_session_detail_use_case()
        result = use_case.execute(
            session_id=session_id,
            user_id=request.user.id,
        )

        session = result["session"]
        messages = result["messages"]

        data = {
            "session": {
                "id": str(session.id),
                "topic": session.topic,
                "message_count": session.message_count,
                "target_words": session.target_words,
                "words_practiced": session.words_practiced,
                "is_active": session.is_active,
                "started_at": session.started_at.isoformat() if session.started_at else None,
                "ended_at": session.ended_at.isoformat() if session.ended_at else None,
            },
            "messages": [
                {
                    "id": str(m.id),
                    "role": m.role,
                    "content": m.content,
                    "corrections": m.corrections,
                    "words_used": m.words_used,
                    "order": m.order,
                    "created_at": m.created_at.isoformat() if m.created_at else None,
                }
                for m in messages
            ],
        }

        return Response(build_success_response(data=data))
