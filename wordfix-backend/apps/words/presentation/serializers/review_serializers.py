"""
Review and enrichment serializers.
"""

from rest_framework import serializers


class ReviewSubmitSerializer(serializers.Serializer):
    """Serializer for submitting a review answer."""

    word_id = serializers.UUIDField()
    quality = serializers.IntegerField(min_value=0, max_value=5)
    response_time_ms = serializers.IntegerField(required=False, default=0, min_value=0)


class ReviewSessionCreateSerializer(serializers.Serializer):
    """Serializer for creating a review session."""

    session_type = serializers.ChoiceField(
        choices=["review", "quick", "focus"],
        required=False,
        default="review",
    )


class EnrichWordSerializer(serializers.Serializer):
    """Serializer for enriching a word."""

    word_id = serializers.UUIDField()


class BatchEnrichSerializer(serializers.Serializer):
    """Serializer for batch enrichment."""

    word_ids = serializers.ListField(
        child=serializers.UUIDField(),
        min_length=1,
        max_length=50,
    )
