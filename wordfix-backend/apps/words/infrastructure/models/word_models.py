"""
Word and WordCategory Django ORM models.
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


class WordDistractor(AbstractBaseModel):
    """Cached smart distractors for a word."""

    GENERATED_BY_CHOICES = [
        ("ai", "AI"),
        ("fallback", "Fallback"),
    ]

    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="distractors",
    )
    distractors = models.JSONField(default=list)
    language = models.CharField(max_length=10, default="uz")
    generated_by = models.CharField(
        max_length=10,
        choices=GENERATED_BY_CHOICES,
        default="ai",
    )

    class Meta:
        db_table = "word_distractors"
        unique_together = ["word", "language"]
        verbose_name = "Word Distractor"
        verbose_name_plural = "Word Distractors"

    def __str__(self) -> str:
        return f"Distractors for {self.word}: {self.distractors}"
