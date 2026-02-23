"""
Common app URL configuration.

System-level endpoints: health checks, config status.
"""

from django.urls import path

from .views import AIPingView, AIStatusView, ConfigStatusView, DetailedHealthCheckView

app_name = "common"

urlpatterns = [
    path("health/detailed/", DetailedHealthCheckView.as_view(), name="health-detailed"),
    path("config/status/", ConfigStatusView.as_view(), name="config-status"),
    path("ai-status/", AIStatusView.as_view(), name="ai-status"),
    path("ai-ping/", AIPingView.as_view(), name="ai-ping"),
]
