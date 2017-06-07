"""
Abstract serializers intended for inheritance across DRF.
"""

from rest_framework import serializers


class PublicIdBaseSerializer(serializers.ModelSerializer):
    """Swaps the value of the ID with the UID for public display."""
    id = serializers.CharField(read_only=True, source='uid')
