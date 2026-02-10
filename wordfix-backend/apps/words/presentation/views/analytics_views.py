"""
Analytics views — overview, weekly/monthly trends, difficult words, calendar.
"""

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.helpers import build_success_response
from ..dependencies import (
    get_analytics_overview_use_case,
    get_difficult_words_use_case,
    get_monthly_stats_use_case,
    get_study_calendar_use_case,
    get_weekly_stats_use_case,
    get_word_progress_use_case,
)


class AnalyticsOverviewView(APIView):
    """GET /api/v1/analytics/overview/ — Overall stats."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        use_case = get_analytics_overview_use_case()
        data = use_case.execute(user_id=request.user.id)
        return Response(build_success_response(data=data))


class AnalyticsWeeklyView(APIView):
    """GET /api/v1/analytics/weekly/ — 7-day trend."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        use_case = get_weekly_stats_use_case()
        data = use_case.execute(user_id=request.user.id)
        return Response(build_success_response(data=data))


class AnalyticsMonthlyView(APIView):
    """GET /api/v1/analytics/monthly/ — 30-day trend."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        use_case = get_monthly_stats_use_case()
        data = use_case.execute(user_id=request.user.id)
        return Response(build_success_response(data=data))


class AnalyticsDifficultWordsView(APIView):
    """GET /api/v1/analytics/difficult-words/ — Hardest words."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        limit = int(request.query_params.get("limit", 10))
        use_case = get_difficult_words_use_case()
        data = use_case.execute(user_id=request.user.id, limit=limit)
        return Response(build_success_response(data=data))


class AnalyticsWordProgressView(APIView):
    """GET /api/v1/analytics/word-progress/ — Word progress distribution."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        use_case = get_word_progress_use_case()
        data = use_case.execute(user_id=request.user.id)
        return Response(build_success_response(data=data))


class AnalyticsCalendarView(APIView):
    """GET /api/v1/analytics/calendar/ — Study heatmap calendar."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        from datetime import date as dt_date

        year = int(request.query_params.get("year", dt_date.today().year))
        month = int(request.query_params.get("month", dt_date.today().month))

        use_case = get_study_calendar_use_case()
        data = use_case.execute(user_id=request.user.id, year=year, month=month)
        return Response(build_success_response(data=data))
