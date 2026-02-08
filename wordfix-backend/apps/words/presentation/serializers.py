"""
Word serializers.
"""

from dataclasses import asdict

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


# =============================================================================
# REVIEW & ENRICHMENT SERIALIZERS
# =============================================================================


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


# =============================================================================
# TEST SERIALIZERS
# =============================================================================


class TestGenerateSerializer(serializers.Serializer):
    """Serializer for generating a test."""

    test_type = serializers.ChoiceField(
        choices=["multiple_choice", "fill_blank", "context_guess", "mixed"],
        default="mixed",
    )
    question_count = serializers.IntegerField(
        min_value=5, max_value=30, default=10,
    )
    difficulty = serializers.ChoiceField(
        choices=["easy", "medium", "hard", "adaptive"],
        default="adaptive",
    )


class TestQuestionSerializer(serializers.Serializer):
    """Serializer for a test question."""

    id = serializers.UUIDField()
    question_type = serializers.CharField()
    question_text = serializers.CharField()
    options = serializers.ListField(child=serializers.CharField(), default=list)
    order = serializers.IntegerField()
    user_answer = serializers.CharField(allow_blank=True)
    is_correct = serializers.BooleanField(allow_null=True)
    correct_answer = serializers.SerializerMethodField()
    explanation = serializers.SerializerMethodField()

    def get_correct_answer(self, obj):
        """Only show correct answer after user has answered."""
        if hasattr(obj, "user_answer") and obj.user_answer:
            return obj.correct_answer
        return None

    def get_explanation(self, obj):
        """Only show explanation after user has answered."""
        if hasattr(obj, "user_answer") and obj.user_answer:
            return obj.explanation
        return None


class TestSessionSerializer(serializers.Serializer):
    """Serializer for a test session."""

    id = serializers.UUIDField()
    test_type = serializers.CharField()
    difficulty = serializers.CharField()
    total_questions = serializers.IntegerField()
    correct_answers = serializers.IntegerField()
    incorrect_answers = serializers.IntegerField()
    score_percentage = serializers.FloatField()
    duration_seconds = serializers.IntegerField()
    is_completed = serializers.BooleanField()
    started_at = serializers.DateTimeField()
    completed_at = serializers.DateTimeField(allow_null=True)
    created_at = serializers.DateTimeField()


class TestSessionDetailSerializer(serializers.Serializer):
    """Serializer for test session detail with questions."""

    session = TestSessionSerializer()
    questions = TestQuestionSerializer(many=True)


class TestAnswerSubmitSerializer(serializers.Serializer):
    """Serializer for submitting a test answer."""

    question_id = serializers.UUIDField()
    answer = serializers.CharField()
    response_time_ms = serializers.IntegerField(required=False, default=0, min_value=0)


# =============================================================================
# GAME SERIALIZERS
# =============================================================================


class GameSessionSerializer(serializers.Serializer):
    """Serializer for a game session."""

    id = serializers.UUIDField()
    game_type = serializers.CharField()
    score = serializers.IntegerField()
    max_score = serializers.IntegerField()
    correct_answers = serializers.IntegerField()
    incorrect_answers = serializers.IntegerField()
    duration_seconds = serializers.IntegerField()
    is_completed = serializers.BooleanField()
    level = serializers.IntegerField()
    xp_earned = serializers.IntegerField()
    started_at = serializers.DateTimeField()
    completed_at = serializers.DateTimeField(allow_null=True)
    created_at = serializers.DateTimeField()


class SpeedRoundStartSerializer(serializers.Serializer):
    """Response serializer for speed round start."""

    session_id = serializers.CharField()
    words = serializers.ListField()
    time_limit = serializers.IntegerField()


class SpeedRoundSubmitSerializer(serializers.Serializer):
    """Serializer for speed round submission."""

    session_id = serializers.UUIDField()
    answers = serializers.ListField(
        child=serializers.DictField(),
    )
    duration_seconds = serializers.IntegerField(default=60, min_value=0)


class WordMatchStartSerializer(serializers.Serializer):
    """Response serializer for word match start."""

    session_id = serializers.CharField()
    words = serializers.ListField()
    translations = serializers.ListField()
    pair_count = serializers.IntegerField()


class WordMatchSubmitSerializer(serializers.Serializer):
    """Serializer for word match submission."""

    session_id = serializers.UUIDField()
    pairs = serializers.ListField(
        child=serializers.DictField(),
    )
    time_seconds = serializers.IntegerField(min_value=0)


class WordContextSubmitSerializer(serializers.Serializer):
    """Serializer for word context submission."""

    session_id = serializers.UUIDField()
    answers = serializers.ListField(
        child=serializers.DictField(),
    )


class GameStatsSerializer(serializers.Serializer):
    """Serializer for game stats."""

    total_games = serializers.IntegerField()
    total_xp = serializers.IntegerField()
    favorite_game = serializers.CharField(allow_null=True)
    by_type = serializers.DictField()
