from rest_framework import viewsets
from api.models import Status
from api.serializers.status import StatusSerializer


class StatusViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Status model.
    Provides CRUD operations: list, create, retrieve, update, partial_update, destroy.
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned statuses.
        """
        return Status.objects.all().order_by('name')
