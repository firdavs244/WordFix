"""
Notification URL routing.
"""

from django.urls import path

from apps.users.presentation.progress_views import (
    NotificationListView,
    NotificationMarkReadView,
    NotificationUnreadCountView,
)

app_name = "notifications"

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    path("read/", NotificationMarkReadView.as_view(), name="notification-read"),
    path("unread-count/", NotificationUnreadCountView.as_view(), name="notification-unread-count"),
]
