"""
Chat URL routing.
"""

from django.urls import path

from .views import (
    ChatEndView,
    ChatHistoryView,
    ChatSendMessageView,
    ChatSessionDetailView,
    ChatStartView,
)

app_name = "chat"

urlpatterns = [
    path("start/", ChatStartView.as_view(), name="chat-start"),
    path("history/", ChatHistoryView.as_view(), name="chat-history"),
    path("sessions/<uuid:session_id>/", ChatSessionDetailView.as_view(), name="chat-session-detail"),
    path("sessions/<uuid:session_id>/message/", ChatSendMessageView.as_view(), name="chat-send-message"),
    path("sessions/<uuid:session_id>/end/", ChatEndView.as_view(), name="chat-end"),
]
