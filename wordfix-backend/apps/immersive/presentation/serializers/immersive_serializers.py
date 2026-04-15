"""
Immersive game serializers.
"""

from rest_framework import serializers


class StartSessionSerializer(serializers.Serializer):
    scenario_id = serializers.UUIDField()
    npc_id = serializers.UUIDField(required=False)
    input_mode = serializers.ChoiceField(choices=["text", "voice", "mixed"], default="text")


class SubmitResponseSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=2000)
    response_time_ms = serializers.IntegerField(required=False, allow_null=True)


class CompleteSessionSerializer(serializers.Serializer):
    """Empty — session_id from URL."""
    pass


class ScenarioFilterSerializer(serializers.Serializer):
    difficulty = serializers.ChoiceField(
        choices=["A1", "A2", "B1", "B2", "C1", "C2"],
        required=False,
    )
    location = serializers.ChoiceField(
        choices=["office", "restaurant", "airport", "hospital", "school", "hotel", "shop", "bank", "park", "gym"],
        required=False,
    )
