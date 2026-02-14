"""
Profile and onboarding use cases.
"""

from uuid import UUID

from apps.common.exceptions import ValidationError
from apps.users.domain.repositories import AbstractUserRepository


class GetUserProfileUseCase:
    """Get user profile by ID."""

    def __init__(self, repository: AbstractUserRepository):
        self.repository = repository

    def execute(self, user_id: UUID):
        """Returns UserEntity."""
        return self.repository.get_by_id(user_id)


class UpdateUserProfileUseCase:
    """Update user profile."""

    ALLOWED_FIELDS = {
        "full_name",
        "native_language",
        "learning_language",
        "proficiency_level",
        "daily_goal",
        "timezone",
    }

    def __init__(self, repository: AbstractUserRepository):
        self.repository = repository

    def execute(self, user_id: UUID, data: dict):
        """Update allowed profile fields. Returns updated UserEntity."""
        filtered = {k: v for k, v in data.items() if k in self.ALLOWED_FIELDS}
        if not filtered:
            return self.repository.get_by_id(user_id)
        return self.repository.update(user_id, **filtered)


class ChangePasswordUseCase:
    """Change user password."""

    def __init__(self, repository: AbstractUserRepository):
        self.repository = repository

    def execute(self, user_id: UUID, old_password: str, new_password: str) -> bool:
        """Verify old password and set new one. Returns True on success."""
        if not self.repository.check_password(user_id, old_password):
            raise ValidationError("Current password is incorrect.")

        self.repository.set_password(user_id, new_password)
        return True


class GetOnboardingQuestionsUseCase:
    """Get all onboarding questions."""

    def __init__(self, question_queryset_fn):
        self.question_queryset_fn = question_queryset_fn

    def execute(self) -> list[dict]:
        """Return all questions grouped by level (without correct_answer)."""
        questions = self.question_queryset_fn()
        return [
            {
                "id": str(q.id),
                "level": q.level,
                "question_text": q.question_text,
                "options": q.options,
                "order": q.order,
            }
            for q in questions
        ]


class SubmitOnboardingResultUseCase:
    """Submit onboarding test answers and determine level."""

    def __init__(self, repository, onboarding_service, xp_service=None):
        self.repository = repository
        self.onboarding_service = onboarding_service
        self.xp_service = xp_service

    def execute(self, user_id: UUID, answers: list[dict]) -> dict:
        """
        1. Check answers against correct answers
        2. Calculate level
        3. Update user proficiency_level
        4. Save OnboardingResult
        5. Award XP
        """
        from apps.users.infrastructure.models import (
            CustomUser,
            OnboardingQuestion,
            OnboardingResult,
        )

        user = CustomUser.objects.get(id=user_id)

        # Check if already completed
        if OnboardingResult.objects.filter(user=user).exists():
            raise ValidationError("Onboarding test already completed.")

        # Verify answers
        checked_answers = []
        total_correct = 0
        for ans in answers:
            question_id = ans.get("question_id")
            user_answer = ans.get("answer", "")
            try:
                question = OnboardingQuestion.objects.get(id=question_id)
                is_correct = user_answer.strip().lower() == question.correct_answer.strip().lower()
                if is_correct:
                    total_correct += 1
                checked_answers.append({
                    "question_id": str(question.id),
                    "answer": user_answer,
                    "is_correct": is_correct,
                    "level": question.level,
                })
            except OnboardingQuestion.DoesNotExist:
                continue

        # Calculate level
        determined_level = self.onboarding_service.calculate_level(checked_answers)

        # Save result
        OnboardingResult.objects.create(
            user=user,
            answers=checked_answers,
            determined_level=determined_level,
            total_correct=total_correct,
            total_questions=len(checked_answers),
        )

        # Update user
        user.proficiency_level = determined_level
        user.has_completed_onboarding = True
        user.save(update_fields=["proficiency_level", "has_completed_onboarding"])

        # Award XP
        if self.xp_service:
            try:
                self.xp_service.award_xp(
                    user_id=user_id,
                    amount=50,
                    reason="daily_goal",
                    description="Completed onboarding test",
                )
            except Exception:
                pass

        return {
            "determined_level": determined_level,
            "total_correct": total_correct,
            "total_questions": len(checked_answers),
            "message": f"Your level has been set to {determined_level}.",
        }


class SkipOnboardingUseCase:
    """Skip onboarding — keep default A1."""

    def execute(self, user_id: UUID) -> dict:
        from apps.users.infrastructure.models import CustomUser, OnboardingResult

        user = CustomUser.objects.get(id=user_id)

        # Idempotent: if already completed, return existing result
        existing = OnboardingResult.objects.filter(user=user).first()
        if existing:
            return {
                "determined_level": existing.determined_level,
                "total_correct": existing.total_correct,
                "total_questions": existing.total_questions,
                "message": "Onboarding already completed.",
            }

        # Create a skip result
        OnboardingResult.objects.create(
            user=user,
            answers=[],
            determined_level="A1",
            total_correct=0,
            total_questions=0,
        )

        user.has_completed_onboarding = True
        user.save(update_fields=["has_completed_onboarding"])

        return {
            "determined_level": "A1",
            "total_correct": 0,
            "total_questions": 0,
            "message": "Onboarding skipped. Your level is set to A1.",
        }
