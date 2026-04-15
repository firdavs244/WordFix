"""
ImmersiveScenario and NPCCharacter Django ORM models.
"""

from django.db import models

from apps.common.models import AbstractBaseModel


class ImmersiveScenario(AbstractBaseModel):
    """Pre-defined immersive learning scenario."""

    LOCATION_CHOICES = [
        ("office", "Office"),
        ("restaurant", "Restaurant"),
        ("airport", "Airport"),
        ("hospital", "Hospital"),
        ("school", "School"),
        ("hotel", "Hotel"),
        ("shop", "Shop"),
        ("bank", "Bank"),
        ("park", "Park"),
        ("gym", "Gym"),
    ]

    DIFFICULTY_CHOICES = [
        ("A1", "Beginner"),
        ("A2", "Elementary"),
        ("B1", "Intermediate"),
        ("B2", "Upper Intermediate"),
        ("C1", "Advanced"),
        ("C2", "Proficient"),
    ]

    name = models.CharField(max_length=100)
    name_uz = models.CharField(max_length=100)
    description = models.TextField()
    description_uz = models.TextField()
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    difficulty = models.CharField(max_length=2, choices=DIFFICULTY_CHOICES)
    scene_config = models.JSONField(default=dict)
    target_vocabulary = models.JSONField(default=list)
    expected_phrases = models.JSONField(default=list)
    max_turns = models.PositiveIntegerField(default=8)
    time_limit_seconds = models.PositiveIntegerField(default=600)
    xp_reward = models.PositiveIntegerField(default=50)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "immersive_scenarios"
        ordering = ["order", "difficulty"]
        verbose_name = "Immersive Scenario"
        verbose_name_plural = "Immersive Scenarios"

    def __str__(self) -> str:
        return f"{self.name} ({self.location}/{self.difficulty})"


class NPCCharacter(AbstractBaseModel):
    """NPC character in an immersive scenario."""

    scenario = models.ForeignKey(
        ImmersiveScenario,
        on_delete=models.CASCADE,
        related_name="npcs",
    )
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=100)
    role_uz = models.CharField(max_length=100)
    personality = models.TextField()
    avatar_config = models.JSONField(default=dict)
    initial_greeting = models.TextField()
    system_prompt = models.TextField()
    voice_config = models.JSONField(default=dict)

    class Meta:
        db_table = "npc_characters"
        ordering = ["name"]
        verbose_name = "NPC Character"
        verbose_name_plural = "NPC Characters"

    def __str__(self) -> str:
        return f"{self.name} ({self.role})"
