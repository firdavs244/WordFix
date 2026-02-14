"""
Serializers for adaptive-intelligence endpoints.
"""

from rest_framework import serializers


class LearningProfileSerializer(serializers.Serializer):
    """Read-only representation of a learning profile."""

    preferred_style = serializers.CharField()
    style_confidence = serializers.FloatField()
    best_hour_start = serializers.IntegerField()
    best_hour_end = serializers.IntegerField()
    best_days = serializers.ListField(child=serializers.IntegerField())
    avg_session_duration = serializers.IntegerField()
    optimal_words_per_session = serializers.IntegerField()
    avg_retention_rate = serializers.FloatField()
    strongest_skills = serializers.ListField(child=serializers.CharField())
    weakest_skills = serializers.ListField(child=serializers.CharField())
    current_difficulty_level = serializers.FloatField()
    difficulty_adjustment_rate = serializers.FloatField()
    last_analyzed_at = serializers.CharField(allow_null=True)


class MistakePatternSerializer(serializers.Serializer):
    """Read-only representation of a mistake pattern."""

    id = serializers.CharField()
    pattern_type = serializers.CharField()
    description = serializers.CharField()
    examples = serializers.ListField()
    occurrence_count = serializers.IntegerField()
    is_resolved = serializers.BooleanField()
    drills_completed = serializers.IntegerField()
    success_rate_after_drills = serializers.FloatField()
    related_words = serializers.ListField(child=serializers.CharField())


class WordRecommendationSerializer(serializers.Serializer):
    """Read-only representation of a word recommendation."""

    id = serializers.CharField()
    recommended_word = serializers.CharField()
    translation = serializers.CharField()
    reason = serializers.CharField()
    reason_type = serializers.CharField()
    priority_score = serializers.FloatField()
    is_accepted = serializers.BooleanField()
    ai_confidence = serializers.FloatField()


class DomainCoverageSerializer(serializers.Serializer):
    """Read-only representation of domain coverage."""

    total = serializers.IntegerField()
    coverage = serializers.FloatField()
    mastered = serializers.IntegerField()
    learning = serializers.IntegerField()


class DifficultyResponseSerializer(serializers.Serializer):
    """Response for adaptive difficulty."""

    difficulty_level = serializers.FloatField()
    adjusted = serializers.BooleanField()
    direction = serializers.CharField()


class AcceptRecommendationSerializer(serializers.Serializer):
    """Input for accepting a recommendation."""

    recommendation_id = serializers.UUIDField()
