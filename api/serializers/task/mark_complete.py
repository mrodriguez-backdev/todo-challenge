from rest_framework import serializers


class MarkTasksAsCompleteSerializer(serializers.Serializer):
    """
    Serializer for marking multiple tasks as complete.
    Receives a list of task IDs to update.
    """
    task_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        help_text="List of task IDs to mark as complete"
    )
