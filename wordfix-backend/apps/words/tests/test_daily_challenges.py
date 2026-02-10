"""
Tests for DailyChallengeService — challenge generation and daily challenge use cases.
"""

import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4
from datetime import date

from apps.words.domain.services import DailyChallengeService
from apps.words.application.use_cases.daily_challenges import (
    GetDailyChallengesUseCase,
    UpdateChallengeProgressUseCase,
    ClaimDailyBonusUseCase,
)


class TestDailyChallengeService:
    """Test challenge generation logic."""

    def test_generates_three_challenges(self):
        challenges = DailyChallengeService.generate_daily_challenges(1, 10)
        assert len(challenges) == 3

    def test_easy_level_uses_easy_pool(self):
        challenges = DailyChallengeService.generate_daily_challenges(1, 10)
        valid_types = {c["type"] for c in DailyChallengeService.CHALLENGE_TYPES_EASY}
        for c in challenges:
            assert c["type"] in valid_types

    def test_medium_level_uses_medium_pool(self):
        challenges = DailyChallengeService.generate_daily_challenges(5, 20)
        valid_types = {c["type"] for c in DailyChallengeService.CHALLENGE_TYPES_MEDIUM}
        for c in challenges:
            assert c["type"] in valid_types

    def test_hard_level_uses_hard_pool(self):
        challenges = DailyChallengeService.generate_daily_challenges(10, 50)
        valid_types = {c["type"] for c in DailyChallengeService.CHALLENGE_TYPES_HARD}
        for c in challenges:
            assert c["type"] in valid_types

    def test_forces_add_words_when_few_words(self):
        challenges = DailyChallengeService.generate_daily_challenges(1, 2)
        types = [c["type"] for c in challenges]
        assert "add_words" in types

    def test_no_duplicate_types(self):
        for _ in range(20):  # Run multiple times due to randomness
            challenges = DailyChallengeService.generate_daily_challenges(5, 30)
            types = [c["type"] for c in challenges]
            assert len(types) == len(set(types)), f"Duplicate types found: {types}"

    def test_challenges_have_required_fields(self):
        challenges = DailyChallengeService.generate_daily_challenges(1, 10)
        for c in challenges:
            assert "type" in c
            assert "target" in c
            assert "current" in c
            assert c["current"] == 0
            assert "completed" in c
            assert c["completed"] is False
            assert "xp_reward" in c
            assert "title" in c


class TestGetDailyChallengesUseCase:
    """Test getting/creating daily challenges."""

    def test_creates_challenges_when_none_exist(self):
        challenge_entity = MagicMock()
        challenge_entity.challenges = []
        challenge_entity.all_completed = False
        challenge_entity.bonus_claimed = False
        challenge_entity.date = date.today()
        challenge_entity.id = uuid4()

        updated_entity = MagicMock()
        updated_entity.challenges = [{"type": "review_words"}]
        updated_entity.all_completed = False
        updated_entity.bonus_claimed = False
        updated_entity.date = date.today()

        challenge_repo = MagicMock()
        challenge_repo.get_or_create_today.return_value = (challenge_entity, True)
        challenge_repo.update.return_value = updated_entity

        word_repo = MagicMock()
        word_repo.get_count_by_user.return_value = 10

        progress_repo = MagicMock()
        progress = MagicMock()
        progress.level = 3
        progress_repo.get_or_create.return_value = progress

        challenge_service = DailyChallengeService()
        uc = GetDailyChallengesUseCase(challenge_repo, word_repo, progress_repo, challenge_service)
        result = uc.execute(uuid4())

        assert "challenges" in result
        assert "date" in result

    def test_returns_existing_challenges(self):
        existing = [
            {"type": "review_words", "target": 5, "current": 2, "completed": False,
             "xp_reward": 20},
        ]
        challenge_entity = MagicMock()
        challenge_entity.challenges = existing
        challenge_entity.all_completed = False
        challenge_entity.bonus_claimed = False
        challenge_entity.date = date.today()

        challenge_repo = MagicMock()
        challenge_repo.get_or_create_today.return_value = (challenge_entity, False)

        uc = GetDailyChallengesUseCase(challenge_repo, MagicMock(), MagicMock(), DailyChallengeService())
        result = uc.execute(uuid4())

        assert result["challenges"] == existing


class TestUpdateChallengeProgressUseCase:
    """Test updating challenge progress."""

    def test_increments_challenge_progress(self):
        challenges = [
            {"type": "review_words", "target": 5, "current": 2, "completed": False,
             "xp_reward": 20, "title": "Review 5 words", "icon": "book"},
        ]
        challenge_entity = MagicMock()
        challenge_entity.challenges = challenges
        challenge_entity.all_completed = False
        challenge_entity.id = uuid4()

        repo = MagicMock()
        repo.get_or_create_today.return_value = (challenge_entity, False)
        repo.update.return_value = challenge_entity

        uc = UpdateChallengeProgressUseCase(repo)
        result = uc.execute(uuid4(), "review_words", amount=1)

        assert result["challenge_updated"] is True

    def test_completes_challenge_at_target(self):
        challenges = [
            {"type": "review_words", "target": 5, "current": 4, "completed": False,
             "xp_reward": 20, "title": "Review 5 words", "icon": "book"},
        ]
        challenge_entity = MagicMock()
        challenge_entity.challenges = challenges
        challenge_entity.all_completed = False
        challenge_entity.id = uuid4()

        repo = MagicMock()
        repo.get_or_create_today.return_value = (challenge_entity, False)
        repo.update.return_value = challenge_entity

        uc = UpdateChallengeProgressUseCase(repo)
        result = uc.execute(uuid4(), "review_words", amount=1)

        assert result["challenge_updated"] is True
        assert result["completed"] is True

    def test_no_match_returns_not_updated(self):
        challenges = [
            {"type": "review_words", "target": 5, "current": 0, "completed": False,
             "xp_reward": 20},
        ]
        challenge_entity = MagicMock()
        challenge_entity.challenges = challenges
        challenge_entity.all_completed = False
        challenge_entity.id = uuid4()

        repo = MagicMock()
        repo.get_or_create_today.return_value = (challenge_entity, False)

        uc = UpdateChallengeProgressUseCase(repo)
        result = uc.execute(uuid4(), "play_game", amount=1)

        assert result["challenge_updated"] is False

    def test_already_completed_challenge_skipped(self):
        challenges = [
            {"type": "review_words", "target": 5, "current": 5, "completed": True,
             "xp_reward": 20},
        ]
        challenge_entity = MagicMock()
        challenge_entity.challenges = challenges
        challenge_entity.all_completed = False
        challenge_entity.id = uuid4()

        repo = MagicMock()
        repo.get_or_create_today.return_value = (challenge_entity, False)

        uc = UpdateChallengeProgressUseCase(repo)
        result = uc.execute(uuid4(), "review_words", amount=1)

        assert result["challenge_updated"] is False
