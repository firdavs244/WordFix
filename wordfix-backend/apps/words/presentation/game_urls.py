"""Game API URL configuration."""

from django.urls import path

from .views import (
    SpeedRoundStartView,
    SpeedRoundSubmitView,
    WordMatchStartView,
    WordMatchSubmitView,
    WordContextStartView,
    WordContextSubmitView,
    GameHistoryView,
    GameStatsView,
)

app_name = "games"

urlpatterns = [
    path("speed-round/start/", SpeedRoundStartView.as_view(), name="speed-round-start"),
    path("speed-round/submit/", SpeedRoundSubmitView.as_view(), name="speed-round-submit"),
    path("word-match/start/", WordMatchStartView.as_view(), name="word-match-start"),
    path("word-match/submit/", WordMatchSubmitView.as_view(), name="word-match-submit"),
    path("word-context/start/", WordContextStartView.as_view(), name="word-context-start"),
    path("word-context/submit/", WordContextSubmitView.as_view(), name="word-context-submit"),
    path("history/", GameHistoryView.as_view(), name="game-history"),
    path("stats/", GameStatsView.as_view(), name="game-stats"),
]
