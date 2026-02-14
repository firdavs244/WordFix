"""
Integration tests for chat use cases.
Covers: StartChatUseCase, SendChatMessageUseCase, EndChatUseCase,
        GetChatHistoryUseCase, GetChatSessionDetailUseCase
"""

from unittest.mock import MagicMock

import pytest

from apps.words.application.use_cases.chat import (
    EndChatUseCase,
    GetChatHistoryUseCase,
    GetChatSessionDetailUseCase,
    SendChatMessageUseCase,
    StartChatUseCase,
)
from apps.words.infrastructure.repositories.chat_repo import DjangoChatRepository
from apps.words.infrastructure.repositories.word_repo import DjangoWordRepository


@pytest.fixture
def chat_repo():
    return DjangoChatRepository()


@pytest.fixture
def word_repo():
    return DjangoWordRepository()


@pytest.fixture
def mock_user_repo(user):
    repo = MagicMock()
    repo.get_user_language_info.return_value = {
        "native_language": "uz",
        "proficiency_level": "B1",
    }
    return repo


@pytest.mark.django_db
class TestStartChatUseCase:
    def test_start_without_ai(self, user, sample_words, chat_repo, word_repo, mock_user_repo):
        uc = StartChatUseCase(
            chat_repo=chat_repo,
            word_repo=word_repo,
            ai_provider=None,
            user_repo=mock_user_repo,
            prompt_template="{proficiency_level} {native_language} {topic} {words_list}",
            language_map={"uz": "Uzbek"},
        )
        result = uc.execute(user.id, topic="travel")
        assert "session_id" in result
        assert result["topic"] == "travel"
        assert "first_message" in result

    def test_start_with_ai_mock(self, user, sample_words, chat_repo, word_repo, mock_user_repo):
        mock_ai = MagicMock()
        mock_ai.generate_chat.return_value = '{"message": "Hello! Let\'s talk about travel!"}'
        uc = StartChatUseCase(
            chat_repo=chat_repo,
            word_repo=word_repo,
            ai_provider=mock_ai,
            user_repo=mock_user_repo,
            prompt_template="{proficiency_level} {native_language} {topic} {words_list}",
            language_map={"uz": "Uzbek"},
        )
        result = uc.execute(user.id, topic="travel")
        assert "session_id" in result
        mock_ai.generate_chat.assert_called_once()

    def test_start_ai_failure_uses_fallback(self, user, sample_words, chat_repo, word_repo, mock_user_repo):
        mock_ai = MagicMock()
        mock_ai.generate_chat.side_effect = Exception("AI error")
        uc = StartChatUseCase(
            chat_repo=chat_repo,
            word_repo=word_repo,
            ai_provider=mock_ai,
            user_repo=mock_user_repo,
            prompt_template="{proficiency_level} {native_language} {topic} {words_list}",
            language_map={"uz": "Uzbek"},
        )
        result = uc.execute(user.id, topic="travel")
        assert "session_id" in result
        assert "first_message" in result

    def test_start_random_topic(self, user, sample_words, chat_repo, word_repo, mock_user_repo):
        uc = StartChatUseCase(
            chat_repo=chat_repo,
            word_repo=word_repo,
            ai_provider=None,
            user_repo=mock_user_repo,
            prompt_template="{proficiency_level} {native_language} {topic} {words_list}",
            language_map={},
        )
        result = uc.execute(user.id, topic=None)
        assert "topic" in result
        assert result["topic"] != ""


@pytest.mark.django_db
class TestSendChatMessageUseCase:
    def _start_chat(self, user, chat_repo, word_repo, mock_user_repo):
        uc = StartChatUseCase(
            chat_repo=chat_repo,
            word_repo=word_repo,
            ai_provider=None,
            user_repo=mock_user_repo,
            prompt_template="{proficiency_level} {native_language} {topic} {words_list}",
            language_map={"uz": "Uzbek"},
        )
        return uc.execute(user.id, topic="travel")

    def test_send_message_without_ai(self, user, sample_words, chat_repo, word_repo, mock_user_repo):
        from apps.words.domain.services import SpacedRepetitionService

        chat_data = self._start_chat(user, chat_repo, word_repo, mock_user_repo)
        uc = SendChatMessageUseCase(
            chat_repo=chat_repo,
            ai_provider=None,
            word_repo=word_repo,
            user_repo=mock_user_repo,
            sr_service=SpacedRepetitionService(),
            prompt_template="{proficiency_level} {native_language} {topic} {words_list}",
            language_map={"uz": "Uzbek"},
        )
        result = uc.execute(
            session_id=chat_data["session_id"],
            user_id=user.id,
            message_text="I like traveling!",
        )
        assert "ai_message" in result
        assert result["ai_message"]  # Should have default reply

    def test_send_message_with_ai(self, user, sample_words, chat_repo, word_repo, mock_user_repo):
        from apps.words.domain.services import SpacedRepetitionService

        chat_data = self._start_chat(user, chat_repo, word_repo, mock_user_repo)
        mock_ai = MagicMock()
        mock_ai.generate_chat.return_value = '{"message": "Great response!", "corrections": [], "words_used_by_student": []}'
        uc = SendChatMessageUseCase(
            chat_repo=chat_repo,
            ai_provider=mock_ai,
            word_repo=word_repo,
            user_repo=mock_user_repo,
            sr_service=SpacedRepetitionService(),
            prompt_template="{proficiency_level} {native_language} {topic} {words_list}",
            language_map={"uz": "Uzbek"},
        )
        result = uc.execute(
            session_id=chat_data["session_id"],
            user_id=user.id,
            message_text="I like traveling!",
        )
        assert result["ai_message"] == "Great response!"


@pytest.mark.django_db
class TestEndChatUseCase:
    def test_end_chat(self, user, sample_words, chat_repo, word_repo, mock_user_repo):
        start_uc = StartChatUseCase(
            chat_repo=chat_repo,
            word_repo=word_repo,
            ai_provider=None,
            user_repo=mock_user_repo,
            prompt_template="{proficiency_level} {native_language} {topic} {words_list}",
            language_map={},
        )
        chat_data = start_uc.execute(user.id, topic="travel")
        uc = EndChatUseCase(chat_repo=chat_repo)
        result = uc.execute(chat_data["session_id"], user.id)
        assert result["session_id"] == chat_data["session_id"]
        assert result["topic"] == "travel"


@pytest.mark.django_db
class TestGetChatHistoryUseCase:
    def test_get_history(self, user, chat_repo):
        uc = GetChatHistoryUseCase(chat_repo=chat_repo)
        sessions, total = uc.execute(user.id)
        assert isinstance(sessions, list)


@pytest.mark.django_db
class TestGetChatSessionDetailUseCase:
    def test_get_detail(self, user, sample_words, chat_repo, word_repo, mock_user_repo):
        start_uc = StartChatUseCase(
            chat_repo=chat_repo,
            word_repo=word_repo,
            ai_provider=None,
            user_repo=mock_user_repo,
            prompt_template="{proficiency_level} {native_language} {topic} {words_list}",
            language_map={},
        )
        chat_data = start_uc.execute(user.id, topic="travel")
        uc = GetChatSessionDetailUseCase(chat_repo=chat_repo)
        result = uc.execute(chat_data["session_id"], user.id)
        assert "session" in result
        assert "messages" in result
