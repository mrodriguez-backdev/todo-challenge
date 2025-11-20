from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from api.views.health import health_check
from api.views.status import StatusViewSet
from api.views.task import TaskViewSet, mark_tasks_as_complete

# Initialize router for ViewSets
router = DefaultRouter()

# Register ViewSets here
router.register(r'status', StatusViewSet, basename='status')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    # Health check endpoint
    path('health/', health_check, name='health-check'),

    # JWT Authentication endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Task custom endpoints
    path('tasks/mark-as-complete/', mark_tasks_as_complete, name='mark-tasks-as-complete'),

    # API Documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Add router URLs to urlpatterns
urlpatterns += router.urls
