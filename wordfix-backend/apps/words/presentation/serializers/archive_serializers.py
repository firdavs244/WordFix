"""
Archive serializers for word archiving endpoints.
"""

from rest_framework import serializers


class BulkArchiveSerializer(serializers.Serializer):
    """Serializer for bulk archive request."""

    word_ids = serializers.ListField(
        child=serializers.UUIDField(),
        min_length=1,
        max_length=100,
        help_text="List of word UUIDs to archive.",
    )


class ArchivedWordSerializer(serializers.Serializer):
    """Serializer for archived word response."""

    id = serializers.UUIDField()
    original_word = serializers.CharField()
    translation = serializers.CharField()
    pronunciation = serializers.CharField()
    part_of_speech = serializers.CharField()
    definition = serializers.CharField()
    difficulty_level = serializers.CharField()
    confidence_score = serializers.FloatField()
    is_mastered = serializers.BooleanField()
    is_archived = serializers.BooleanField()
    archived_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
