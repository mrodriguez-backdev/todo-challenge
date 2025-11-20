from rest_framework import serializers
from api.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.
    Handles serialization/deserialization of Task objects.
    """
    status_name = serializers.CharField(source='status.name', read_only=True)
    status_color = serializers.CharField(source='status.hexa_color', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'content',
            'status',
            'status_name',
            'status_color',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
