from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.response import Response
from rest_framework.decorators import action
from openstreetmaps.models import OSMTask
from openstreetmaps.serializers import TaskSerializer

from django_celery_beat.models import PeriodicTask


class TaskView(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = OSMTask.objects.all()

    @action(methods=['get'], detail=True)
    def start(self, request, pk=None):
        try:
            task = OSMTask.objects.get(id=pk)
            periodic_task = PeriodicTask.objects.get(name=task.place.value)
            
        except PeriodicTask.DoesNotExist:
            return Response({'detail': f"Task with id {pk} is broken. Please, delete and recreate this task"}, status=HTTP_404_NOT_FOUND)
        except Exception as err:
            return Response({'detail': "Unkonw error. Contact with administrator"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'detail': "ok"})
