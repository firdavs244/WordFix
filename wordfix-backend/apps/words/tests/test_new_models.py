"""
Tests for new models: WordDistractor, ConfusingPair, DailyChallenge, combo fields,
StoryRound, and ListeningRound.
"""

import pytest
from datetime import date
from uuid import UUID

from apps.words.infrastructure.models import (
    WordDistractor,
    ConfusingPair,
    DailyChallenge,
    ReviewSession,
    TestSession,
    GameSession,
    StoryRound,
    ListeningRound,
)


@pytest.mark.django_db
class TestWordDistractorModel:
    """Test WordDistractor model."""

    def test_create_word_distractor(self, sample_word):
        distractor = WordDistractor.objects.create(
            word=sample_word,
            distractors=["goodbye", "sorry", "thanks"],
            language="en",
            generated_by="ai",
        )
        assert distractor.id is not None
        assert distractor.distractors == ["goodbye", "sorry", "thanks"]
        assert distractor.generated_by == "ai"

    def test_unique_together_word_language(self, sample_word):
        WordDistractor.objects.create(
            word=sample_word,
            distractors=["a", "b", "c"],
            language="en",
        )
        with pytest.raises(Exception):
            WordDistractor.objects.create(
                word=sample_word,
                distractors=["d", "e", "f"],
                language="en",
            )

    def test_default_generated_by(self, sample_word):
        distractor = WordDistractor.objects.create(
            word=sample_word,
            distractors=["a", "b"],
            language="en",
        )
        assert distractor.generated_by == "ai"


@pytest.mark.django_db
class TestConfusingPairModel:
    """Test ConfusingPair model."""

    def test_create_confusing_pair(self, user, sample_words):
        pair = ConfusingPair.objects.create(
            user=user,
            word_1=sample_words[0],
            word_2=sample_words[1],
        )
        assert pair.id is not None
        assert pair.confusion_count == 1
        assert pair.is_resolved is False

    def test_unique_together(self, user, sample_words):
        ConfusingPair.objects.create(
            user=user,
            word_1=sample_words[0],
            word_2=sample_words[1],
        )
        with pytest.raises(Exception):
            ConfusingPair.objects.create(
                user=user,
                word_1=sample_words[0],
                word_2=sample_words[1],
            )

    def test_confusion_count_increment(self, confusing_pair):
        confusing_pair.confusion_count += 1
        confusing_pair.save()
        confusing_pair.refresh_from_db()
        assert confusing_pair.confusion_count == 4


@pytest.mark.django_db
class TestDailyChallengeModel:
    """Test DailyChallenge model."""

    def test_create_daily_challenge(self, user):
        challenge = DailyChallenge.objects.create(
            user=user,
            date=date.today(),
            challenges=[
                {"type": "review_words", "target": 5, "current": 0, "completed": False},
            ],
        )
        assert challenge.id is not None
        assert challenge.all_completed is False
        assert challenge.bonus_claimed is False

    def test_unique_together_user_date(self, user):
        DailyChallenge.objects.create(
            user=user,
            date=date.today(),
            challenges=[],
        )
        with pytest.raises(Exception):
            DailyChallenge.objects.create(
                user=user,
                date=date.today(),
                challenges=[],
            )


@pytest.mark.django_db
class TestComboFieldsOnSession:
    """Test combo fields exist on session models."""

    def test_review_session_combo_fields(self, review_session):
        assert review_session.current_combo == 0
        assert review_session.max_combo == 0
        assert review_session.combo_xp_bonus == 0

    def test_test_session_combo_fields(self, test_session):
        assert test_session.current_combo == 0
        assert test_session.max_combo == 0
        assert test_session.combo_xp_bonus == 0

    def test_game_session_combo_fields(self, game_session):
        assert game_session.current_combo == 0
        assert game_session.max_combo == 0
        assert game_session.combo_xp_bonus == 0

    def test_update_combo_fields(self, review_session):
        review_session.current_combo = 5
        review_session.max_combo = 10
        review_session.combo_xp_bonus = 25
        review_session.save()
        review_session.refresh_from_db()
        assert review_session.current_combo == 5
        assert review_session.max_combo == 10
        assert review_session.combo_xp_bonus == 25


@pytest.mark.django_db
class TestStoryRoundModel:
    """Test StoryRound model."""

    def test_create_story_round(self, user):
        session = GameSession.objects.create(
            user=user, game_type="story_builder", max_score=100,
        )
        story_round = StoryRound.objects.create(
            session=session,
            round_number=1,
            ai_text="Once upon a time...",
            target_words=["apple", "run"],
        )
        assert story_round.id is not None
        assert story_round.round_number == 1
        assert story_round.target_words == ["apple", "run"]
        assert story_round.score == 0

    def test_story_round_defaults(self, user):
        session = GameSession.objects.create(
            user=user, game_type="story_builder", max_score=100,
        )
        story_round = StoryRound.objects.create(
            session=session, round_number=1,
        )
        assert story_round.ai_text == ""
        assert story_round.user_text == ""
        assert story_round.target_words == []
        assert story_round.words_used == []
        assert story_round.grammar_corrections == []
        assert story_round.is_correct_usage is False
        assert story_round.score == 0

    def test_multiple_rounds_per_session(self, user):
        session = GameSession.objects.create(
            user=user, game_type="story_builder", max_score=100,
        )
        for i in range(5):
            StoryRound.objects.create(
                session=session, round_number=i + 1,
                ai_text=f"Round {i + 1} text",
            )
        assert StoryRound.objects.filter(session=session).count() == 5


@pytest.mark.django_db
class TestListeningRoundModel:
    """Test ListeningRound model."""

    def test_create_listening_round(self, user, sample_word):
        session = GameSession.objects.create(
            user=user, game_type="listening_challenge", max_score=100,
        )
        listening_round = ListeningRound.objects.create(
            session=session,
            word=sample_word,
            round_number=1,
            correct_answer="hello",
        )
        assert listening_round.id is not None
        assert listening_round.correct_answer == "hello"
        assert listening_round.max_attempts == 3

    def test_listening_round_defaults(self, user, sample_word):
        session = GameSession.objects.create(
            user=user, game_type="listening_challenge", max_score=100,
        )
        listening_round = ListeningRound.objects.create(
            session=session, word=sample_word,
            round_number=1, correct_answer="hello",
        )
        assert listening_round.user_answers == []
        assert listening_round.attempts_used == 0
        assert listening_round.is_correct is False
        assert listening_round.hints_shown == []
        assert listening_round.score == 0

    def test_update_listening_round_attempts(self, user, sample_word):
        session = GameSession.objects.create(
            user=user, game_type="listening_challenge", max_score=100,
        )
        listening_round = ListeningRound.objects.create(
            session=session, word=sample_word,
            round_number=1, correct_answer="hello",
        )
        listening_round.user_answers = ["helo", "hello"]
        listening_round.attempts_used = 2
        listening_round.is_correct = True
        listening_round.score = 7
        listening_round.save()
        listening_round.refresh_from_db()
        assert listening_round.attempts_used == 2
        assert listening_round.is_correct is True
        assert listening_round.score == 7
