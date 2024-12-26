from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from apps.users.permissions import IsAdmin, IsManager, IsEmployee

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAdmin()]
        elif self.request.method == 'GET':
            return [IsAuthenticated()]
        return []
