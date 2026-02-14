"""
URL routes for adaptive-intelligence endpoints.
"""

from django.urls import path

from apps.users.presentation.learning_views import (
    AdaptiveDifficultyView,
    AnalyzeLearningProfileView,
    DomainCoverageView,
    LearningProfileView,
    MistakePatternsView,
    WordRecommendationsView,
)

app_name = "learning"

urlpatterns = [
    path("", LearningProfileView.as_view(), name="profile"),
    path("analyze/", AnalyzeLearningProfileView.as_view(), name="analyze"),
    path("mistake-patterns/", MistakePatternsView.as_view(), name="mistake-patterns"),
    path("recommendations/", WordRecommendationsView.as_view(), name="recommendations"),
    path("domain-coverage/", DomainCoverageView.as_view(), name="domain-coverage"),
    path("difficulty/", AdaptiveDifficultyView.as_view(), name="difficulty"),
]
