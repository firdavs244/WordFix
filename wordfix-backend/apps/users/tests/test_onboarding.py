"""
Tests for onboarding level test.
"""

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.domain.services.onboarding_service import OnboardingService
from apps.users.infrastructure.models import (
    CustomUser,
    OnboardingQuestion,
    OnboardingResult,
    UserProgress,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    u = CustomUser.objects.create_user(
        email="onboard@example.com",
        username="onboarduser",
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
    """Seed 18 onboarding questions (3 per level)."""
    from apps.users.management.commands.seed_onboarding_questions import QUESTIONS

    created = []
    for q in QUESTIONS:
        obj = OnboardingQuestion.objects.create(**q)
        created.append(obj)
    return created


def _make_answers(questions, correct_levels):
    """Helper to make answers — correct for given levels, wrong for others."""
    answers = []
    for q in questions:
        if q.level in correct_levels:
            answers.append({"question_id": str(q.id), "answer": q.correct_answer})
        else:
            # Pick wrong answer
            wrong = [o for o in q.options if o != q.correct_answer]
            answers.append({"question_id": str(q.id), "answer": wrong[0] if wrong else "wrong"})
    return answers


class TestOnboardingService:
    """Domain service unit tests."""

    def test_calculate_level_all_correct(self):
        svc = OnboardingService()
        answers = []
        for level in ["A1", "A2", "B1", "B2", "C1", "C2"]:
            for _ in range(3):
                answers.append({"level": level, "is_correct": True})
        assert svc.calculate_level(answers) == "C2"

    def test_calculate_level_a1_only(self):
        svc = OnboardingService()
        answers = [
            {"level": "A1", "is_correct": True},
            {"level": "A1", "is_correct": True},
            {"level": "A1", "is_correct": True},
            {"level": "A2", "is_correct": False},
            {"level": "A2", "is_correct": False},
            {"level": "A2", "is_correct": False},
        ]
        assert svc.calculate_level(answers) == "A1"

    def test_calculate_level_b1(self):
        svc = OnboardingService()
        answers = []
        for level in ["A1", "A2", "B1"]:
            for _ in range(3):
                answers.append({"level": level, "is_correct": True})
        for _ in range(3):
            answers.append({"level": "B2", "is_correct": False})
        assert svc.calculate_level(answers) == "B1"

    def test_calculate_level_empty(self):
        svc = OnboardingService()
        assert svc.calculate_level([]) == "A1"

    def test_calculate_level_adaptive(self):
        """Various answer combos testing adaptive logic."""
        svc = OnboardingService()
        # A1: 2/3, A2: 2/3, B1: 1/3 → A2
        answers = [
            {"level": "A1", "is_correct": True},
            {"level": "A1", "is_correct": True},
            {"level": "A1", "is_correct": False},
            {"level": "A2", "is_correct": True},
            {"level": "A2", "is_correct": False},
            {"level": "A2", "is_correct": True},
            {"level": "B1", "is_correct": True},
            {"level": "B1", "is_correct": False},
            {"level": "B1", "is_correct": False},
        ]
        assert svc.calculate_level(answers) == "A2"


class TestOnboarding:
    """Integration tests for onboarding endpoints."""

    def test_get_questions(self, auth_client, seed_questions):
        """18 questions returned, no correct_answer."""
        response = auth_client.get("/api/v1/auth/onboarding/questions/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        questions = data["data"]["questions"]
        assert len(questions) == 18

    def test_questions_no_correct_answer(self, auth_client, seed_questions):
        """correct_answer should NOT be in the response."""
        response = auth_client.get("/api/v1/auth/onboarding/questions/")
        questions = response.json()["data"]["questions"]
        for q in questions:
            assert "correct_answer" not in q

    def test_submit_all_correct(self, auth_client, user, seed_questions):
        """All correct → C2."""
        answers = _make_answers(seed_questions, ["A1", "A2", "B1", "B2", "C1", "C2"])
        response = auth_client.post(
            "/api/v1/auth/onboarding/submit/",
            {"answers": answers},
            format="json",
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["determined_level"] == "C2"

    def test_submit_a1_only(self, auth_client, user, seed_questions):
        """Only A1 correct → A1."""
        answers = _make_answers(seed_questions, ["A1"])
        response = auth_client.post(
            "/api/v1/auth/onboarding/submit/",
            {"answers": answers},
            format="json",
        )
        assert response.status_code == 200
        assert response.json()["data"]["determined_level"] == "A1"

    def test_submit_b1_level(self, auth_client, user, seed_questions):
        """A1+A2+B1 correct, B2 wrong → B1."""
        answers = _make_answers(seed_questions, ["A1", "A2", "B1"])
        response = auth_client.post(
            "/api/v1/auth/onboarding/submit/",
            {"answers": answers},
            format="json",
        )
        assert response.status_code == 200
        assert response.json()["data"]["determined_level"] == "B1"

    def test_submit_updates_user_level(self, auth_client, user, seed_questions):
        """proficiency_level updated in DB."""
        answers = _make_answers(seed_questions, ["A1", "A2"])
        auth_client.post(
            "/api/v1/auth/onboarding/submit/",
            {"answers": answers},
            format="json",
        )
        user.refresh_from_db()
        assert user.proficiency_level == "A2"

    def test_submit_creates_result(self, auth_client, user, seed_questions):
        """OnboardingResult created."""
        answers = _make_answers(seed_questions, ["A1"])
        auth_client.post(
            "/api/v1/auth/onboarding/submit/",
            {"answers": answers},
            format="json",
        )
        assert OnboardingResult.objects.filter(user=user).exists()

    def test_submit_gives_xp(self, auth_client, user, seed_questions):
        """XP awarded after onboarding."""
        answers = _make_answers(seed_questions, ["A1"])
        auth_client.post(
            "/api/v1/auth/onboarding/submit/",
            {"answers": answers},
            format="json",
        )
        progress = UserProgress.objects.get(user=user)
        assert progress.total_xp >= 50

    def test_submit_sets_onboarding_completed(self, auth_client, user, seed_questions):
        """has_completed_onboarding = True."""
        answers = _make_answers(seed_questions, ["A1"])
        auth_client.post(
            "/api/v1/auth/onboarding/submit/",
            {"answers": answers},
            format="json",
        )
        user.refresh_from_db()
        assert user.has_completed_onboarding is True

    def test_skip_onboarding(self, auth_client, user, seed_questions):
        """Skip keeps A1, sets flag True."""
        response = auth_client.post("/api/v1/auth/onboarding/skip/")
        assert response.status_code == 200
        user.refresh_from_db()
        assert user.proficiency_level == "A1"
        assert user.has_completed_onboarding is True

    def test_status_not_completed(self, auth_client, user):
        """Status before onboarding."""
        response = auth_client.get("/api/v1/auth/onboarding/status/")
        assert response.status_code == 200
        assert response.json()["data"]["completed"] is False

    def test_status_completed(self, auth_client, user, seed_questions):
        """Status after onboarding."""
        answers = _make_answers(seed_questions, ["A1"])
        auth_client.post(
            "/api/v1/auth/onboarding/submit/",
            {"answers": answers},
            format="json",
        )
        response = auth_client.get("/api/v1/auth/onboarding/status/")
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["completed"] is True
        assert data["determined_level"] == "A1"

    def test_double_submit(self, auth_client, user, seed_questions):
        """Second submit returns 400."""
        answers = _make_answers(seed_questions, ["A1"])
        auth_client.post(
            "/api/v1/auth/onboarding/submit/",
            {"answers": answers},
            format="json",
        )
        response = auth_client.post(
            "/api/v1/auth/onboarding/submit/",
            {"answers": answers},
            format="json",
        )
        assert response.status_code == 400
