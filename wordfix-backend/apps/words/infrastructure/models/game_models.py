"""
GameSession, StoryRound, ListeningRound Django ORM models.
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
        ("story_builder", "Story Builder"),
        ("listening_challenge", "Listening Challenge"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="game_sessions",
    )
    game_type = models.CharField(max_length=20, choices=GAME_TYPE_CHOICES)
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


class StoryRound(AbstractBaseModel):
    """A single round in a Story Builder game."""

    session = models.ForeignKey(
        GameSession,
        on_delete=models.CASCADE,
        related_name="story_rounds",
    )
    round_number = models.PositiveIntegerField()
    ai_text = models.TextField()
    user_text = models.TextField(blank=True, default="")
    target_words = models.JSONField(default=list)
    words_used = models.JSONField(default=list)
    grammar_corrections = models.JSONField(default=list)
    is_correct_usage = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "story_rounds"
        ordering = ["round_number"]
        unique_together = ["session", "round_number"]
        verbose_name = "Story Round"
        verbose_name_plural = "Story Rounds"

    def __str__(self) -> str:
        return f"StoryRound {self.round_number} for session {self.session_id}"


class ListeningRound(AbstractBaseModel):
    """A single round in a Listening Challenge game."""

    session = models.ForeignKey(
        GameSession,
        on_delete=models.CASCADE,
        related_name="listening_rounds",
    )
    word = models.ForeignKey(
        "words.Word",
        on_delete=models.CASCADE,
    )
    round_number = models.PositiveIntegerField()
    correct_answer = models.CharField(max_length=100)
    user_answers = models.JSONField(default=list)
    attempts_used = models.PositiveIntegerField(default=0)
    max_attempts = models.PositiveIntegerField(default=3)
    is_correct = models.BooleanField(default=False)
    hints_shown = models.JSONField(default=list)
    score = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "listening_rounds"
        ordering = ["round_number"]
        unique_together = ["session", "round_number"]
        verbose_name = "Listening Round"
        verbose_name_plural = "Listening Rounds"

    def __str__(self) -> str:
        return f"ListeningRound {self.round_number} for session {self.session_id}"
