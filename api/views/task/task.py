from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from api.models import Task, Status
from api.serializers.task import TaskSerializer, MarkTasksAsCompleteSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Task model.
    Provides CRUD operations: list, create, retrieve, update, partial_update, destroy.
    Includes filtering and search capabilities.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'status': ['exact'],
        'created_at': ['exact', 'gte', 'lte', 'range'],
    }
    search_fields = ['name', 'content']
    ordering_fields = ['created_at', 'updated_at', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Optionally filter tasks with select_related for performance.
        """
        return Task.objects.select_related('status').all()
