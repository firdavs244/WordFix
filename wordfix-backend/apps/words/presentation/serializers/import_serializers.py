"""
Smart import serializers.
"""

from rest_framework import serializers


class AnalyzeTextSerializer(serializers.Serializer):
    """Serializer for text analysis request."""

    text = serializers.CharField(max_length=5000, min_length=1)
    max_words = serializers.IntegerField(default=20, min_value=1, max_value=50)

    def validate_text(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("Text cannot be empty.")
        return value.strip()


class WordSuggestionSerializer(serializers.Serializer):
    """Serializer for a word suggestion from analysis."""

    word = serializers.CharField()
    translation = serializers.CharField(allow_blank=True, default="")
    part_of_speech = serializers.CharField(allow_blank=True, default="")
    context_sentence = serializers.CharField(allow_blank=True, default="")
    difficulty = serializers.CharField(default="medium")
    reason = serializers.CharField(allow_blank=True, default="")


class ImportWordsSerializer(serializers.Serializer):
    """Serializer for importing selected words."""

    words = serializers.ListField(
        child=serializers.DictField(),
        min_length=1,
    )

    def validate_words(self, value):
        for word_data in value:
            if not word_data.get("original_word", "").strip():
                raise serializers.ValidationError("Each word must have an 'original_word' field.")
        return value
