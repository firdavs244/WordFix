"""
Adaptive Intelligence models (Sprint 10).

Learning profile, mistake patterns, domain coverage, word recommendations,
and session performance tracking.
"""

import uuid

from django.db import models

from .user_models import CustomUser


class LearningProfile(models.Model):
    """Adaptive learning profile that stores style, schedule, and difficulty preferences."""

    STYLE_CHOICES = [
        ("visual", "Visual"),
        ("auditory", "Auditory"),
        ("reading", "Reading"),
        ("kinesthetic", "Kinesthetic"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="learning_profile",
    )
    preferred_style = models.CharField(
        max_length=15,
        choices=STYLE_CHOICES,
        default="visual",
    )
    style_confidence = models.FloatField(default=0.0)

    # Optimal study schedule
    best_hour_start = models.PositiveIntegerField(default=9)
    best_hour_end = models.PositiveIntegerField(default=12)
    best_days = models.JSONField(default=list, blank=True)  # e.g. [0,1,2,3,4]

    # Session stats
    avg_session_duration = models.PositiveIntegerField(default=15)  # minutes
    optimal_words_per_session = models.PositiveIntegerField(default=10)
    avg_retention_rate = models.FloatField(default=0.0)

    # Skills
    strongest_skills = models.JSONField(default=list, blank=True)
    weakest_skills = models.JSONField(default=list, blank=True)

    # Difficulty
    current_difficulty_level = models.FloatField(default=0.5)
    difficulty_adjustment_rate = models.FloatField(default=0.05)

    # Analysis
    last_analyzed_at = models.DateTimeField(null=True, blank=True)
    analysis_data = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "learning_profiles"
        verbose_name = "Learning Profile"
        verbose_name_plural = "Learning Profiles"

    def __str__(self) -> str:
        return f"LearningProfile({self.user.email}, style={self.preferred_style})"


class MistakePattern(models.Model):
    """Tracks recurring mistake patterns for a user."""

    PATTERN_TYPE_CHOICES = [
        ("l1_interference", "L1 Interference"),
        ("morphological", "Morphological"),
        ("semantic", "Semantic"),
        ("phonological", "Phonological"),
        ("spelling", "Spelling"),
        ("collocation", "Collocation"),
        ("grammar", "Grammar"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="mistake_patterns",
    )
    pattern_type = models.CharField(max_length=20, choices=PATTERN_TYPE_CHOICES)
    description = models.TextField(blank=True, default="")
    examples = models.JSONField(default=list, blank=True)
    occurrence_count = models.PositiveIntegerField(default=1)
    last_occurred_at = models.DateTimeField(auto_now=True)
    is_resolved = models.BooleanField(default=False)
    drills_completed = models.PositiveIntegerField(default=0)
    success_rate_after_drills = models.FloatField(default=0.0)
    related_words = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mistake_patterns"
        ordering = ["-occurrence_count"]
        indexes = [
            models.Index(fields=["user", "pattern_type"]),
            models.Index(fields=["user", "is_resolved"]),
        ]
        verbose_name = "Mistake Pattern"
        verbose_name_plural = "Mistake Patterns"

    def __str__(self) -> str:
        return f"MistakePattern({self.user.email}, {self.pattern_type}, count={self.occurrence_count})"


class DomainCoverage(models.Model):
    """Tracks how well a user covers each vocabulary domain."""

    DOMAIN_CHOICES = [
        ("academic", "Academic"),
        ("business", "Business"),
        ("technology", "Technology"),
        ("daily_life", "Daily Life"),
        ("science", "Science"),
        ("arts", "Arts"),
        ("travel", "Travel"),
        ("medical", "Medical"),
        ("legal", "Legal"),
        ("social", "Social"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="domain_coverages",
    )
    domain = models.CharField(max_length=15, choices=DOMAIN_CHOICES)
    total_words_in_domain = models.PositiveIntegerField(default=0)
    coverage_percentage = models.FloatField(default=0.0)
    mastered_count = models.PositiveIntegerField(default=0)
    learning_count = models.PositiveIntegerField(default=0)
    last_updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "domain_coverages"
        unique_together = ["user", "domain"]
        verbose_name = "Domain Coverage"
        verbose_name_plural = "Domain Coverages"

    def __str__(self) -> str:
        return f"DomainCoverage({self.user.email}, {self.domain}, {self.coverage_percentage:.0f}%)"


class WordRecommendation(models.Model):
    """AI-generated word recommendations for a user."""

    REASON_TYPE_CHOICES = [
        ("domain_gap", "Domain Gap"),
        ("confusion_fix", "Confusion Fix"),
        ("level_appropriate", "Level Appropriate"),
        ("high_frequency", "High Frequency"),
        ("user_interest", "User Interest"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="word_recommendations",
    )
    recommended_word = models.CharField(max_length=100)
    translation = models.CharField(max_length=200, blank=True, default="")
    reason = models.TextField(blank=True, default="")
    reason_type = models.CharField(max_length=20, choices=REASON_TYPE_CHOICES, default="level_appropriate")
    priority_score = models.FloatField(default=0.5)
    is_accepted = models.BooleanField(default=False)
    is_dismissed = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(null=True, blank=True)
    ai_confidence = models.FloatField(default=0.0)
    source_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "word_recommendations"
        ordering = ["-priority_score", "-created_at"]
        indexes = [
            models.Index(fields=["user", "recommended_word"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recommended_word"],
                condition=models.Q(is_accepted=False, is_dismissed=False),
                name="unique_active_recommendation_per_user",
            ),
        ]
        verbose_name = "Word Recommendation"
        verbose_name_plural = "Word Recommendations"

    def __str__(self) -> str:
        return f"Recommendation({self.user.email}, '{self.recommended_word}', score={self.priority_score})"


class SessionPerformance(models.Model):
    """Records performance metrics for each study session."""

    SESSION_TYPE_CHOICES = [
        ("review", "Review"),
        ("test", "Test"),
        ("game", "Game"),
        ("chat", "Chat"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="session_performances",
    )
    session_type = models.CharField(max_length=10, choices=SESSION_TYPE_CHOICES)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    hour_of_day = models.PositiveIntegerField(default=0)  # 0-23
    day_of_week = models.PositiveIntegerField(default=0)  # 0=Mon, 6=Sun
    accuracy = models.FloatField(default=0.0)
    completion_rate = models.FloatField(default=0.0)
    engagement_score = models.FloatField(default=0.0)
    effectiveness_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "session_performances"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "hour_of_day"]),
            models.Index(fields=["user", "day_of_week"]),
        ]
        verbose_name = "Session Performance"
        verbose_name_plural = "Session Performances"

    def __str__(self) -> str:
        return f"SessionPerformance({self.user.email}, {self.session_type}, eff={self.effectiveness_score:.2f})"
