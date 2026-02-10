"""
Challenge URL routing.
"""

from django.urls import path

from .views import (
    ClaimDailyBonusView,
    DailyChallengesView,
)

app_name = "challenges"

urlpatterns = [
    path("today/", DailyChallengesView.as_view(), name="challenges-today"),
    path("claim/", ClaimDailyBonusView.as_view(), name="challenges-claim"),
]
