"""
Immersive game URL patterns.
"""

from django.urls import path

from .views.immersive_views import (
    ScenarioDetailView,
    ScenarioListView,
    SessionCompleteView,
    SessionDetailView,
    SessionHintView,
    SessionHistoryView,
    SessionRespondView,
    SessionRespondVoiceView,
    SessionStartView,
)

urlpatterns = [
    # Scenarios
    path("scenarios/", ScenarioListView.as_view(), name="immersive-scenario-list"),
    path("scenarios/<uuid:scenario_id>/", ScenarioDetailView.as_view(), name="immersive-scenario-detail"),

    # Sessions
    path("sessions/start/", SessionStartView.as_view(), name="immersive-session-start"),
    path("sessions/history/", SessionHistoryView.as_view(), name="immersive-session-history"),
    path("sessions/<uuid:session_id>/", SessionDetailView.as_view(), name="immersive-session-detail"),
    path("sessions/<uuid:session_id>/respond/", SessionRespondView.as_view(), name="immersive-session-respond"),
    path("sessions/<uuid:session_id>/respond-voice/", SessionRespondVoiceView.as_view(), name="immersive-session-respond-voice"),
    path("sessions/<uuid:session_id>/complete/", SessionCompleteView.as_view(), name="immersive-session-complete"),
    path("sessions/<uuid:session_id>/hint/", SessionHintView.as_view(), name="immersive-session-hint"),
]
