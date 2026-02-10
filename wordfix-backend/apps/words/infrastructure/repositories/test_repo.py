"""
Test session & question repository implementations using Django ORM.
"""

from uuid import UUID

from apps.common.exceptions import EntityNotFoundError
from apps.words.domain.entities import (
    TestQuestionEntity,
    TestSessionEntity,
)
from apps.words.domain.repositories import (
    AbstractTestQuestionRepository,
    AbstractTestSessionRepository,
)
from apps.words.infrastructure.models import (
    TestQuestion,
    TestSession,
)


class DjangoTestSessionRepository(AbstractTestSessionRepository):
    """Concrete implementation for TestSession."""

    def _to_entity(self, session: TestSession) -> TestSessionEntity:
        return TestSessionEntity(
            id=session.id,
            user_id=session.user_id,
            test_type=session.test_type,
            difficulty=session.difficulty,
            total_questions=session.total_questions,
            correct_answers=session.correct_answers,
            incorrect_answers=session.incorrect_answers,
            score_percentage=session.score_percentage,
            started_at=session.started_at,
            completed_at=session.completed_at,
            duration_seconds=session.duration_seconds,
            is_completed=session.is_completed,
            current_combo=session.current_combo,
            max_combo=session.max_combo,
            combo_xp_bonus=session.combo_xp_bonus,
            is_active=session.is_active,
            created_at=session.created_at,
            updated_at=session.updated_at,
        )

    def create(self, user_id: UUID, **kwargs) -> TestSessionEntity:
        session = TestSession.objects.create(user_id=user_id, **kwargs)
        return self._to_entity(session)

    def get_by_id(self, session_id: UUID, user_id: UUID) -> TestSessionEntity:
        try:
            session = TestSession.objects.get(id=session_id, user_id=user_id)
            return self._to_entity(session)
        except TestSession.DoesNotExist:
            raise EntityNotFoundError("Test session not found.")

    def update(self, session_id: UUID, **kwargs) -> TestSessionEntity:
        try:
            session = TestSession.objects.get(id=session_id)
        except TestSession.DoesNotExist:
            raise EntityNotFoundError("Test session not found.")
        for field, value in kwargs.items():
            setattr(session, field, value)
        session.save()
        return self._to_entity(session)

    def get_by_user(
        self, user_id: UUID, page: int = 1, page_size: int = 20
    ) -> tuple[list[TestSessionEntity], int]:
        qs = TestSession.objects.filter(user_id=user_id).order_by("-started_at")
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        sessions = [self._to_entity(s) for s in qs[start:end]]
        return sessions, total


class DjangoTestQuestionRepository(AbstractTestQuestionRepository):
    """Concrete implementation for TestQuestion."""

    def _to_entity(self, q: TestQuestion) -> TestQuestionEntity:
        return TestQuestionEntity(
            id=q.id,
            session_id=q.session_id,
            word_id=q.word_id,
            question_type=q.question_type,
            question_text=q.question_text,
            correct_answer=q.correct_answer,
            options=q.options,
            user_answer=q.user_answer,
            is_correct=q.is_correct,
            response_time_ms=q.response_time_ms,
            explanation=q.explanation,
            order=q.order,
            is_active=q.is_active,
            created_at=q.created_at,
            updated_at=q.updated_at,
        )

    def create(self, **kwargs) -> TestQuestionEntity:
        q = TestQuestion.objects.create(**kwargs)
        return self._to_entity(q)

    def bulk_create(self, questions_data: list[dict]) -> list[TestQuestionEntity]:
        questions = [TestQuestion(**data) for data in questions_data]
        created = TestQuestion.objects.bulk_create(questions)
        return [self._to_entity(q) for q in created]

    def get_by_id(self, question_id: UUID) -> TestQuestionEntity:
        try:
            q = TestQuestion.objects.get(id=question_id)
            return self._to_entity(q)
        except TestQuestion.DoesNotExist:
            raise EntityNotFoundError("Test question not found.")

    def get_by_session(self, session_id: UUID) -> list[TestQuestionEntity]:
        qs = TestQuestion.objects.filter(session_id=session_id).order_by("order")
        return [self._to_entity(q) for q in qs]

    def update(self, question_id: UUID, **kwargs) -> TestQuestionEntity:
        try:
            q = TestQuestion.objects.get(id=question_id)
        except TestQuestion.DoesNotExist:
            raise EntityNotFoundError("Test question not found.")
        for field, value in kwargs.items():
            setattr(q, field, value)
        q.save()
        return self._to_entity(q)
