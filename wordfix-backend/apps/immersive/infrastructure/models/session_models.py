"""
ImmersiveSession and ConversationTurn Django ORM models.
"""

from django.conf import settings
from django.db import models

from apps.common.models import AbstractBaseModel

from .scenario_models import ImmersiveScenario, NPCCharacter


class ImmersiveSession(AbstractBaseModel):
    """A user's immersive game session."""

    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("abandoned", "Abandoned"),
        ("timeout", "Timeout"),
    ]

    INPUT_MODE_CHOICES = [
        ("text", "Text"),
        ("voice", "Voice"),
        ("mixed", "Mixed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="immersive_sessions",
    )
    scenario = models.ForeignKey(
        ImmersiveScenario,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    npc = models.ForeignKey(
        NPCCharacter,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    input_mode = models.CharField(max_length=5, choices=INPUT_MODE_CHOICES, default="text")
    score = models.PositiveIntegerField(default=0)
    max_score = models.PositiveIntegerField(default=100)
    turn_count = models.PositiveIntegerField(default=0)
    hints_used = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    xp_earned = models.PositiveIntegerField(default=0)
    fluency_score = models.FloatField(default=0.0)
    accuracy_score = models.FloatField(default=0.0)
    vocabulary_score = models.FloatField(default=0.0)
    task_completion_score = models.FloatField(default=0.0)
    conversation_context = models.JSONField(default=list)

    class Meta:
        db_table = "immersive_sessions"
        ordering = ["-started_at"]
        verbose_name = "Immersive Session"
        verbose_name_plural = "Immersive Sessions"

    def __str__(self) -> str:
        return f"Immersive {self.scenario.location} by user {self.user_id}"


class ConversationTurn(AbstractBaseModel):
    """A single conversation turn in an immersive session."""

    ROLE_CHOICES = [("npc", "NPC"), ("user", "User")]
    INPUT_TYPE_CHOICES = [("text", "Text"), ("voice", "Voice")]

    session = models.ForeignKey(
        ImmersiveSession,
        on_delete=models.CASCADE,
        related_name="turns",
    )
    turn_number = models.PositiveIntegerField()
    role = models.CharField(max_length=4, choices=ROLE_CHOICES)
    content = models.TextField()
    audio_url = models.CharField(max_length=500, blank=True, default="")
    input_type = models.CharField(max_length=5, choices=INPUT_TYPE_CHOICES, default="text")

    # AI analysis results (for user turns only)
    grammar_errors = models.JSONField(default=list)
    vocabulary_feedback = models.JSONField(default=list)
    relevance_score = models.FloatField(default=0.0)
    grammar_score = models.FloatField(default=0.0)
    vocabulary_score_turn = models.FloatField(default=0.0)
    score = models.PositiveIntegerField(default=0)
    hint_level_used = models.PositiveIntegerField(default=0)
    response_time_ms = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = "conversation_turns"
        ordering = ["turn_number"]
        unique_together = ["session", "turn_number"]
        verbose_name = "Conversation Turn"
        verbose_name_plural = "Conversation Turns"

    def __str__(self) -> str:
        return f"Turn {self.turn_number} ({self.role}) in session {self.session_id}"
