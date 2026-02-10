"""
ChatSession and ChatMessage Django ORM models.
"""

from django.conf import settings
from django.db import models

from apps.common.models import AbstractBaseModel


class ChatSession(AbstractBaseModel):
    """AI Chat session for conversation practice."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_sessions",
    )
    topic = models.CharField(max_length=200, blank=True, default="")
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    message_count = models.PositiveIntegerField(default=0)
    words_practiced = models.ManyToManyField(
        "Word",
        related_name="chat_sessions",
        blank=True,
    )
    target_words = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "chat_sessions"
        ordering = ["-started_at"]
        verbose_name = "Chat Session"
        verbose_name_plural = "Chat Sessions"

    def __str__(self) -> str:
        return f"Chat '{self.topic}' by user {self.user_id}"


class ChatMessage(AbstractBaseModel):
    """Individual message within a chat session."""

    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
    ]

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    corrections = models.JSONField(default=list, blank=True)
    words_used = models.JSONField(default=list, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "chat_messages"
        ordering = ["order"]
        verbose_name = "Chat Message"
        verbose_name_plural = "Chat Messages"

    def __str__(self) -> str:
        return f"{self.role}: {self.content[:50]}"
