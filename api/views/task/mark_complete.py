from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
from api.models import Task, Status
from api.serializers.task import TaskSerializer, MarkTasksAsCompleteSerializer


@extend_schema(
    request=MarkTasksAsCompleteSerializer,
    responses={
        200: TaskSerializer(many=True),
        404: {'description': 'Completed status not found'},
        400: {'description': 'Invalid request data'}
    },
    examples=[
        OpenApiExample(
            'Mark tasks as complete',
            value={'task_ids': [1, 2, 3]},
            request_only=True,
            description='Example: Mark tasks with IDs 1, 2, and 3 as complete'
        ),
    ],
    description='Mark multiple tasks as complete. Automatically finds the "Completado" status and updates all specified tasks.',
    summary='Mark tasks as complete'
)

@api_view(['POST'])
def mark_tasks_as_complete(request):
    """
    Mark multiple tasks as complete.
    Automatically finds the 'Completado' status and updates all specified tasks.

    Request body: {"task_ids": [1, 2, 3]}

    Returns:
        200: Tasks successfully marked as complete
        404: Completado status not found
        400: Invalid request data
    """
    serializer = MarkTasksAsCompleteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    task_ids = serializer.validated_data['task_ids']

    # Find the "Completado" status (case-insensitive)
    try:
        completed_status = Status.objects.get(name__iexact='completado')
    except Status.DoesNotExist:
        return Response(
            {'error': 'Completado status not found. Please create a status with name "Completado".'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Get all requested tasks
    tasks = Task.objects.filter(id__in=task_ids).select_related('status')

    # Separate already completed from pending
    already_completed_tasks = []
    to_complete_tasks = []

    for task in tasks:
        task_data = {
            'id': task.id,
            'name': task.name,
            'status': task.status.name
        }
        if task.status.id == completed_status.id:
            already_completed_tasks.append(task_data)
        else:
            to_complete_tasks.append(task_data)

    # Update only non-completed tasks
    updated_count = 0
    to_complete_ids = [task['id'] for task in to_complete_tasks]
    if to_complete_ids:
        updated_count = Task.objects.filter(id__in=to_complete_ids).update(status=completed_status)
        # Update the status in our data structure after processing
        for task in to_complete_tasks:
            task['status'] = completed_status.name

    # Build response
    response_data = {
        'message': f'{updated_count} task(s) marked as complete',
        'updated_count': updated_count,
        'tasks': to_complete_tasks
    }

    # Add already completed tasks if any
    if already_completed_tasks:
        response_data['warning'] = f'{len(already_completed_tasks)} task(s) were already completed'
        response_data['already_completed_tasks'] = already_completed_tasks

    return Response(response_data, status=status.HTTP_200_OK)
