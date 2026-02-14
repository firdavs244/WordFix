"""
Integration tests for testing use cases.
Covers: GenerateTestUseCase (AI + fallback), SubmitTestAnswerUseCase,
        CompleteTestSessionUseCase, GetTestHistoryUseCase, GetTestDetailUseCase
"""

from unittest.mock import MagicMock

import pytest

from apps.words.application.use_cases.testing import (
    CompleteTestSessionUseCase,
    GenerateTestUseCase,
    GetTestDetailUseCase,
    GetTestHistoryUseCase,
    SubmitTestAnswerUseCase,
)
from apps.words.infrastructure.repositories.test_repo import (
    DjangoTestQuestionRepository,
    DjangoTestSessionRepository,
)
from apps.words.infrastructure.repositories.word_repo import DjangoWordRepository


@pytest.fixture
def word_repo():
    return DjangoWordRepository()


@pytest.fixture
def session_repo():
    return DjangoTestSessionRepository()


@pytest.fixture
def question_repo():
    return DjangoTestQuestionRepository()


@pytest.mark.django_db
class TestGenerateTestUseCaseFallback:
    """Test the fallback path when AI is not available."""

    def test_generate_multiple_choice_fallback(self, user, sample_words, word_repo, session_repo, question_repo):
        uc = GenerateTestUseCase(
            word_repo=word_repo,
            test_session_repo=session_repo,
            test_question_repo=question_repo,
            ai_provider=None,
            prompt_templates={},
            language_map={},
        )
        result = uc.execute(
            user_id=user.id,
            test_type="multiple_choice",
            difficulty="adaptive",
            question_count=5,
        )
        assert "session" in result
        assert "questions" in result
        assert len(result["questions"]) == 5

    def test_generate_fill_blank_fallback(self, user, sample_words, word_repo, session_repo, question_repo):
        uc = GenerateTestUseCase(
            word_repo=word_repo,
            test_session_repo=session_repo,
            test_question_repo=question_repo,
            ai_provider=None,
            prompt_templates={},
            language_map={},
        )
        result = uc.execute(
            user_id=user.id,
            test_type="fill_blank",
            difficulty="adaptive",
            question_count=5,
        )
        assert "session" in result
        assert len(result["questions"]) == 5

    def test_generate_context_guess_fallback(self, user, sample_words, word_repo, session_repo, question_repo):
        uc = GenerateTestUseCase(
            word_repo=word_repo,
            test_session_repo=session_repo,
            test_question_repo=question_repo,
            ai_provider=None,
            prompt_templates={},
            language_map={},
        )
        result = uc.execute(
            user_id=user.id,
            test_type="context_guess",
            difficulty="adaptive",
            question_count=5,
        )
        assert "session" in result
        assert len(result["questions"]) == 5

    def test_generate_with_difficulty_easy(self, user, sample_words, word_repo, session_repo, question_repo):
        uc = GenerateTestUseCase(
            word_repo=word_repo,
            test_session_repo=session_repo,
            test_question_repo=question_repo,
            ai_provider=None,
            prompt_templates={},
            language_map={},
        )
        result = uc.execute(
            user_id=user.id,
            test_type="multiple_choice",
            difficulty="easy",
            question_count=5,
        )
        assert len(result["questions"]) == 5

    def test_generate_with_difficulty_hard(self, user, sample_words, word_repo, session_repo, question_repo):
        uc = GenerateTestUseCase(
            word_repo=word_repo,
            test_session_repo=session_repo,
            test_question_repo=question_repo,
            ai_provider=None,
            prompt_templates={},
            language_map={},
        )
        result = uc.execute(
            user_id=user.id,
            test_type="multiple_choice",
            difficulty="hard",
            question_count=5,
        )
        assert len(result["questions"]) == 5

    def test_generate_not_enough_words_raises(self, user, word_repo, session_repo, question_repo):
        from apps.common.exceptions import ValidationError

        uc = GenerateTestUseCase(
            word_repo=word_repo,
            test_session_repo=session_repo,
            test_question_repo=question_repo,
            ai_provider=None,
            prompt_templates={},
            language_map={},
        )
        with pytest.raises(ValidationError):
            uc.execute(
                user_id=user.id,
                test_type="multiple_choice",
                difficulty="adaptive",
                question_count=5,
            )


@pytest.mark.django_db
class TestGenerateTestUseCaseAI:
    """Test the AI path."""

    def test_generate_with_ai(self, user, sample_words, word_repo, session_repo, question_repo):
        mock_ai = MagicMock()
        mock_ai.is_available.return_value = True
        mock_ai.generate_json.return_value = {
            "questions": [
                {
                    "word": sample_words[i].original_word,
                    "question": f"What does '{sample_words[i].original_word}' mean?",
                    "correct_answer": sample_words[i].translation,
                    "options": [sample_words[i].translation, "a", "b", "c"],
                    "explanation": "test explanation",
                }
                for i in range(5)
            ]
        }
        uc = GenerateTestUseCase(
            word_repo=word_repo,
            test_session_repo=session_repo,
            test_question_repo=question_repo,
            ai_provider=mock_ai,
            prompt_templates={"multiple_choice": "{native_language} {proficiency_level} {count} {words_list}"},
            language_map={"uz": "Uzbek"},
        )
        result = uc.execute(
            user_id=user.id,
            test_type="multiple_choice",
            difficulty="adaptive",
            question_count=5,
        )
        assert len(result["questions"]) == 5
        mock_ai.generate_json.assert_called_once()

    def test_ai_failure_falls_back(self, user, sample_words, word_repo, session_repo, question_repo):
        mock_ai = MagicMock()
        mock_ai.is_available.return_value = True
        mock_ai.generate_json.side_effect = Exception("API Error")
        uc = GenerateTestUseCase(
            word_repo=word_repo,
            test_session_repo=session_repo,
            test_question_repo=question_repo,
            ai_provider=mock_ai,
            prompt_templates={"multiple_choice": "{native_language} {proficiency_level} {count} {words_list}"},
            language_map={},
        )
        result = uc.execute(
            user_id=user.id,
            test_type="multiple_choice",
            difficulty="adaptive",
            question_count=5,
        )
        assert len(result["questions"]) == 5


@pytest.mark.django_db
class TestSubmitTestAnswerUseCase:
    def _create_test(self, user, sample_words, word_repo, session_repo, question_repo):
        uc = GenerateTestUseCase(
            word_repo=word_repo,
            test_session_repo=session_repo,
            test_question_repo=question_repo,
            ai_provider=None,
            prompt_templates={},
            language_map={},
        )
        return uc.execute(
            user_id=user.id,
            test_type="multiple_choice",
            difficulty="adaptive",
            question_count=5,
        )

    def test_submit_correct_answer(self, user, sample_words, word_repo, session_repo, question_repo):
        from apps.words.domain.services import SpacedRepetitionService

        test_data = self._create_test(user, sample_words, word_repo, session_repo, question_repo)
        question = test_data["questions"][0]
        activity_repo = MagicMock()
        activity_repo.get_or_create_today.return_value = MagicMock(
            id="test", words_reviewed=0, correct_answers=0, incorrect_answers=0, xp_earned=0
        )

        uc = SubmitTestAnswerUseCase(
            question_repo=question_repo,
            word_repo=word_repo,
            sr_service=SpacedRepetitionService(),
            activity_repo=activity_repo,
        )
        result = uc.execute(
            question_id=question.id,
            user_id=user.id,
            answer=question.correct_answer,
        )
        assert result["is_correct"] is True

    def test_submit_wrong_answer(self, user, sample_words, word_repo, session_repo, question_repo):
        from apps.words.domain.services import SpacedRepetitionService

        test_data = self._create_test(user, sample_words, word_repo, session_repo, question_repo)
        question = test_data["questions"][0]
        activity_repo = MagicMock()

        uc = SubmitTestAnswerUseCase(
            question_repo=question_repo,
            word_repo=word_repo,
            sr_service=SpacedRepetitionService(),
            activity_repo=activity_repo,
        )
        result = uc.execute(
            question_id=question.id,
            user_id=user.id,
            answer="totally_wrong_answer",
        )
        assert result["is_correct"] is False
        assert "correct_answer" in result


@pytest.mark.django_db
class TestCompleteTestSessionUseCase:
    def test_complete_session(self, user, sample_words, word_repo, session_repo, question_repo):
        gen_uc = GenerateTestUseCase(
            word_repo=word_repo,
            test_session_repo=session_repo,
            test_question_repo=question_repo,
            ai_provider=None,
            prompt_templates={},
            language_map={},
        )
        test_data = gen_uc.execute(
            user_id=user.id,
            test_type="multiple_choice",
            difficulty="adaptive",
            question_count=5,
        )

        activity_repo = MagicMock()
        activity_repo.get_or_create_today.return_value = MagicMock(
            id="test", words_reviewed=0, correct_answers=0, incorrect_answers=0, xp_earned=0
        )

        uc = CompleteTestSessionUseCase(
            test_session_repo=session_repo,
            test_question_repo=question_repo,
            activity_repo=activity_repo,
        )
        result = uc.execute(
            session_id=test_data["session"].id,
            user_id=user.id,
        )
        assert result.is_completed is True


@pytest.mark.django_db
class TestGetTestHistoryUseCase:
    def test_get_history(self, user, session_repo):
        uc = GetTestHistoryUseCase(test_session_repo=session_repo)
        sessions, total = uc.execute(user.id)
        assert isinstance(sessions, list)


@pytest.mark.django_db
class TestGetTestDetailUseCase:
    def test_get_detail(self, user, sample_words, word_repo, session_repo, question_repo):
        gen_uc = GenerateTestUseCase(
            word_repo=word_repo,
            test_session_repo=session_repo,
            test_question_repo=question_repo,
            ai_provider=None,
            prompt_templates={},
            language_map={},
        )
        test_data = gen_uc.execute(
            user_id=user.id,
            test_type="multiple_choice",
            difficulty="adaptive",
            question_count=5,
        )
        uc = GetTestDetailUseCase(
            test_session_repo=session_repo,
            test_question_repo=question_repo,
        )
        result = uc.execute(
            session_id=test_data["session"].id,
            user_id=user.id,
        )
        assert "session" in result
        assert "questions" in result
