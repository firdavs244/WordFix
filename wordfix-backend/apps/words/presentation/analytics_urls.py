"""
Analytics URL routing.
"""

from django.urls import path

from .views import (
    AnalyticsCalendarView,
    AnalyticsDifficultWordsView,
    AnalyticsMonthlyView,
    AnalyticsOverviewView,
    AnalyticsWeeklyView,
    AnalyticsWordProgressView,
)

app_name = "analytics"

urlpatterns = [
    path("overview/", AnalyticsOverviewView.as_view(), name="analytics-overview"),
    path("weekly/", AnalyticsWeeklyView.as_view(), name="analytics-weekly"),
    path("monthly/", AnalyticsMonthlyView.as_view(), name="analytics-monthly"),
    path("difficult-words/", AnalyticsDifficultWordsView.as_view(), name="analytics-difficult-words"),
    path("word-progress/", AnalyticsWordProgressView.as_view(), name="analytics-word-progress"),
    path("calendar/", AnalyticsCalendarView.as_view(), name="analytics-calendar"),
]
