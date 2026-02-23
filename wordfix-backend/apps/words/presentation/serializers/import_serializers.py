"""
Smart import serializers.
"""

from rest_framework import serializers


class AnalyzeTextSerializer(serializers.Serializer):
    """Serializer for text analysis request."""

    text = serializers.CharField(max_length=5000, min_length=1)
    max_words = serializers.IntegerField(default=50, min_value=1, max_value=100)

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
    definition = serializers.CharField(allow_blank=True, default="")
    pronunciation = serializers.CharField(allow_blank=True, default="")
    in_user_library = serializers.BooleanField(default=False)


class AnalyzeTextResponseSerializer(serializers.Serializer):
    """Serializer for analyze text response."""

    suggestions = WordSuggestionSerializer(many=True)
    parse_mode = serializers.CharField(default="fallback")
    total_found = serializers.IntegerField(default=0)
    already_in_library = serializers.IntegerField(default=0)
    text_difficulty = serializers.CharField(default="A1")


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


class CSVUploadSerializer(serializers.Serializer):
    """CSV file upload serializer."""

    file = serializers.FileField()

    def validate_file(self, value):
        if value.size > 1024 * 1024:  # 1MB
            raise serializers.ValidationError("File too large (max 1MB).")
        if not value.name.endswith(".csv"):
            raise serializers.ValidationError("Only CSV files are accepted.")
        return value


class CSVValidateResultSerializer(serializers.Serializer):
    """CSV validation result serializer."""

    headers = serializers.ListField()
    preview = serializers.ListField()
    total_rows = serializers.IntegerField()
    valid_rows = serializers.IntegerField()
    errors = serializers.ListField()
    has_translation = serializers.BooleanField()
    has_difficulty = serializers.BooleanField()
    has_category = serializers.BooleanField()


class CSVImportResultSerializer(serializers.Serializer):
    """CSV import result serializer."""

    total_in_file = serializers.IntegerField()
    imported = serializers.IntegerField()
    skipped_duplicate = serializers.IntegerField()
    skipped_invalid = serializers.IntegerField()
    errors = serializers.ListField()
    categories_created = serializers.ListField()
