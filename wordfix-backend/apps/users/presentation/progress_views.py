"""
Progress, Badge, and Notification API views.
"""

import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.helpers import build_success_response, build_error_response
from .progress_dependencies import (
    get_xp_service,
    get_badge_service,
    get_notification_service,
)

logger = logging.getLogger(__name__)


# =============================================================================
# XP & PROGRESS VIEWS
# =============================================================================


class UserProgressView(APIView):
    """GET /api/v1/users/progress/ — Get user's level, XP, and stats."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        xp_service = get_xp_service()
        level_info = xp_service.get_level_info(request.user.id)
        return Response(
            build_success_response(data=level_info, message="Progress retrieved."),
            status=status.HTTP_200_OK,
        )


class XPHistoryView(APIView):
    """GET /api/v1/users/xp-history/ — Get XP history for last 7 days."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        days = int(request.query_params.get("days", 7))
        xp_service = get_xp_service()
        history = xp_service.get_xp_history(request.user.id, days=days)
        return Response(
            build_success_response(data=history, message="XP history retrieved."),
            status=status.HTTP_200_OK,
        )


# =============================================================================
# BADGE VIEWS
# =============================================================================


class UserBadgesView(APIView):
    """GET /api/v1/users/badges/ — Get user's badges + available badges."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        badge_service = get_badge_service()
        badges = badge_service.get_available_badges(request.user.id)
        earned_count = sum(1 for b in badges if b["is_earned"])
        return Response(
            build_success_response(
                data={
                    "badges": badges,
                    "earned_count": earned_count,
                    "total_count": len(badges),
                },
                message="Badges retrieved.",
            ),
            status=status.HTTP_200_OK,
        )


class AllBadgesView(APIView):
    """GET /api/v1/badges/ — Get all available badges."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        badge_service = get_badge_service()
        badges = badge_service.get_available_badges(request.user.id)
        return Response(
            build_success_response(data=badges, message="All badges retrieved."),
            status=status.HTTP_200_OK,
        )


# =============================================================================
# NOTIFICATION VIEWS
# =============================================================================


class NotificationListView(APIView):
    """GET /api/v1/notifications/ — Get paginated notifications."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))
        notification_service = get_notification_service()
        notifications, total = notification_service.get_notifications(
            request.user.id, page=page, page_size=page_size,
        )
        unread_count = notification_service.get_unread_count(request.user.id)
        total_pages = (total + page_size - 1) // page_size

        return Response(
            build_success_response(
                data={
                    "notifications": [
                        {
                            "id": str(n.id),
                            "type": n.type,
                            "title": n.title,
                            "message": n.message,
                            "is_read": n.is_read,
                            "data": n.data,
                            "created_at": n.created_at.isoformat() if n.created_at else None,
                        }
                        for n in notifications
                    ],
                    "unread_count": unread_count,
                },
                message="Notifications retrieved.",
                meta={
                    "page": page,
                    "page_size": page_size,
                    "total_count": total,
                    "total_pages": total_pages,
                },
            ),
            status=status.HTTP_200_OK,
        )


class NotificationMarkReadView(APIView):
    """POST /api/v1/notifications/read/ — Mark notification(s) as read."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        notification_service = get_notification_service()

        if request.data.get("all"):
            count = notification_service.mark_all_as_read(request.user.id)
            return Response(
                build_success_response(
                    data={"marked_count": count},
                    message="All notifications marked as read.",
                ),
                status=status.HTTP_200_OK,
            )

        notification_id = request.data.get("notification_id")
        if not notification_id:
            return Response(
                build_error_response(message="notification_id or all=true is required."),
                status=status.HTTP_400_BAD_REQUEST,
            )

        success = notification_service.mark_as_read(notification_id, request.user.id)
        if not success:
            return Response(
                build_error_response(message="Notification not found."),
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            build_success_response(message="Notification marked as read."),
            status=status.HTTP_200_OK,
        )


class NotificationUnreadCountView(APIView):
    """GET /api/v1/notifications/unread-count/ — Get unread notification count."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        notification_service = get_notification_service()
        count = notification_service.get_unread_count(request.user.id)
        return Response(
            build_success_response(data={"count": count}, message="Unread count retrieved."),
            status=status.HTTP_200_OK,
        )
