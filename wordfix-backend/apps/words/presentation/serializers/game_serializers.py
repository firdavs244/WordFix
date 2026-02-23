"""
Game serializers.
"""

from rest_framework import serializers


class GameSessionSerializer(serializers.Serializer):
    """Serializer for a game session."""

    id = serializers.UUIDField()
    game_type = serializers.CharField()
    score = serializers.IntegerField()
    max_score = serializers.IntegerField()
    correct_answers = serializers.IntegerField()
    incorrect_answers = serializers.IntegerField()
    total_questions = serializers.SerializerMethodField()
    duration_seconds = serializers.IntegerField()
    is_completed = serializers.BooleanField()
    level = serializers.IntegerField()
    xp_earned = serializers.IntegerField()
    current_combo = serializers.IntegerField()
    max_combo = serializers.IntegerField()
    combo_xp_bonus = serializers.IntegerField()
    started_at = serializers.DateTimeField()
    completed_at = serializers.DateTimeField(allow_null=True)
    created_at = serializers.DateTimeField()

    def get_total_questions(self, obj) -> int:
        return (getattr(obj, 'correct_answers', 0) or 0) + (getattr(obj, 'incorrect_answers', 0) or 0)


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


# =============================================================================
# Story Builder serializers
# =============================================================================


class StoryBuilderStartSerializer(serializers.Serializer):
    """Request serializer for starting story builder."""
    genre = serializers.CharField(required=False, default="", allow_blank=True)


class StoryBuilderStartResponseSerializer(serializers.Serializer):
    """Response serializer for story builder start."""
    session_id = serializers.UUIDField()
    genre = serializers.CharField()
    ai_text = serializers.CharField()
    target_words = serializers.ListField(child=serializers.CharField())
    total_rounds = serializers.IntegerField()
    current_round = serializers.IntegerField()
    all_target_words = serializers.ListField(child=serializers.CharField())


class StoryRoundSubmitSerializer(serializers.Serializer):
    """Request serializer for submitting a story round."""
    session_id = serializers.UUIDField()
    user_text = serializers.CharField(min_length=10, max_length=500)


class StoryRoundResultSerializer(serializers.Serializer):
    """Response serializer for story round result."""
    round_result = serializers.DictField()
    next_round = serializers.DictField(allow_null=True)
    session_stats = serializers.DictField()
    combo = serializers.IntegerField()
    multiplier = serializers.FloatField()
    xp_earned = serializers.IntegerField()


class StoryBuilderCompleteSerializer(serializers.Serializer):
    """Request serializer for completing story builder."""
    session_id = serializers.UUIDField()


class StoryBuilderCompleteResponseSerializer(serializers.Serializer):
    """Response serializer for story builder completion."""
    total_score = serializers.IntegerField()
    max_score = serializers.IntegerField()
    rounds = serializers.ListField()
    full_story = serializers.CharField()
    xp_earned = serializers.IntegerField()


# =============================================================================
# Listening Challenge serializers
# =============================================================================


class ListeningStartResponseSerializer(serializers.Serializer):
    """Response serializer for listening challenge start."""
    session_id = serializers.UUIDField()
    total_rounds = serializers.IntegerField()
    current_round = serializers.IntegerField()
    first_word = serializers.DictField()


class ListeningAnswerSerializer(serializers.Serializer):
    """Request serializer for submitting a listening answer."""
    session_id = serializers.UUIDField()
    round_number = serializers.IntegerField(min_value=1)
    answer = serializers.CharField(max_length=100)


class ListeningAnswerResultSerializer(serializers.Serializer):
    """Response serializer for listening answer result."""
    is_correct = serializers.BooleanField()
    score = serializers.IntegerField()
    attempts_used = serializers.IntegerField()
    attempts_remaining = serializers.IntegerField()
    hint = serializers.CharField(allow_blank=True)
    correct_answer = serializers.CharField(allow_blank=True)
    next_round = serializers.DictField(allow_null=True)
    combo = serializers.IntegerField()
    multiplier = serializers.FloatField()
    xp_earned = serializers.IntegerField()


class ListeningCompleteSerializer(serializers.Serializer):
    """Request serializer for completing listening challenge."""
    session_id = serializers.UUIDField()


# =============================================================================
# Synonym & Antonym serializers
# =============================================================================


class SynonymAntonymStartResponseSerializer(serializers.Serializer):
    """Response serializer for synonym/antonym game start."""
    session_id = serializers.UUIDField()
    total_rounds = serializers.IntegerField()
    current_round = serializers.IntegerField()
    rounds = serializers.ListField()


class SynonymAntonymAnswerSerializer(serializers.Serializer):
    """Request serializer for submitting a synonym/antonym answer."""
    session_id = serializers.UUIDField()
    round_number = serializers.IntegerField(min_value=1)
    answer = serializers.CharField(max_length=100)


class SynonymAntonymAnswerResultSerializer(serializers.Serializer):
    """Response serializer for synonym/antonym answer result."""
    is_correct = serializers.BooleanField()
    correct_answer = serializers.CharField()
    score = serializers.IntegerField()
    next_round = serializers.DictField(allow_null=True)
    combo = serializers.IntegerField()
    multiplier = serializers.FloatField()
    xp_earned = serializers.IntegerField()


class SynonymAntonymCompleteSerializer(serializers.Serializer):
    """Request serializer for completing synonym/antonym game."""
    session_id = serializers.UUIDField()


# =============================================================================
# Irregular Verbs serializers
# =============================================================================


class IrregularVerbsStartSerializer(serializers.Serializer):
    """Request serializer for starting irregular verbs game."""
    word_count = serializers.IntegerField(required=False, default=10, min_value=5, max_value=30)
    tier = serializers.CharField(required=False, default="", allow_blank=True)


class IrregularVerbsStartResponseSerializer(serializers.Serializer):
    """Response serializer for irregular verbs game start."""
    session_id = serializers.UUIDField()
    total_rounds = serializers.IntegerField()
    current_round = serializers.IntegerField()
    tier = serializers.CharField()
    rounds = serializers.ListField()


class IrregularVerbAnswerSerializer(serializers.Serializer):
    """Request serializer for submitting an irregular verb answer."""
    session_id = serializers.UUIDField()
    round_number = serializers.IntegerField(min_value=1)
    past_simple = serializers.CharField(max_length=50)
    past_participle = serializers.CharField(max_length=50)


class IrregularVerbAnswerResultSerializer(serializers.Serializer):
    """Response serializer for irregular verb answer result."""
    past_simple_correct = serializers.BooleanField()
    past_participle_correct = serializers.BooleanField()
    correct_past_simple = serializers.CharField(allow_blank=True)
    correct_past_participle = serializers.CharField(allow_blank=True)
    score = serializers.IntegerField()
    attempts_used = serializers.IntegerField()
    attempts_remaining = serializers.IntegerField()
    hints = serializers.DictField()
    next_round = serializers.DictField(allow_null=True)
    combo = serializers.IntegerField()
    multiplier = serializers.FloatField()
    xp_earned = serializers.IntegerField()


class IrregularVerbsCompleteSerializer(serializers.Serializer):
    """Request serializer for completing irregular verbs game."""
    session_id = serializers.UUIDField()
