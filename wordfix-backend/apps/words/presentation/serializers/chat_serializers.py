"""
Chat serializers.
"""

from rest_framework import serializers


class StartChatSerializer(serializers.Serializer):
    """Serializer for starting a chat session."""

    topic = serializers.CharField(required=False, allow_blank=True, default="")


class ChatMessageSerializer(serializers.Serializer):
    """Serializer for sending a chat message."""

    message = serializers.CharField(min_length=1, max_length=2000)


class ChatSessionListSerializer(serializers.Serializer):
    """Serializer for chat session list."""

    id = serializers.UUIDField()
    topic = serializers.CharField()
    message_count = serializers.IntegerField()
    target_words = serializers.ListField()
    is_active = serializers.BooleanField()
    started_at = serializers.DateTimeField()
    ended_at = serializers.DateTimeField(allow_null=True)
    created_at = serializers.DateTimeField()
