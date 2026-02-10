"""
ConfusingPair Django ORM model — tracks word pairs that users frequently confuse.
"""

from django.conf import settings
from django.db import models

from apps.common.models import AbstractBaseModel


class ConfusingPair(AbstractBaseModel):
    """Tracks pairs of words that a user frequently confuses."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="confusing_pairs",
    )
    word_1 = models.ForeignKey(
        "Word",
        on_delete=models.CASCADE,
        related_name="confused_as_first",
    )
    word_2 = models.ForeignKey(
        "Word",
        on_delete=models.CASCADE,
        related_name="confused_as_second",
    )
    confusion_count = models.PositiveIntegerField(default=1)
    last_confused_at = models.DateTimeField(auto_now=True)
    is_resolved = models.BooleanField(default=False)
    drill_data = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "confusing_pairs"
        unique_together = ["user", "word_1", "word_2"]
        ordering = ["-confusion_count", "-last_confused_at"]
        verbose_name = "Confusing Pair"
        verbose_name_plural = "Confusing Pairs"

    def __str__(self) -> str:
        return f"Confusing: {self.word_1} <-> {self.word_2} (user {self.user_id})"
