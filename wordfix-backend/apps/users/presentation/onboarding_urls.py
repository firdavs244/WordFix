"""
Onboarding URL routing.
"""

from django.urls import path

from .onboarding_views import (
    OnboardingQuestionsView,
    OnboardingSubmitView,
    OnboardingSkipView,
    OnboardingStatusView,
)

urlpatterns = [
    path("questions/", OnboardingQuestionsView.as_view(), name="onboarding-questions"),
    path("submit/", OnboardingSubmitView.as_view(), name="onboarding-submit"),
    path("skip/", OnboardingSkipView.as_view(), name="onboarding-skip"),
    path("status/", OnboardingStatusView.as_view(), name="onboarding-status"),
]
