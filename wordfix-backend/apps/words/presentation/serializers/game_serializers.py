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
