"""Test API URL configuration."""

from django.urls import path

from .views import (
    TestGenerateView,
    TestSessionDetailView,
    TestSubmitAnswerView,
    TestCompleteView,
    TestHistoryView,
)

app_name = "tests"

urlpatterns = [
    path("generate/", TestGenerateView.as_view(), name="test-generate"),
    path("history/", TestHistoryView.as_view(), name="test-history"),
    path("<uuid:session_id>/", TestSessionDetailView.as_view(), name="test-detail"),
    path("<uuid:session_id>/answer/", TestSubmitAnswerView.as_view(), name="test-answer"),
    path("<uuid:session_id>/complete/", TestCompleteView.as_view(), name="test-complete"),
]
