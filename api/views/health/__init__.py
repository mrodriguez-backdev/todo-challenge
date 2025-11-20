from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import connection


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint that verifies the application and database status.

    Returns:
        200: Application is healthy and database is connected
        503: Service unavailable (database connection failed)
    """
    try:
        # Check database connection
        connection.ensure_connection()

        return Response({
            'status': 'healthy',
            'database': 'connected',
            'message': 'Application is running correctly'
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'database': 'disconnected',
            'message': str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
