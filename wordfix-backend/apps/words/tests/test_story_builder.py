"""
Tests for Story Builder game use cases.
"""

import uuid
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from apps.words.application.use_cases.games import (
    CompleteStoryBuilderUseCase,
    StartStoryBuilderUseCase,
    SubmitStoryRoundUseCase,
)
from apps.words.domain.entities import GameSessionEntity, StoryRoundEntity, WordEntity
from apps.words.tests.conftest import make_word_entity


def _make_game_session(**overrides):
    defaults = dict(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        game_type="story_builder",
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


def _make_story_round(**overrides):
    defaults = dict(
        id=uuid.uuid4(),
        session_id=uuid.uuid4(),
        round_number=1,
        ai_text="Once upon a time in a land of apples...",
        user_text="",
        target_words=["apple", "run"],
        words_used=[],
        grammar_corrections=[],
        is_correct_usage=False,
        score=0,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    defaults.update(overrides)
    return StoryRoundEntity(**defaults)


class TestStartStoryBuilderUseCase:

    def setup_method(self):
        self.game_repo = MagicMock()
        self.word_repo = MagicMock()
        self.ai_provider = MagicMock()

    def _make_uc(self, ai_provider="DEFAULT"):
        provider = self.ai_provider if ai_provider == "DEFAULT" else ai_provider
        return StartStoryBuilderUseCase(
            word_repo=self.word_repo,
            game_repo=self.game_repo,
            ai_provider=provider,
        )

    def test_start_with_ai_provider(self):
        """Start story with working AI provider."""
        user_id = uuid.uuid4()
        words = [make_word_entity(confidence_score=30, original_word=f"word{i}") for i in range(10)]
        self.word_repo.get_all_by_user.return_value = (words, len(words))
        session = _make_game_session(user_id=user_id)
        self.game_repo.create.return_value = session
        story_round = _make_story_round(session_id=session.id)
        self.game_repo.create_story_round.return_value = story_round

        self.ai_provider.is_available.return_value = True
        self.ai_provider.generate_json.return_value = {"story_text": "Once upon a time..."}

        uc = self._make_uc()
        result = uc.execute(user_id)

        assert "session_id" in result
        assert "ai_text" in result
        assert "genre" in result
        self.game_repo.create.assert_called_once()

    def test_start_without_ai_uses_fallback(self):
        """Start story without AI falls back to templates."""
        user_id = uuid.uuid4()
        words = [make_word_entity(confidence_score=30, original_word=f"word{i}") for i in range(10)]
        self.word_repo.get_all_by_user.return_value = (words, len(words))
        session = _make_game_session(user_id=user_id)
        self.game_repo.create.return_value = session
        story_round = _make_story_round(session_id=session.id)
        self.game_repo.create_story_round.return_value = story_round

        uc = self._make_uc(ai_provider=None)
        result = uc.execute(user_id)

        assert "session_id" in result
        assert "ai_text" in result

    def test_start_with_unavailable_ai(self):
        """AI provider says not available → use fallback."""
        user_id = uuid.uuid4()
        words = [make_word_entity(confidence_score=30, original_word=f"word{i}") for i in range(10)]
        self.word_repo.get_all_by_user.return_value = (words, len(words))
        session = _make_game_session(user_id=user_id)
        self.game_repo.create.return_value = session
        story_round = _make_story_round(session_id=session.id)
        self.game_repo.create_story_round.return_value = story_round

        self.ai_provider.is_available.return_value = False
        uc = self._make_uc()
        result = uc.execute(user_id)

        assert "session_id" in result

    def test_start_not_enough_words(self):
        """Not enough words → ValidationError."""
        user_id = uuid.uuid4()
        words = [make_word_entity(confidence_score=30, original_word=f"word{i}") for i in range(2)]
        self.word_repo.get_all_by_user.return_value = (words, len(words))

        uc = self._make_uc()
        with pytest.raises(Exception):
            uc.execute(user_id)

    def test_selects_low_confidence_words(self):
        """Words with confidence < 80 are preferred."""
        user_id = uuid.uuid4()
        low = [make_word_entity(confidence_score=20, original_word=f"low{i}") for i in range(8)]
        high = [make_word_entity(confidence_score=90, original_word=f"high{i}") for i in range(4)]
        self.word_repo.get_all_by_user.return_value = (low + high, 12)
        session = _make_game_session(user_id=user_id)
        self.game_repo.create.return_value = session
        story_round = _make_story_round(session_id=session.id)
        self.game_repo.create_story_round.return_value = story_round

        self.ai_provider.is_available.return_value = False
        uc = self._make_uc()
        result = uc.execute(user_id)

        assert "session_id" in result


class TestSubmitStoryRoundUseCase:

    def setup_method(self):
        self.game_repo = MagicMock()
        self.word_repo = MagicMock()
        self.ai_provider = MagicMock()
        self.sr_service = MagicMock()

    def _make_uc(self, ai_provider="DEFAULT"):
        provider = self.ai_provider if ai_provider == "DEFAULT" else ai_provider
        return SubmitStoryRoundUseCase(
            game_repo=self.game_repo,
            word_repo=self.word_repo,
            ai_provider=provider,
            sr_service=self.sr_service,
        )

    def test_submit_with_ai_analysis(self):
        """Submit round with AI analysis working."""
        user_id = uuid.uuid4()
        session = _make_game_session(user_id=user_id)
        self.game_repo.get_by_id.return_value = session

        current_round = _make_story_round(
            session_id=session.id, round_number=1,
            target_words=["apple", "run"],
        )
        self.game_repo.get_story_rounds.return_value = [current_round]

        words = [
            make_word_entity(original_word="apple", confidence_score=30),
            make_word_entity(original_word="run", confidence_score=30),
            make_word_entity(original_word="beautiful", confidence_score=30),
        ]
        self.word_repo.get_all_by_user.return_value = (words, len(words))
        self.word_repo.get_by_id.return_value = words[0]
        self.word_repo.update.return_value = words[0]

        self.ai_provider.is_available.return_value = True
        self.ai_provider.generate_json.return_value = {
            "words_used_correctly": ["apple", "run"],
            "grammar_corrections": [],
            "score": 18,
            "feedback": "Great!",
            "continuation": "The story continues...",
        }

        uc = self._make_uc()
        result = uc.execute(
            session_id=session.id,
            user_id=user_id,
            user_text="The apple fell and I had to run.",
        )

        assert "round_result" in result
        assert "xp_earned" in result

    def test_submit_without_ai_uses_fallback(self):
        """Submit round without AI falls back to word presence check."""
        user_id = uuid.uuid4()
        session = _make_game_session(user_id=user_id)
        self.game_repo.get_by_id.return_value = session

        current_round = _make_story_round(
            session_id=session.id, round_number=1,
            target_words=["apple", "run"],
        )
        self.game_repo.get_story_rounds.return_value = [current_round]

        words = [
            make_word_entity(original_word="apple", confidence_score=30),
            make_word_entity(original_word="run", confidence_score=30),
            make_word_entity(original_word="beautiful", confidence_score=30),
        ]
        self.word_repo.get_all_by_user.return_value = (words, len(words))

        uc = self._make_uc(ai_provider=None)
        result = uc.execute(
            session_id=session.id,
            user_id=user_id,
            user_text="The apple fell and I had to run quickly.",
        )

        assert "round_result" in result

    def test_submit_last_round_no_next(self):
        """Round 5 submission does not create round 6."""
        user_id = uuid.uuid4()
        session = _make_game_session(user_id=user_id)
        self.game_repo.get_by_id.return_value = session

        rounds = [_make_story_round(session_id=session.id, round_number=i + 1) for i in range(4)]
        current_round = _make_story_round(
            session_id=session.id, round_number=5,
            target_words=["apple"],
        )
        rounds.append(current_round)
        self.game_repo.get_story_rounds.return_value = rounds

        words = [make_word_entity(original_word="apple", confidence_score=30)]
        self.word_repo.get_all_by_user.return_value = (words, len(words))

        uc = self._make_uc(ai_provider=None)
        result = uc.execute(
            session_id=session.id,
            user_id=user_id,
            user_text="I saw an apple on the tree and it was beautiful.",
        )

        assert result["next_round"] is None


class TestCompleteStoryBuilderUseCase:

    def setup_method(self):
        self.game_repo = MagicMock()
        self.xp_service = MagicMock()
        self.badge_service = MagicMock()

    def _make_uc(self):
        return CompleteStoryBuilderUseCase(
            game_repo=self.game_repo,
            xp_service=self.xp_service,
            badge_service=self.badge_service,
        )

    def test_complete_calculates_total_score(self):
        """Complete game → score totalled from rounds."""
        user_id = uuid.uuid4()
        session = _make_game_session(user_id=user_id)
        self.game_repo.get_by_id.return_value = session

        rounds = [
            _make_story_round(round_number=i + 1, score=15) for i in range(5)
        ]
        self.game_repo.get_story_rounds.return_value = rounds
        self.xp_service.award_xp.return_value = {"xp_gained": 15}
        self.badge_service.check_and_award_badges.return_value = []

        uc = self._make_uc()
        result = uc.execute(user_id=user_id, session_id=session.id)

        assert "total_score" in result
        assert "full_story" in result
        assert result["total_score"] == 75

    def test_complete_awards_xp(self):
        """Complete game → XP awarded."""
        user_id = uuid.uuid4()
        session = _make_game_session(user_id=user_id)
        self.game_repo.get_by_id.return_value = session
        self.game_repo.get_story_rounds.return_value = [
            _make_story_round(round_number=1, score=20, ai_text="Once...", user_text="Then..."),
        ]
        self.xp_service.award_xp.return_value = {"xp_gained": 15}
        self.badge_service.check_and_award_badges.return_value = []

        uc = self._make_uc()
        result = uc.execute(user_id=user_id, session_id=session.id)

        self.xp_service.award_xp.assert_called()

    def test_complete_checks_badges(self):
        """Complete game → badges checked."""
        user_id = uuid.uuid4()
        session = _make_game_session(user_id=user_id)
        self.game_repo.get_by_id.return_value = session
        self.game_repo.get_story_rounds.return_value = [
            _make_story_round(round_number=1, score=20),
        ]
        self.xp_service.award_xp.return_value = {"xp_gained": 15}
        self.badge_service.check_and_award_badges.return_value = []

        uc = self._make_uc()
        uc.execute(user_id=user_id, session_id=session.id)

        self.badge_service.check_and_award_badges.assert_called_once()

    def test_complete_without_xp_service(self):
        """Complete game without XP service → no error."""
        user_id = uuid.uuid4()
        session = _make_game_session(user_id=user_id)
        self.game_repo.get_by_id.return_value = session
        self.game_repo.get_story_rounds.return_value = [
            _make_story_round(round_number=1, score=15),
        ]

        uc = CompleteStoryBuilderUseCase(
            game_repo=self.game_repo,
            xp_service=None,
            badge_service=None,
        )
        result = uc.execute(user_id=user_id, session_id=session.id)

        assert "total_score" in result
