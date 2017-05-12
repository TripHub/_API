"""
Abstract serializers intended for inheritance across DRF.
"""

from rest_framework import serializers


class PublicIdBaseSerializer(serializers.ModelSerializer):
    """Swaps the ID in favour of the UID."""
    id = serializers.CharField(source='uid')
