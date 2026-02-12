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
    StoryBuilderStartView,
    StoryBuilderSubmitView,
    StoryBuilderCompleteView,
    ListeningStartView,
    ListeningAnswerView,
    ListeningCompleteView,
)

app_name = "games"

urlpatterns = [
    path("speed-round/start/", SpeedRoundStartView.as_view(), name="speed-round-start"),
    path("speed-round/submit/", SpeedRoundSubmitView.as_view(), name="speed-round-submit"),
    path("word-match/start/", WordMatchStartView.as_view(), name="word-match-start"),
    path("word-match/submit/", WordMatchSubmitView.as_view(), name="word-match-submit"),
    path("word-context/start/", WordContextStartView.as_view(), name="word-context-start"),
    path("word-context/submit/", WordContextSubmitView.as_view(), name="word-context-submit"),
    path("story-builder/start/", StoryBuilderStartView.as_view(), name="story-builder-start"),
    path("story-builder/submit/", StoryBuilderSubmitView.as_view(), name="story-builder-submit"),
    path("story-builder/complete/", StoryBuilderCompleteView.as_view(), name="story-builder-complete"),
    path("listening/start/", ListeningStartView.as_view(), name="listening-start"),
    path("listening/answer/", ListeningAnswerView.as_view(), name="listening-answer"),
    path("listening/complete/", ListeningCompleteView.as_view(), name="listening-complete"),
    path("history/", GameHistoryView.as_view(), name="game-history"),
    path("stats/", GameStatsView.as_view(), name="game-stats"),
]
