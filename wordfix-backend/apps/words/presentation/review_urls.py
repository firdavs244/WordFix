"""
Review URL routing.
"""

from django.urls import path

from .views import (
    CompleteSessionView,
    DailyProgressView,
    PredictedIntervalsView,
    ReviewHistoryView,
    ReviewSessionCreateView,
    ReviewSessionDetailView,
    ReviewSummaryView,
    ReviewWordsView,
    StreakView,
    SubmitAnswerView,
)

app_name = "review"

urlpatterns = [
    path("words/", ReviewWordsView.as_view(), name="review-words"),
    path("sessions/", ReviewSessionCreateView.as_view(), name="session-create"),
    path("sessions/<uuid:session_id>/", ReviewSessionDetailView.as_view(), name="session-detail"),
    path("sessions/<uuid:session_id>/answer/", SubmitAnswerView.as_view(), name="session-answer"),
    path("sessions/<uuid:session_id>/complete/", CompleteSessionView.as_view(), name="session-complete"),
    path("summary/", ReviewSummaryView.as_view(), name="review-summary"),
    path("history/", ReviewHistoryView.as_view(), name="review-history"),
    path("streak/", StreakView.as_view(), name="streak"),
    path("daily-progress/", DailyProgressView.as_view(), name="daily-progress"),
    path("words/<uuid:word_id>/predict/", PredictedIntervalsView.as_view(), name="predicted-intervals"),
]
