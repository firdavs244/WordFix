"""
Word and category serializers.
"""

from rest_framework import serializers


class WordCategorySerializer(serializers.Serializer):
    """Word category serializer."""

    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=50)
    color = serializers.CharField(max_length=7, required=False, default="#6C5CE7")
    icon = serializers.CharField(max_length=50, required=False, default="book")
    words_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class WordCreateSerializer(serializers.Serializer):
    """Serializer for creating a word."""

    original_word = serializers.CharField(max_length=100)
    translation = serializers.CharField(required=False, default="", allow_blank=True)
    category_id = serializers.UUIDField(required=False, allow_null=True)
    difficulty_level = serializers.ChoiceField(
        choices=["easy", "medium", "hard"],
        required=False,
        default="medium",
    )
    notes = serializers.CharField(required=False, default="", allow_blank=True)
    tags = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
    pronunciation = serializers.CharField(required=False, default="", allow_blank=True)
    part_of_speech = serializers.ChoiceField(
        choices=["noun", "verb", "adjective", "adverb", "preposition",
                 "conjunction", "pronoun", "interjection", "phrase", "other", ""],
        required=False,
        default="",
    )
    definition = serializers.CharField(required=False, default="", allow_blank=True)
    example_sentence = serializers.CharField(required=False, default="", allow_blank=True)

    def validate_original_word(self, value: str) -> str:
        return value.strip().lower()


class WordUpdateSerializer(serializers.Serializer):
    """Serializer for updating a word (all fields optional)."""

    translation = serializers.CharField(required=False, allow_blank=True)
    pronunciation = serializers.CharField(required=False, allow_blank=True)
    part_of_speech = serializers.ChoiceField(
        choices=["noun", "verb", "adjective", "adverb", "preposition",
                 "conjunction", "pronoun", "interjection", "phrase", "other", ""],
        required=False,
    )
    definition = serializers.CharField(required=False, allow_blank=True)
    example_sentence = serializers.CharField(required=False, allow_blank=True)
    example_translation = serializers.CharField(required=False, allow_blank=True)
    synonyms = serializers.ListField(child=serializers.CharField(), required=False)
    antonyms = serializers.ListField(child=serializers.CharField(), required=False)
    collocations = serializers.ListField(child=serializers.CharField(), required=False)
    word_family = serializers.ListField(child=serializers.CharField(), required=False)
    notes = serializers.CharField(required=False, allow_blank=True)
    category_id = serializers.UUIDField(required=False, allow_null=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    difficulty_level = serializers.ChoiceField(
        choices=["easy", "medium", "hard"], required=False,
    )
    is_mastered = serializers.BooleanField(required=False)
    confidence_score = serializers.FloatField(required=False, min_value=0, max_value=100)


class WordListSerializer(serializers.Serializer):
    """Serializer for word list items."""

    id = serializers.UUIDField()
    original_word = serializers.CharField()
    translation = serializers.CharField()
    confidence_score = serializers.FloatField()
    category = WordCategorySerializer(allow_null=True)
    difficulty_level = serializers.CharField()
    is_mastered = serializers.BooleanField()
    is_enriched = serializers.BooleanField()
    part_of_speech = serializers.CharField()
    review_count = serializers.IntegerField()
    created_at = serializers.DateTimeField()


class WordDetailSerializer(serializers.Serializer):
    """Serializer for word detail (all fields)."""

    id = serializers.UUIDField()
    original_word = serializers.CharField()
    translation = serializers.CharField()
    pronunciation = serializers.CharField()
    part_of_speech = serializers.CharField()
    definition = serializers.CharField()
    example_sentence = serializers.CharField()
    example_translation = serializers.CharField()
    synonyms = serializers.ListField()
    antonyms = serializers.ListField()
    collocations = serializers.ListField()
    word_family = serializers.ListField()
    image_url = serializers.CharField()
    audio_url = serializers.CharField()
    notes = serializers.CharField()
    mnemonic = serializers.CharField(allow_blank=True)
    usage_notes = serializers.CharField(allow_blank=True)
    category = WordCategorySerializer(allow_null=True)
    tags = serializers.ListField()
    difficulty_level = serializers.CharField()
    is_enriched = serializers.BooleanField()
    enrichment_status = serializers.CharField()
    enrichment_error = serializers.CharField(allow_blank=True)
    enriched_at = serializers.DateTimeField(allow_null=True)
    confidence_score = serializers.FloatField()
    next_review_at = serializers.DateTimeField(allow_null=True)
    review_count = serializers.IntegerField()
    correct_count = serializers.IntegerField()
    incorrect_count = serializers.IntegerField()
    last_reviewed_at = serializers.DateTimeField(allow_null=True)
    is_mastered = serializers.BooleanField()
    easiness_factor = serializers.FloatField()
    repetition_number = serializers.IntegerField()
    interval_days = serializers.IntegerField()
    accuracy_rate = serializers.FloatField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class WordStatsSerializer(serializers.Serializer):
    """Serializer for word stats."""

    total = serializers.IntegerField()
    mastered = serializers.IntegerField()
    learning = serializers.IntegerField()
    new = serializers.IntegerField()
    by_difficulty = serializers.DictField()
    by_category = serializers.ListField()
    average_confidence = serializers.FloatField()


class BulkWordCreateSerializer(serializers.Serializer):
    """Serializer for bulk word creation."""

    words = serializers.ListField(
        child=serializers.DictField(),
        min_length=1,
        max_length=100,
    )
