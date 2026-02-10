"""
Confusing pairs serializers.
"""

from rest_framework import serializers


class ConfusingPairWordSerializer(serializers.Serializer):
    """Nested serializer for word info within a confusing pair."""

    id = serializers.UUIDField()
    original_word = serializers.CharField()
    translation = serializers.CharField()


class ConfusingPairSerializer(serializers.Serializer):
    """Serializer for a confusing pair."""

    id = serializers.CharField()
    word_1 = ConfusingPairWordSerializer()
    word_2 = ConfusingPairWordSerializer()
    confusion_count = serializers.IntegerField()
    last_confused_at = serializers.CharField(allow_null=True)
    is_resolved = serializers.BooleanField()


class ConfusingPairDetailSerializer(serializers.Serializer):
    """Serializer for confusing pair detail with drill data."""

    id = serializers.CharField()
    word_1 = serializers.DictField()
    word_2 = serializers.DictField()
    confusion_count = serializers.IntegerField()
    last_confused_at = serializers.CharField(allow_null=True)
    is_resolved = serializers.BooleanField()
    drill_data = serializers.DictField(default=dict)


class ConfusingPairDrillSerializer(serializers.Serializer):
    """Serializer for drill data."""

    explanation = serializers.CharField()
    word_1_examples = serializers.ListField(default=list)
    word_2_examples = serializers.ListField(default=list)
    mnemonic = serializers.CharField(default="")
    test_questions = serializers.ListField(default=list)


class ConfusingPairCountSerializer(serializers.Serializer):
    """Serializer for unresolved count."""

    count = serializers.IntegerField()
