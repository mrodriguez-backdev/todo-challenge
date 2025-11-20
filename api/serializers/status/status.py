from rest_framework import serializers
from api.models import Status


class StatusSerializer(serializers.ModelSerializer):
    """
    Serializer for Status model.
    Handles serialization/deserialization of Status objects.
    """
    class Meta:
        model = Status
        fields = ['id', 'name', 'hexa_color', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
