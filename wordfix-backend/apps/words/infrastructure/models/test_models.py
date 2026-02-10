"""
TestSession and TestQuestion Django ORM models.
"""

from django.conf import settings
from django.db import models

from apps.common.models import AbstractBaseModel


class TestSession(AbstractBaseModel):
    """AI-generated test session."""

    TEST_TYPE_CHOICES = [
        ("multiple_choice", "Multiple Choice"),
        ("fill_blank", "Fill in the Blank"),
        ("context_guess", "Context Guess"),
        ("mixed", "Mixed"),
    ]

    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
        ("adaptive", "Adaptive"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="test_sessions",
    )
    test_type = models.CharField(max_length=20, choices=TEST_TYPE_CHOICES)
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default="adaptive",
    )
    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    incorrect_answers = models.PositiveIntegerField(default=0)
    score_percentage = models.FloatField(default=0.0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    words_tested = models.ManyToManyField(
        "Word",
        through="TestQuestion",
        related_name="test_sessions",
        blank=True,
    )
    current_combo = models.PositiveIntegerField(default=0)
    max_combo = models.PositiveIntegerField(default=0)
    combo_xp_bonus = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "test_sessions"
        ordering = ["-started_at"]
        verbose_name = "Test Session"
        verbose_name_plural = "Test Sessions"

    def __str__(self) -> str:
        return f"Test {self.test_type} by user {self.user_id}"


class TestQuestion(AbstractBaseModel):
    """Individual question within a test session."""

    QUESTION_TYPE_CHOICES = [
        ("multiple_choice", "Multiple Choice"),
        ("fill_blank", "Fill in the Blank"),
        ("context_guess", "Context Guess"),
        ("word_to_translation", "Word to Translation"),
        ("translation_to_word", "Translation to Word"),
        ("listen_and_type", "Listen and Type"),
    ]

    session = models.ForeignKey(
        TestSession,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    word = models.ForeignKey(
        "Word",
        on_delete=models.CASCADE,
        related_name="test_questions",
    )
    question_type = models.CharField(max_length=25, choices=QUESTION_TYPE_CHOICES)
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=500)
    options = models.JSONField(default=list, blank=True)
    user_answer = models.CharField(max_length=500, blank=True, default="")
    is_correct = models.BooleanField(null=True, blank=True)
    response_time_ms = models.PositiveIntegerField(null=True, blank=True)
    explanation = models.TextField(blank=True, default="")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "test_questions"
        ordering = ["order"]
        verbose_name = "Test Question"
        verbose_name_plural = "Test Questions"

    def __str__(self) -> str:
        return f"Q{self.order}: {self.question_text[:50]}"
