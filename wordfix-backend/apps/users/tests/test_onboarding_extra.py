"""
Additional onboarding tests for coverage — edge cases in service and use cases.
"""

from unittest.mock import patch, MagicMock

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.domain.services.onboarding_service import OnboardingService
from apps.users.infrastructure.models import (
    CustomUser,
    UserProgress,
    OnboardingQuestion,
    OnboardingResult,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    u = CustomUser.objects.create_user(
        email="onbextra@example.com",
        username="onbextra",
        password="testpass123",
    )
    UserProgress.objects.create(user=u)
    return u


@pytest.fixture
def auth_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return api_client


@pytest.fixture
def seed_questions(db):
    questions = []
    for level in ["A1", "A2", "B1", "B2", "C1", "C2"]:
        for order in range(1, 4):
            q = OnboardingQuestion.objects.create(
                level=level,
                question_text=f"{level} Q{order}?",
                correct_answer="correct",
                options=["correct", "wrong1", "wrong2", "wrong3"],
                order=order,
            )
            questions.append(q)
    return questions


class TestOnboardingServiceEdgeCases:
    """Edge cases for OnboardingService.calculate_level()."""

    def test_empty_answers_returns_a1(self):
        service = OnboardingService()
        assert service.calculate_level([]) == "A1"

    def test_all_wrong_returns_a1(self):
        service = OnboardingService()
        answers = [
            {"question_id": 1, "answer": "x", "is_correct": False, "level": "A1"},
            {"question_id": 2, "answer": "x", "is_correct": False, "level": "A1"},
            {"question_id": 3, "answer": "x", "is_correct": False, "level": "A1"},
        ]
        assert service.calculate_level(answers) == "A1"

    def test_pass_a1_only(self):
        service = OnboardingService()
        answers = [
            {"question_id": 1, "answer": "a", "is_correct": True, "level": "A1"},
            {"question_id": 2, "answer": "a", "is_correct": True, "level": "A1"},
            {"question_id": 3, "answer": "a", "is_correct": False, "level": "A1"},
            {"question_id": 4, "answer": "a", "is_correct": False, "level": "A2"},
            {"question_id": 5, "answer": "a", "is_correct": False, "level": "A2"},
            {"question_id": 6, "answer": "a", "is_correct": False, "level": "A2"},
        ]
        assert service.calculate_level(answers) == "A1"

    def test_pass_through_b2(self):
        service = OnboardingService()
        answers = []
        for level in ["A1", "A2", "B1", "B2"]:
            for i in range(3):
                answers.append({
                    "question_id": i,
                    "answer": "a",
                    "is_correct": True,
                    "level": level,
                })
        # Fail C1
        for i in range(3):
            answers.append({
                "question_id": i + 100,
                "answer": "a",
                "is_correct": False,
                "level": "C1",
            })
        assert service.calculate_level(answers) == "B2"

    def test_pass_all_levels_returns_c2(self):
        service = OnboardingService()
        answers = []
        for level in ["A1", "A2", "B1", "B2", "C1", "C2"]:
            for i in range(3):
                answers.append({
                    "question_id": i,
                    "answer": "a",
                    "is_correct": True,
                    "level": level,
                })
        assert service.calculate_level(answers) == "C2"

    def test_missing_level_in_answer_defaults_a1(self):
        service = OnboardingService()
        answers = [
            {"question_id": 1, "answer": "a", "is_correct": True},
            {"question_id": 2, "answer": "a", "is_correct": True},
            {"question_id": 3, "answer": "a", "is_correct": True},
        ]
        result = service.calculate_level(answers)
        assert result == "A1"

    def test_total_zero_at_level_breaks(self):
        """If a level has 0 total questions, it's treated as not passed."""
        service = OnboardingService()
        answers = [
            {"question_id": 1, "answer": "a", "is_correct": True, "level": "A1"},
            {"question_id": 2, "answer": "a", "is_correct": True, "level": "A1"},
            {"question_id": 3, "answer": "a", "is_correct": True, "level": "A1"},
            # Skip A2 entirely → B1 questions should not be checked
            {"question_id": 4, "answer": "a", "is_correct": True, "level": "B1"},
        ]
        # A2 has no questions → breaks there, returns A1
        assert service.calculate_level(answers) == "A1"


class TestOnboardingSubmitEdgeCases:
    """Edge cases for onboarding submit endpoint."""

    def test_submit_already_completed(self, auth_client, user, seed_questions):
        """Second submit returns error (duplicate)."""
        user.has_completed_onboarding = True
        user.save()

        OnboardingResult.objects.create(
            user=user,
            answers=[],
            determined_level="A1",
            total_correct=0,
            total_questions=0,
        )

        response = auth_client.post(
            "/api/v1/auth/onboarding/submit/",
            {"answers": [{"question_id": str(seed_questions[0].id), "answer": "correct"}]},
            format="json",
        )
        assert response.status_code == 400

    def test_status_endpoint_not_completed(self, auth_client, user, seed_questions):
        """Status shows has_completed_onboarding=False for new user."""
        response = auth_client.get("/api/v1/auth/onboarding/status/")
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["has_completed_onboarding"] is False

    def test_status_endpoint_completed(self, auth_client, user, seed_questions):
        """Status shows result after completing."""
        user.has_completed_onboarding = True
        user.proficiency_level = "B1"
        user.save()

        OnboardingResult.objects.create(
            user=user,
            answers=[],
            determined_level="B1",
            total_correct=6,
            total_questions=9,
        )

        response = auth_client.get("/api/v1/auth/onboarding/status/")
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["has_completed_onboarding"] is True
        assert data["determined_level"] == "B1"
