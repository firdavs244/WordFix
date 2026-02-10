"""
DailyChallenge Django ORM model — daily challenge tasks for users.
"""

from django.conf import settings
from django.db import models

from apps.common.models import AbstractBaseModel


class DailyChallenge(AbstractBaseModel):
    """Daily challenge tasks generated for each user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="daily_challenges",
    )
    date = models.DateField()
    challenges = models.JSONField(default=list)
    all_completed = models.BooleanField(default=False)
    bonus_claimed = models.BooleanField(default=False)

    class Meta:
        db_table = "daily_challenges"
        unique_together = ["user", "date"]
        ordering = ["-date"]
        verbose_name = "Daily Challenge"
        verbose_name_plural = "Daily Challenges"

    def __str__(self) -> str:
        return f"Challenges for user {self.user_id} on {self.date}"
