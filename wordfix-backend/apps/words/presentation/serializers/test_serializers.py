"""
Test serializers.
"""

from rest_framework import serializers


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
