"""
GameSession Django ORM model.
"""

from django.conf import settings
from django.db import models

from apps.common.models import AbstractBaseModel


class GameSession(AbstractBaseModel):
    """Game session for word games."""

    GAME_TYPE_CHOICES = [
        ("speed_round", "Speed Round"),
        ("word_match", "Word Match"),
        ("word_context", "Word Context"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="game_sessions",
    )
    game_type = models.CharField(max_length=15, choices=GAME_TYPE_CHOICES)
    score = models.PositiveIntegerField(default=0)
    max_score = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    incorrect_answers = models.PositiveIntegerField(default=0)
    duration_seconds = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    level = models.PositiveIntegerField(default=1)
    xp_earned = models.PositiveIntegerField(default=0)
    current_combo = models.PositiveIntegerField(default=0)
    max_combo = models.PositiveIntegerField(default=0)
    combo_xp_bonus = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "game_sessions"
        ordering = ["-started_at"]
        verbose_name = "Game Session"
        verbose_name_plural = "Game Sessions"

    def __str__(self) -> str:
        return f"Game {self.game_type} by user {self.user_id}"
