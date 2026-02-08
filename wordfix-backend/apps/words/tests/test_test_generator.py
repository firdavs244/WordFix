"""
Tests for AI Test Generator use cases and views.
"""

import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from django.utils import timezone

from apps.words.application.use_cases import (
    CompleteTestSessionUseCase,
    GenerateTestUseCase,
    GetTestDetailUseCase,
    GetTestHistoryUseCase,
    SubmitTestAnswerUseCase,
)
from apps.words.domain.services import SpacedRepetitionService
from apps.words.infrastructure.models import TestQuestion as QModel, TestSession as SModel, Word
from apps.words.tests.conftest import make_word_entity


# =============================================================================
# USE CASE TESTS
# =============================================================================


@pytest.mark.django_db
class TestGenerateTestUseCase:
    """Tests for GenerateTestUseCase."""

    def test_generate_multiple_choice(self, user, sample_words):
        """AI mock → multiple choice questions created."""
        mock_ai = MagicMock()
        mock_ai.is_available.return_value = True
        mock_ai.generate_json.return_value = [
            {
                "word": "apple",
                "question_type": "word_to_translation",
                "question": 'What does "apple" mean?',
                "correct_answer": "olma",
                "options": ["olma", "nok", "uzum", "olcha"],
                "explanation": "Apple means olma.",
            }
            for _ in range(5)
        ]

        from apps.words.infrastructure.repositories import (
            DjangoTestQuestionRepository,
            DjangoTestSessionRepository,
            DjangoWordRepository,
        )

        uc = GenerateTestUseCase(
            word_repo=DjangoWordRepository(),
            test_session_repo=DjangoTestSessionRepository(),
            test_question_repo=DjangoTestQuestionRepository(),
            ai_provider=mock_ai,
            prompt_templates={"multiple_choice": "test {count} {words_list} {native_language} {proficiency_level}"},
        )

        result = uc.execute(
            user_id=user.id,
            test_type="multiple_choice",
            question_count=5,
            difficulty="adaptive",
        )

        assert "session" in result
        assert "questions" in result
        assert result["session"].test_type == "multiple_choice"
        assert len(result["questions"]) == 5

    def test_generate_fill_blank(self, user, sample_words):
        """AI mock → fill blank questions created."""
        mock_ai = MagicMock()
        mock_ai.is_available.return_value = True
        mock_ai.generate_json.return_value = [
            {
                "word": "apple",
                "question_type": "fill_blank",
                "sentence_with_blank": "I ate an ___ today.",
                "correct_answer": "apple",
                "hint": "a fruit",
                "explanation": "Apple is a fruit.",
            }
            for _ in range(5)
        ]

        from apps.words.infrastructure.repositories import (
            DjangoTestQuestionRepository,
            DjangoTestSessionRepository,
            DjangoWordRepository,
        )

        uc = GenerateTestUseCase(
            word_repo=DjangoWordRepository(),
            test_session_repo=DjangoTestSessionRepository(),
            test_question_repo=DjangoTestQuestionRepository(),
            ai_provider=mock_ai,
            prompt_templates={"fill_blank": "test {count} {words_list} {native_language} {proficiency_level}"},
        )

        result = uc.execute(
            user_id=user.id,
            test_type="fill_blank",
            question_count=5,
        )

        assert len(result["questions"]) == 5

    def test_generate_context_guess(self, user, sample_words):
        """AI mock → context guess questions created."""
        mock_ai = MagicMock()
        mock_ai.is_available.return_value = True
        mock_ai.generate_json.return_value = [
            {
                "word": "apple",
                "question_type": "context_guess",
                "context_paragraph": "I like eating ___.",
                "question": "What fits?",
                "correct_answer": "apple",
                "options": ["apple", "car", "book", "chair"],
                "explanation": "Context clue: eating.",
            }
            for _ in range(5)
        ]

        from apps.words.infrastructure.repositories import (
            DjangoTestQuestionRepository,
            DjangoTestSessionRepository,
            DjangoWordRepository,
        )

        uc = GenerateTestUseCase(
            word_repo=DjangoWordRepository(),
            test_session_repo=DjangoTestSessionRepository(),
            test_question_repo=DjangoTestQuestionRepository(),
            ai_provider=mock_ai,
            prompt_templates={"context_guess": "test {count} {words_list} {native_language} {proficiency_level}"},
        )

        result = uc.execute(
            user_id=user.id,
            test_type="context_guess",
            question_count=5,
        )

        assert len(result["questions"]) == 5

    def test_generate_mixed(self, user, sample_words):
        """Mixed type uses multiple choice prompt."""
        mock_ai = MagicMock()
        mock_ai.is_available.return_value = True
        mock_ai.generate_json.return_value = [
            {
                "word": "apple",
                "question_type": "multiple_choice",
                "question": 'What does "apple" mean?',
                "correct_answer": "olma",
                "options": ["olma", "nok", "uzum", "olcha"],
                "explanation": "Apple means olma.",
            }
            for _ in range(5)
        ]

        from apps.words.infrastructure.repositories import (
            DjangoTestQuestionRepository,
            DjangoTestSessionRepository,
            DjangoWordRepository,
        )

        uc = GenerateTestUseCase(
            word_repo=DjangoWordRepository(),
            test_session_repo=DjangoTestSessionRepository(),
            test_question_repo=DjangoTestQuestionRepository(),
            ai_provider=mock_ai,
            prompt_templates={"multiple_choice": "test {count} {words_list} {native_language} {proficiency_level}"},
        )

        result = uc.execute(user_id=user.id, test_type="mixed")
        assert result["session"].test_type == "mixed"

    def test_generate_fallback_no_ai(self, user, sample_words):
        """AI unavailable → fallback test generated."""
        from apps.words.infrastructure.repositories import (
            DjangoTestQuestionRepository,
            DjangoTestSessionRepository,
            DjangoWordRepository,
        )

        uc = GenerateTestUseCase(
            word_repo=DjangoWordRepository(),
            test_session_repo=DjangoTestSessionRepository(),
            test_question_repo=DjangoTestQuestionRepository(),
            ai_provider=None,  # No AI
        )

        result = uc.execute(user_id=user.id, test_type="multiple_choice", question_count=5)

        assert len(result["questions"]) == 5
        assert result["session"].test_type == "multiple_choice"

    def test_generate_not_enough_words(self, user):
        """< 5 words → ValidationError."""
        # Create only 3 words
        for i in range(3):
            Word.objects.create(
                user=user,
                original_word=f"word{i}",
                translation=f"trans{i}",
            )

        from apps.words.infrastructure.repositories import (
            DjangoTestQuestionRepository,
            DjangoTestSessionRepository,
            DjangoWordRepository,
        )

        uc = GenerateTestUseCase(
            word_repo=DjangoWordRepository(),
            test_session_repo=DjangoTestSessionRepository(),
            test_question_repo=DjangoTestQuestionRepository(),
        )

        with pytest.raises(Exception) as exc_info:
            uc.execute(user_id=user.id)
        assert "5 words" in str(exc_info.value)

    def test_adaptive_difficulty(self, user, sample_words):
        """Adaptive difficulty selects mixed confidence words."""
        # Set varied confidence
        words = Word.objects.filter(user=user)
        for i, word in enumerate(words):
            word.confidence_score = i * 20
            word.save()

        from apps.words.infrastructure.repositories import (
            DjangoTestQuestionRepository,
            DjangoTestSessionRepository,
            DjangoWordRepository,
        )

        uc = GenerateTestUseCase(
            word_repo=DjangoWordRepository(),
            test_session_repo=DjangoTestSessionRepository(),
            test_question_repo=DjangoTestQuestionRepository(),
        )

        result = uc.execute(
            user_id=user.id, test_type="multiple_choice",
            question_count=5, difficulty="adaptive",
        )
        assert len(result["questions"]) == 5


@pytest.mark.django_db
class TestSubmitTestAnswerUseCase:
    """Tests for SubmitTestAnswerUseCase."""

    def _create_test_session_with_question(self, user, sample_words):
        """Helper to create a test session with one question."""
        session = SModel.objects.create(
            user=user,
            test_type="multiple_choice",
            total_questions=1,
        )
        word = sample_words[0]
        question = QModel.objects.create(
            session=session,
            word=word,
            question_type="word_to_translation",
            question_text='What does "apple" mean?',
            correct_answer="olma",
            options=["olma", "nok", "uzum", "olcha"],
            explanation="Apple means olma.",
            order=1,
        )
        return session, question, word

    def test_submit_correct_answer(self, user, sample_words):
        """Correct answer → is_correct=True, SR updated."""
        session, question, word = self._create_test_session_with_question(user, sample_words)

        from apps.words.infrastructure.repositories import (
            DjangoDailyActivityRepository,
            DjangoTestQuestionRepository,
            DjangoWordRepository,
        )

        uc = SubmitTestAnswerUseCase(
            question_repo=DjangoTestQuestionRepository(),
            word_repo=DjangoWordRepository(),
            sr_service=SpacedRepetitionService(),
            activity_repo=DjangoDailyActivityRepository(),
        )

        result = uc.execute(
            question_id=question.id,
            user_id=user.id,
            answer="olma",
        )

        assert result["is_correct"] is True
        assert result["correct_answer"] == "olma"

        # Check word was updated
        updated_word = Word.objects.get(id=word.id)
        assert updated_word.review_count == 1
        assert updated_word.correct_count == 1

    def test_submit_incorrect_answer(self, user, sample_words):
        """Incorrect answer → is_correct=False, SR updated."""
        session, question, word = self._create_test_session_with_question(user, sample_words)

        from apps.words.infrastructure.repositories import (
            DjangoDailyActivityRepository,
            DjangoTestQuestionRepository,
            DjangoWordRepository,
        )

        uc = SubmitTestAnswerUseCase(
            question_repo=DjangoTestQuestionRepository(),
            word_repo=DjangoWordRepository(),
            sr_service=SpacedRepetitionService(),
            activity_repo=DjangoDailyActivityRepository(),
        )

        result = uc.execute(
            question_id=question.id,
            user_id=user.id,
            answer="nok",
        )

        assert result["is_correct"] is False

        updated_word = Word.objects.get(id=word.id)
        assert updated_word.review_count == 1
        assert updated_word.incorrect_count == 1


@pytest.mark.django_db
class TestCompleteTestSessionUseCase:
    """Tests for CompleteTestSessionUseCase."""

    def test_complete_session(self, user, sample_words):
        """Score calculation works correctly."""
        session = SModel.objects.create(
            user=user,
            test_type="multiple_choice",
            total_questions=3,
        )
        for i, word in enumerate(sample_words[:3]):
            QModel.objects.create(
                session=session,
                word=word,
                question_type="word_to_translation",
                question_text=f"Q{i}",
                correct_answer="correct",
                user_answer="answer",
                is_correct=(i < 2),  # 2 correct, 1 wrong
                order=i + 1,
            )

        from apps.words.infrastructure.repositories import (
            DjangoDailyActivityRepository,
            DjangoTestQuestionRepository,
            DjangoTestSessionRepository,
        )

        uc = CompleteTestSessionUseCase(
            test_session_repo=DjangoTestSessionRepository(),
            test_question_repo=DjangoTestQuestionRepository(),
            activity_repo=DjangoDailyActivityRepository(),
        )

        result = uc.execute(session_id=session.id, user_id=user.id)

        assert result.is_completed is True
        assert result.correct_answers == 2
        assert result.incorrect_answers == 1
        assert result.score_percentage == pytest.approx(66.7, abs=0.1)


@pytest.mark.django_db
class TestGetTestHistoryUseCase:
    """Tests for GetTestHistoryUseCase."""

    def test_test_history(self, user):
        """Paginated history returns correctly."""
        for _ in range(3):
            SModel.objects.create(
                user=user,
                test_type="multiple_choice",
                is_completed=True,
            )

        from apps.words.infrastructure.repositories import DjangoTestSessionRepository

        uc = GetTestHistoryUseCase(
            test_session_repo=DjangoTestSessionRepository(),
        )

        sessions, total = uc.execute(user_id=user.id, page=1, page_size=10)
        assert total == 3
        assert len(sessions) == 3
