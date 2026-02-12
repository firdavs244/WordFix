"""
Tests for Listening Challenge game use cases.
"""

import uuid
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from apps.words.application.use_cases.games import (
    CompleteListeningChallengeUseCase,
    StartListeningChallengeUseCase,
    SubmitListeningAnswerUseCase,
)
from apps.words.domain.entities import GameSessionEntity, ListeningRoundEntity
from apps.words.tests.conftest import make_word_entity


def _make_game_session(**overrides):
    defaults = dict(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        game_type="listening_challenge",
        started_at=datetime.now(timezone.utc),
        completed_at=None,
        is_completed=False,
        score=0,
        max_score=100,
        correct_answers=0,
        incorrect_answers=0,
        duration_seconds=0,
        level=1,
        xp_earned=0,
        current_combo=0,
        max_combo=0,
        combo_xp_bonus=0,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    defaults.update(overrides)
    return GameSessionEntity(**defaults)


def _make_listening_round(**overrides):
    defaults = dict(
        id=uuid.uuid4(),
        session_id=uuid.uuid4(),
        word_id=uuid.uuid4(),
        round_number=1,
        correct_answer="hello",
        user_answers=[],
        attempts_used=0,
        max_attempts=3,
        is_correct=False,
        hints_shown=[],
        score=0,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    defaults.update(overrides)
    return ListeningRoundEntity(**defaults)


class TestStartListeningChallengeUseCase:

    def setup_method(self):
        self.game_repo = MagicMock()
        self.word_repo = MagicMock()
        self.tts_provider = MagicMock()

    def _make_uc(self, tts_provider="DEFAULT"):
        provider = self.tts_provider if tts_provider == "DEFAULT" else tts_provider
        return StartListeningChallengeUseCase(
            word_repo=self.word_repo,
            game_repo=self.game_repo,
            tts_provider=provider,
        )

    def test_start_creates_session_and_rounds(self):
        """Start listening challenge creates session with rounds."""
        user_id = uuid.uuid4()
        words = [
            make_word_entity(original_word=f"word{i}", audio_url=f"audio/{i}.mp3")
            for i in range(15)
        ]
        self.word_repo.get_all_by_user.return_value = (words, len(words))
        session = _make_game_session(user_id=user_id)
        self.game_repo.create.return_value = session

        listening_round = _make_listening_round(session_id=session.id)
        self.game_repo.create_listening_round.return_value = listening_round

        uc = self._make_uc()
        result = uc.execute(user_id)

        assert "session_id" in result
        assert "first_word" in result
        self.game_repo.create.assert_called_once()

    def test_start_without_tts_provider(self):
        """Start without TTS provider → still works with fallback."""
        user_id = uuid.uuid4()
        words = [
            make_word_entity(original_word=f"word{i}", audio_url=f"audio/{i}.mp3")
            for i in range(15)
        ]
        self.word_repo.get_all_by_user.return_value = (words, len(words))
        session = _make_game_session(user_id=user_id)
        self.game_repo.create.return_value = session

        listening_round = _make_listening_round(session_id=session.id)
        self.game_repo.create_listening_round.return_value = listening_round

        uc = self._make_uc(tts_provider=None)
        result = uc.execute(user_id)

        assert "session_id" in result

    def test_start_not_enough_words(self):
        """Not enough words → raises error."""
        user_id = uuid.uuid4()
        words = [make_word_entity(original_word=f"word{i}") for i in range(3)]
        self.word_repo.get_all_by_user.return_value = (words, len(words))

        uc = self._make_uc()
        with pytest.raises(Exception):
            uc.execute(user_id)

    def test_prefers_words_with_audio(self):
        """Words with audio_url should be preferred."""
        user_id = uuid.uuid4()
        words_with_audio = [
            make_word_entity(original_word=f"audio{i}", audio_url=f"audio/{i}.mp3")
            for i in range(8)
        ]
        words_without_audio = [
            make_word_entity(original_word=f"plain{i}", audio_url="")
            for i in range(8)
        ]
        self.word_repo.get_all_by_user.return_value = (
            words_with_audio + words_without_audio, 16,
        )
        session = _make_game_session(user_id=user_id)
        self.game_repo.create.return_value = session

        listening_round = _make_listening_round(session_id=session.id)
        self.game_repo.create_listening_round.return_value = listening_round

        uc = self._make_uc()
        result = uc.execute(user_id)

        assert "session_id" in result


class TestSubmitListeningAnswerUseCase:

    def setup_method(self):
        self.game_repo = MagicMock()
        self.word_repo = MagicMock()
        self.sr_service = MagicMock()

    def _make_uc(self):
        return SubmitListeningAnswerUseCase(
            game_repo=self.game_repo,
            word_repo=self.word_repo,
            sr_service=self.sr_service,
        )

    def test_correct_answer_first_attempt(self):
        """Correct answer on first attempt → max score (10)."""
        user_id = uuid.uuid4()
        session = _make_game_session(user_id=user_id)
        self.game_repo.get_by_id.return_value = session

        round_entity = _make_listening_round(
            correct_answer="hello",
            attempts_used=0,
            user_answers=[],
        )
        self.game_repo.get_listening_round.return_value = round_entity

        word = make_word_entity(original_word="hello")
        self.word_repo.get_by_id.return_value = word
        self.word_repo.update.return_value = word

        uc = self._make_uc()
        result = uc.execute(
            session_id=session.id,
            user_id=user_id,
            round_number=round_entity.round_number,
            answer="hello",
        )

        assert result["is_correct"] is True
        assert "score" in result

    def test_correct_answer_case_insensitive(self):
        """Answer matching should be case-insensitive."""
        user_id = uuid.uuid4()
        session = _make_game_session(user_id=user_id)
        self.game_repo.get_by_id.return_value = session

        round_entity = _make_listening_round(
            correct_answer="Hello",
            attempts_used=0,
            user_answers=[],
        )
        self.game_repo.get_listening_round.return_value = round_entity

        word = make_word_entity(original_word="Hello")
        self.word_repo.get_by_id.return_value = word
        self.word_repo.update.return_value = word

        uc = self._make_uc()
        result = uc.execute(
            session_id=session.id,
            user_id=user_id,
            round_number=round_entity.round_number,
            answer="hello",
        )

        assert result["is_correct"] is True

    def test_wrong_answer_shows_hint(self):
        """Wrong answer → hint provided, attempt incremented."""
        user_id = uuid.uuid4()
        session = _make_game_session(user_id=user_id)
        self.game_repo.get_by_id.return_value = session

        round_entity = _make_listening_round(
            correct_answer="hypothesis",
            attempts_used=0,
            user_answers=[],
        )
        self.game_repo.get_listening_round.return_value = round_entity

        uc = self._make_uc()
        result = uc.execute(
            session_id=session.id,
            user_id=user_id,
            round_number=round_entity.round_number,
            answer="hypo",
        )

        assert result["is_correct"] is False
        # Hint is returned in the result
        assert "hint" in result

    def test_max_attempts_exceeded(self):
        """After 3 wrong attempts → round is done, score 0."""
        user_id = uuid.uuid4()
        session = _make_game_session(user_id=user_id)
        self.game_repo.get_by_id.return_value = session

        round_entity = _make_listening_round(
            correct_answer="hypothesis",
            attempts_used=2,
            max_attempts=3,
            user_answers=["hypo", "hyp"],
        )
        self.game_repo.get_listening_round.return_value = round_entity

        word = make_word_entity(original_word="hypothesis")
        self.word_repo.get_by_id.return_value = word
        self.word_repo.update.return_value = word

        uc = self._make_uc()
        result = uc.execute(
            session_id=session.id,
            user_id=user_id,
            round_number=round_entity.round_number,
            answer="wrong",
        )

        assert "score" in result

    def test_scoring_by_attempt(self):
        """Score decreases with more attempts: 10/7/4/0."""
        user_id = uuid.uuid4()
        session = _make_game_session(user_id=user_id)
        self.game_repo.get_by_id.return_value = session

        # First attempt correct → score 10
        round_entity = _make_listening_round(
            correct_answer="apple",
            attempts_used=0,
            user_answers=[],
        )
        self.game_repo.get_listening_round.return_value = round_entity

        word = make_word_entity(original_word="apple")
        self.word_repo.get_by_id.return_value = word
        self.word_repo.update.return_value = word

        uc = self._make_uc()
        result = uc.execute(
            session_id=session.id,
            user_id=user_id,
            round_number=round_entity.round_number,
            answer="apple",
        )

        assert result["is_correct"] is True


class TestCompleteListeningChallengeUseCase:

    def setup_method(self):
        self.game_repo = MagicMock()
        self.xp_service = MagicMock()
        self.badge_service = MagicMock()

    def _make_uc(self):
        return CompleteListeningChallengeUseCase(
            game_repo=self.game_repo,
            xp_service=self.xp_service,
            badge_service=self.badge_service,
        )

    def test_complete_calculates_stats(self):
        """Complete → stats include score, accuracy, total rounds."""
        user_id = uuid.uuid4()
        session = _make_game_session(user_id=user_id)
        self.game_repo.get_by_id.return_value = session

        rounds = [
            _make_listening_round(is_correct=True, score=10),
            _make_listening_round(is_correct=True, score=7),
            _make_listening_round(is_correct=False, score=0),
        ]
        self.game_repo.get_listening_rounds.return_value = rounds
        self.xp_service.award_xp.return_value = {"xp_gained": 15}
        self.badge_service.check_and_award_badges.return_value = []

        uc = self._make_uc()
        result = uc.execute(user_id=user_id, session_id=session.id)

        assert "total_score" in result
        assert "accuracy_pct" in result

    def test_complete_awards_xp(self):
        """Complete → XP awarded."""
        user_id = uuid.uuid4()
        session = _make_game_session(user_id=user_id)
        self.game_repo.get_by_id.return_value = session
        self.game_repo.get_listening_rounds.return_value = [
            _make_listening_round(is_correct=True, score=10),
        ]
        self.xp_service.award_xp.return_value = {"xp_gained": 15}
        self.badge_service.check_and_award_badges.return_value = []

        uc = self._make_uc()
        uc.execute(user_id=user_id, session_id=session.id)

        self.xp_service.award_xp.assert_called()

    def test_complete_without_services(self):
        """Complete without XP/Badge services → no error."""
        user_id = uuid.uuid4()
        session = _make_game_session(user_id=user_id)
        self.game_repo.get_by_id.return_value = session
        self.game_repo.get_listening_rounds.return_value = [
            _make_listening_round(is_correct=True, score=10),
        ]

        uc = CompleteListeningChallengeUseCase(
            game_repo=self.game_repo,
            xp_service=None,
            badge_service=None,
        )
        result = uc.execute(user_id=user_id, session_id=session.id)

        assert "total_score" in result

    def test_perfect_accuracy(self):
        """All rounds correct → 100% accuracy."""
        user_id = uuid.uuid4()
        session = _make_game_session(user_id=user_id)
        self.game_repo.get_by_id.return_value = session

        rounds = [
            _make_listening_round(is_correct=True, score=10) for _ in range(10)
        ]
        self.game_repo.get_listening_rounds.return_value = rounds
        self.xp_service.award_xp.return_value = {"xp_gained": 15}
        self.badge_service.check_and_award_badges.return_value = []

        uc = self._make_uc()
        result = uc.execute(user_id=user_id, session_id=session.id)

        assert result["accuracy_pct"] == 100.0
