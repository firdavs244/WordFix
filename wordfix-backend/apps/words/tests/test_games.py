"""
Tests for Game use cases.
"""

import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from apps.words.application.use_cases import (
    GetGameHistoryUseCase,
    GetGameStatsUseCase,
    StartSpeedRoundUseCase,
    StartWordContextUseCase,
    StartWordMatchUseCase,
    SubmitSpeedRoundUseCase,
    SubmitWordContextUseCase,
    SubmitWordMatchUseCase,
)
from apps.words.domain.services import SpacedRepetitionService
from apps.words.infrastructure.models import GameSession, Word


@pytest.mark.django_db
class TestSpeedRound:
    """Tests for Speed Round game."""

    def test_speed_round_start(self, user, sample_words):
        """Start returns words + options."""
        from apps.words.infrastructure.repositories import (
            DjangoGameSessionRepository,
            DjangoWordRepository,
        )

        uc = StartSpeedRoundUseCase(
            word_repo=DjangoWordRepository(),
            game_session_repo=DjangoGameSessionRepository(),
        )

        result = uc.execute(user_id=user.id)

        assert "session_id" in result
        assert "words" in result
        assert "time_limit" in result
        assert result["time_limit"] == 60
        assert len(result["words"]) > 0

        first_word = result["words"][0]
        assert "word" in first_word
        assert "options" in first_word
        assert len(first_word["options"]) == 4

    def test_speed_round_submit(self, user, sample_words):
        """Submit calculates score and updates SR."""
        from apps.words.infrastructure.repositories import (
            DjangoDailyActivityRepository,
            DjangoGameSessionRepository,
            DjangoWordRepository,
        )

        # Start the game first
        start_uc = StartSpeedRoundUseCase(
            word_repo=DjangoWordRepository(),
            game_session_repo=DjangoGameSessionRepository(),
        )
        start_result = start_uc.execute(user_id=user.id)

        # Submit some answers
        answers = []
        for word_data in start_result["words"][:3]:
            answers.append({
                "word_id": word_data["word_id"],
                "selected_answer": word_data["correct_translation"],
            })

        submit_uc = SubmitSpeedRoundUseCase(
            word_repo=DjangoWordRepository(),
            game_session_repo=DjangoGameSessionRepository(),
            sr_service=SpacedRepetitionService(),
            activity_repo=DjangoDailyActivityRepository(),
        )

        session = submit_uc.execute(
            session_id=start_result["session_id"],
            user_id=user.id,
            answers=answers,
        )

        assert session.is_completed is True
        assert session.correct_answers == 3
        assert session.xp_earned > 0


@pytest.mark.django_db
class TestWordMatch:
    """Tests for Word Match game."""

    def test_word_match_start(self, user, sample_words):
        """Start returns words + shuffled translations."""
        from apps.words.infrastructure.repositories import (
            DjangoGameSessionRepository,
            DjangoWordRepository,
        )

        uc = StartWordMatchUseCase(
            word_repo=DjangoWordRepository(),
            game_session_repo=DjangoGameSessionRepository(),
        )

        result = uc.execute(user_id=user.id, pair_count=5)

        assert "session_id" in result
        assert "words" in result
        assert "translations" in result
        assert len(result["words"]) == 5
        assert len(result["translations"]) == 5

    def test_word_match_submit(self, user, sample_words):
        """Submit checks pairs, updates SR."""
        from apps.words.infrastructure.repositories import (
            DjangoDailyActivityRepository,
            DjangoGameSessionRepository,
            DjangoWordRepository,
        )

        start_uc = StartWordMatchUseCase(
            word_repo=DjangoWordRepository(),
            game_session_repo=DjangoGameSessionRepository(),
        )
        start_result = start_uc.execute(user_id=user.id, pair_count=5)

        # Build correct pairs
        pairs = []
        for word_data in start_result["words"]:
            word = Word.objects.get(id=word_data["word_id"])
            pairs.append({
                "word_id": word_data["word_id"],
                "matched_translation": word.translation,
            })

        submit_uc = SubmitWordMatchUseCase(
            word_repo=DjangoWordRepository(),
            game_session_repo=DjangoGameSessionRepository(),
            sr_service=SpacedRepetitionService(),
            activity_repo=DjangoDailyActivityRepository(),
        )

        session = submit_uc.execute(
            session_id=start_result["session_id"],
            user_id=user.id,
            pairs=pairs,
            time_seconds=30,
        )

        assert session.is_completed is True
        assert session.correct_answers == 5


@pytest.mark.django_db
class TestWordContext:
    """Tests for Word Context game."""

    def test_word_context_start(self, user, sample_words):
        """AI mock → context paragraphs returned."""
        mock_ai = MagicMock()
        mock_ai.is_available.return_value = True
        mock_ai.generate_json.return_value = [
            {
                "word": "apple",
                "context": "I ate a delicious ___ yesterday.",
                "correct_answer": "apple",
                "options": ["apple", "car", "book", "house"],
                "explanation": "Context: eating.",
            }
            for _ in range(5)
        ]

        from apps.words.infrastructure.repositories import (
            DjangoGameSessionRepository,
            DjangoWordRepository,
        )

        uc = StartWordContextUseCase(
            word_repo=DjangoWordRepository(),
            game_session_repo=DjangoGameSessionRepository(),
            ai_provider=mock_ai,
            prompt_template="test {words_list} {native_language} {proficiency_level}",
        )

        result = uc.execute(user_id=user.id)

        assert "session_id" in result
        assert "questions" in result
        assert len(result["questions"]) == 5

    def test_word_context_fallback(self, user, sample_words):
        """AI fail → example sentences used."""
        from apps.words.infrastructure.repositories import (
            DjangoGameSessionRepository,
            DjangoWordRepository,
        )

        uc = StartWordContextUseCase(
            word_repo=DjangoWordRepository(),
            game_session_repo=DjangoGameSessionRepository(),
            ai_provider=None,  # No AI
        )

        result = uc.execute(user_id=user.id)

        assert "session_id" in result
        assert "questions" in result
        assert len(result["questions"]) == 5

    def test_word_context_submit(self, user, sample_words):
        """Submit context answers calculates score."""
        from apps.words.infrastructure.repositories import (
            DjangoDailyActivityRepository,
            DjangoGameSessionRepository,
            DjangoWordRepository,
        )

        # Start
        start_uc = StartWordContextUseCase(
            word_repo=DjangoWordRepository(),
            game_session_repo=DjangoGameSessionRepository(),
        )
        start_result = start_uc.execute(user_id=user.id)

        # Submit correct answers
        answers = []
        for q in start_result["questions"]:
            answers.append({
                "word_id": q["word_id"],
                "selected_answer": q["correct_answer"],
            })

        submit_uc = SubmitWordContextUseCase(
            word_repo=DjangoWordRepository(),
            game_session_repo=DjangoGameSessionRepository(),
            sr_service=SpacedRepetitionService(),
            activity_repo=DjangoDailyActivityRepository(),
        )

        session = submit_uc.execute(
            session_id=start_result["session_id"],
            user_id=user.id,
            answers=answers,
        )

        assert session.is_completed is True
        assert session.correct_answers == 5


@pytest.mark.django_db
class TestGameHistory:
    """Tests for game history and stats."""

    def test_game_history(self, user):
        """Paginated history."""
        for gt in ["speed_round", "word_match", "word_context"]:
            GameSession.objects.create(
                user=user, game_type=gt, is_completed=True, score=10,
            )

        from apps.words.infrastructure.repositories import DjangoGameSessionRepository

        uc = GetGameHistoryUseCase(
            game_session_repo=DjangoGameSessionRepository(),
        )
        sessions, total = uc.execute(user_id=user.id)
        assert total == 3

    def test_game_stats(self, user):
        """Stats aggregation."""
        GameSession.objects.create(
            user=user, game_type="speed_round", is_completed=True,
            score=20, xp_earned=100,
        )
        GameSession.objects.create(
            user=user, game_type="speed_round", is_completed=True,
            score=25, xp_earned=150,
        )

        from apps.words.infrastructure.repositories import DjangoGameSessionRepository

        uc = GetGameStatsUseCase(
            game_session_repo=DjangoGameSessionRepository(),
        )
        stats = uc.execute(user_id=user.id)

        assert stats["total_games"] == 2
        assert stats["total_xp"] == 250
        assert stats["favorite_game"] == "speed_round"
        assert stats["by_type"]["speed_round"]["best_score"] == 25

    def test_not_enough_words(self, user):
        """< 5 words → error."""
        Word.objects.create(user=user, original_word="one", translation="bir")

        from apps.words.infrastructure.repositories import (
            DjangoGameSessionRepository,
            DjangoWordRepository,
        )

        uc = StartSpeedRoundUseCase(
            word_repo=DjangoWordRepository(),
            game_session_repo=DjangoGameSessionRepository(),
        )

        with pytest.raises(Exception) as exc_info:
            uc.execute(user_id=user.id)
        assert "5 words" in str(exc_info.value)

    def test_xp_calculation(self, user, sample_words):
        """XP doubles for 80%+ accuracy."""
        from apps.words.infrastructure.repositories import (
            DjangoDailyActivityRepository,
            DjangoGameSessionRepository,
            DjangoWordRepository,
        )

        start_uc = StartSpeedRoundUseCase(
            word_repo=DjangoWordRepository(),
            game_session_repo=DjangoGameSessionRepository(),
        )
        start_result = start_uc.execute(user_id=user.id)

        # Submit ALL correct answers (100% accuracy → x2 XP)
        answers = []
        for word_data in start_result["words"]:
            answers.append({
                "word_id": word_data["word_id"],
                "selected_answer": word_data["correct_translation"],
            })

        submit_uc = SubmitSpeedRoundUseCase(
            word_repo=DjangoWordRepository(),
            game_session_repo=DjangoGameSessionRepository(),
            sr_service=SpacedRepetitionService(),
            activity_repo=DjangoDailyActivityRepository(),
        )

        session = submit_uc.execute(
            session_id=start_result["session_id"],
            user_id=user.id,
            answers=answers,
        )

        n = len(answers)
        expected_xp = n * 10 * 2  # x2 bonus for 100% accuracy
        assert session.xp_earned == expected_xp
