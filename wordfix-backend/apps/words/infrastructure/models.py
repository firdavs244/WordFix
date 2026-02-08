"""
Word, WordCategory, ReviewSession, ReviewLog, DailyStreak, DailyActivity,
TestSession, TestQuestion, GameSession Django ORM models.
"""

import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

from apps.common.models import AbstractBaseModel


class WordCategory(AbstractBaseModel):
    """Word category model."""

    color_validator = RegexValidator(
        regex=r"^#[0-9A-Fa-f]{6}$",
        message="Color must be a valid hex color code (e.g., #6C5CE7).",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="word_categories",
    )
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default="#6C5CE7", validators=[color_validator])
    icon = models.CharField(max_length=50, default="book")
    words_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "word_categories"
        unique_together = ["user", "name"]
        ordering = ["name"]
        verbose_name = "Word Category"
        verbose_name_plural = "Word Categories"

    def __str__(self) -> str:
        return self.name


class Word(AbstractBaseModel):
    """Word model — the core vocabulary item."""

    PART_OF_SPEECH_CHOICES = [
        ("noun", "Noun"),
        ("verb", "Verb"),
        ("adjective", "Adjective"),
        ("adverb", "Adverb"),
        ("preposition", "Preposition"),
        ("conjunction", "Conjunction"),
        ("pronoun", "Pronoun"),
        ("interjection", "Interjection"),
        ("phrase", "Phrase"),
        ("other", "Other"),
    ]

    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    ENRICHMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("enriching", "Enriching"),
        ("enriched", "Enriched"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="words",
        db_index=True,
    )
    original_word = models.CharField(max_length=100, db_index=True)
    translation = models.CharField(max_length=200, blank=True, default="")
    pronunciation = models.CharField(max_length=200, blank=True, default="")
    part_of_speech = models.CharField(
        max_length=15,
        choices=PART_OF_SPEECH_CHOICES,
        blank=True,
        default="",
    )
    definition = models.TextField(blank=True, default="")
    example_sentence = models.TextField(blank=True, default="")
    example_translation = models.TextField(blank=True, default="")
    synonyms = models.JSONField(default=list, blank=True)
    antonyms = models.JSONField(default=list, blank=True)
    collocations = models.JSONField(default=list, blank=True)
    word_family = models.JSONField(default=list, blank=True)
    image_url = models.URLField(blank=True, default="")
    audio_url = models.URLField(blank=True, default="")
    notes = models.TextField(blank=True, default="")
    mnemonic = models.TextField(blank=True, default="")
    usage_notes = models.TextField(blank=True, default="")
    category = models.ForeignKey(
        WordCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="words",
    )
    tags = models.JSONField(default=list, blank=True)
    difficulty_level = models.CharField(
        max_length=6,
        choices=DIFFICULTY_CHOICES,
        default="medium",
    )
    is_enriched = models.BooleanField(default=False)
    enrichment_status = models.CharField(
        max_length=10,
        choices=ENRICHMENT_STATUS_CHOICES,
        default="pending",
        db_index=True,
    )
    enrichment_error = models.TextField(blank=True, default="")
    enriched_at = models.DateTimeField(null=True, blank=True)
    confidence_score = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    next_review_at = models.DateTimeField(null=True, blank=True)
    review_count = models.PositiveIntegerField(default=0)
    correct_count = models.PositiveIntegerField(default=0)
    incorrect_count = models.PositiveIntegerField(default=0)
    last_reviewed_at = models.DateTimeField(null=True, blank=True)
    is_mastered = models.BooleanField(default=False)
    # SM-2 fields
    easiness_factor = models.FloatField(default=2.5)
    repetition_number = models.PositiveIntegerField(default=0)
    interval_days = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "words"
        unique_together = ["user", "original_word"]
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "is_mastered"]),
            models.Index(fields=["user", "confidence_score"]),
            models.Index(fields=["user", "next_review_at"]),
            models.Index(fields=["user", "category"]),
        ]
        verbose_name = "Word"
        verbose_name_plural = "Words"

    def __str__(self) -> str:
        return self.original_word

    def clean(self) -> None:
        super().clean()
        if self.original_word:
            self.original_word = self.original_word.strip().lower()

    def save(self, *args, **kwargs):
        if self.original_word:
            self.original_word = self.original_word.strip().lower()
        super().save(*args, **kwargs)

    @property
    def accuracy_rate(self) -> float:
        """Calculate accuracy rate from review stats."""
        if self.review_count == 0:
            return 0.0
        return round((self.correct_count / self.review_count) * 100, 1)


class ReviewSession(AbstractBaseModel):
    """A review session tracking user's study activity."""

    SESSION_TYPE_CHOICES = [
        ("review", "Review"),
        ("quick", "Quick"),
        ("focus", "Focus"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="review_sessions",
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    total_words = models.PositiveIntegerField(default=0)
    correct_count = models.PositiveIntegerField(default=0)
    incorrect_count = models.PositiveIntegerField(default=0)
    average_quality = models.FloatField(default=0.0)
    duration_seconds = models.PositiveIntegerField(default=0)
    session_type = models.CharField(
        max_length=10,
        choices=SESSION_TYPE_CHOICES,
        default="review",
    )
    is_completed = models.BooleanField(default=False)

    class Meta:
        db_table = "review_sessions"
        ordering = ["-started_at"]
        verbose_name = "Review Session"
        verbose_name_plural = "Review Sessions"

    def __str__(self) -> str:
        return f"Review {self.session_type} by user {self.user_id} at {self.started_at}"


class ReviewLog(AbstractBaseModel):
    """Individual word review log within a session."""

    session = models.ForeignKey(
        ReviewSession,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logs",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="review_logs",
    )
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="review_logs",
    )
    quality = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    response_time_ms = models.PositiveIntegerField(null=True, blank=True)
    is_correct = models.BooleanField()
    reviewed_at = models.DateTimeField(auto_now_add=True)
    previous_confidence = models.FloatField(default=0.0)
    new_confidence = models.FloatField(default=0.0)
    previous_interval = models.PositiveIntegerField(default=0)
    new_interval = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "review_logs"
        ordering = ["-reviewed_at"]
        verbose_name = "Review Log"
        verbose_name_plural = "Review Logs"

    def __str__(self) -> str:
        return f"Review of '{self.word}' quality={self.quality}"


class DailyStreak(AbstractBaseModel):
    """Tracks consecutive daily study streaks for a user."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="streak",
    )
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    streak_frozen_until = models.DateField(null=True, blank=True)
    total_review_days = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "daily_streaks"
        verbose_name = "Daily Streak"
        verbose_name_plural = "Daily Streaks"

    def __str__(self) -> str:
        return f"Streak {self.current_streak} days for user {self.user_id}"


class DailyActivity(AbstractBaseModel):
    """Tracks daily learning activity for a user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="daily_activities",
    )
    date = models.DateField()
    words_reviewed = models.PositiveIntegerField(default=0)
    words_added = models.PositiveIntegerField(default=0)
    words_mastered = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    incorrect_answers = models.PositiveIntegerField(default=0)
    total_time_seconds = models.PositiveIntegerField(default=0)
    goal_completed = models.BooleanField(default=False)
    xp_earned = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "daily_activities"
        unique_together = ["user", "date"]
        ordering = ["-date"]
        verbose_name = "Daily Activity"
        verbose_name_plural = "Daily Activities"

    def __str__(self) -> str:
        return f"Activity for user {self.user_id} on {self.date}"


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
        Word,
        through="TestQuestion",
        related_name="test_sessions",
        blank=True,
    )

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
        Word,
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

    class Meta:
        db_table = "game_sessions"
        ordering = ["-started_at"]
        verbose_name = "Game Session"
        verbose_name_plural = "Game Sessions"

    def __str__(self) -> str:
        return f"Game {self.game_type} by user {self.user_id}"
