"""
Tests for LearningProfileService.
"""

import pytest

from apps.users.domain.services.learning_profile_service import LearningProfileService


class TestLearningProfileService:

    def setup_method(self):
        self.service = LearningProfileService()

    def test_analyze_style_visual(self):
        """High word_match & word_context → visual style."""
        stats = {
            "review_accuracy": 0.5,
            "test_accuracy": 0.5,
            "game_scores": {"word_match": 0.9, "word_context": 0.9},
            "listening_accuracy": 0.3,
        }
        result = self.service.analyze_learning_style(stats)
        assert result["style"] == "visual"
        assert 0 < result["confidence"] <= 1
        assert "breakdown" in result

    def test_analyze_style_auditory(self):
        """High listening accuracy → auditory style."""
        stats = {
            "review_accuracy": 0.3,
            "test_accuracy": 0.3,
            "game_scores": {"listening_challenge": 0.95, "story_builder": 0.8},
            "listening_accuracy": 0.95,
        }
        result = self.service.analyze_learning_style(stats)
        assert result["style"] == "auditory"

    def test_optimal_time_calculation(self):
        """Returns best hours and days from performance data."""
        performances = [
            {"hour": 9, "day": 0, "effectiveness": 0.9},
            {"hour": 9, "day": 1, "effectiveness": 0.85},
            {"hour": 14, "day": 2, "effectiveness": 0.6},
            {"hour": 10, "day": 0, "effectiveness": 0.8},
            {"hour": 10, "day": 3, "effectiveness": 0.75},
        ]
        result = self.service.calculate_optimal_time(performances)
        assert 9 in result["best_hours"]
        assert len(result["best_hours"]) <= 3
        assert 0 <= result["confidence"] <= 1

    def test_difficulty_adjustment_up(self):
        """Accuracy > 0.8 increases difficulty."""
        new_level = self.service.calculate_difficulty_adjustment(0.5, 0.9, 0.05)
        assert new_level == 0.55

    def test_difficulty_adjustment_down(self):
        """Accuracy < 0.5 decreases difficulty."""
        new_level = self.service.calculate_difficulty_adjustment(0.5, 0.3, 0.05)
        assert new_level == 0.45

    def test_difficulty_no_change(self):
        """Accuracy between 0.5 and 0.8 keeps difficulty the same."""
        new_level = self.service.calculate_difficulty_adjustment(0.5, 0.65, 0.05)
        assert new_level == 0.5
