"""
Challenge serializers.
"""

from rest_framework import serializers


class DailyChallengeSerializer(serializers.Serializer):
    """Serializer for daily challenges."""

    date = serializers.CharField()
    challenges = serializers.ListField()
    all_completed = serializers.BooleanField()
    bonus_claimed = serializers.BooleanField()


class ClaimBonusSerializer(serializers.Serializer):
    """Serializer for claim bonus response."""

    claimed = serializers.BooleanField()
    message = serializers.CharField()
