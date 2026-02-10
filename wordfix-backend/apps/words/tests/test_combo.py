"""
Tests for ComboService — combo multiplier logic.
"""

import pytest

from apps.words.domain.services import ComboService


class TestComboServiceGetMultiplier:
    """Test get_multiplier static method."""

    def test_no_combo(self):
        assert ComboService.get_multiplier(0) == 1.0

    def test_single_correct(self):
        assert ComboService.get_multiplier(1) == 1.0

    def test_combo_2(self):
        assert ComboService.get_multiplier(2) == 1.5

    def test_combo_5(self):
        assert ComboService.get_multiplier(5) == 2.0

    def test_combo_10(self):
        assert ComboService.get_multiplier(10) == 3.0

    def test_combo_20(self):
        assert ComboService.get_multiplier(20) == 5.0

    def test_combo_50_uses_highest_threshold(self):
        assert ComboService.get_multiplier(50) == 5.0


class TestComboServiceCalculateXP:
    """Test calculate_combo_xp method."""

    def test_no_combo_xp(self):
        xp, mult = ComboService.calculate_combo_xp(10, 0)
        assert xp == 10
        assert mult == 1.0

    def test_combo_2_xp(self):
        xp, mult = ComboService.calculate_combo_xp(10, 2)
        assert xp == 15
        assert mult == 1.5

    def test_combo_5_xp(self):
        xp, mult = ComboService.calculate_combo_xp(10, 5)
        assert xp == 20
        assert mult == 2.0

    def test_combo_10_xp(self):
        xp, mult = ComboService.calculate_combo_xp(10, 10)
        assert xp == 30
        assert mult == 3.0

    def test_combo_20_xp(self):
        xp, mult = ComboService.calculate_combo_xp(10, 20)
        assert xp == 50
        assert mult == 5.0

    def test_zero_base_xp(self):
        xp, mult = ComboService.calculate_combo_xp(0, 10)
        assert xp == 0
        assert mult == 3.0

    def test_large_base_xp(self):
        xp, mult = ComboService.calculate_combo_xp(100, 5)
        assert xp == 200
        assert mult == 2.0
