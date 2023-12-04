from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.response import Response
from rest_framework.decorators import action
from openstreetmaps.models import OSMTask, OSMTaskResult
from openstreetmaps.serializers import TaskSerializer, TaskResultSerializer
from google_maps_parser_api.celery import send_osm_task_to_collector
from django_celery_beat.models import PeriodicTask
import json


class TaskView(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = OSMTask.objects.all()

    @action(methods=['get'], detail=True)
    def start(self, request, pk=None):
        try:
            task = OSMTask.objects.get(id=pk)
            periodic_task = PeriodicTask.objects.get(name=task.region)
            send_osm_task_to_collector.delay(*json.loads(periodic_task.args))
        except PeriodicTask.DoesNotExist:
            return Response({'detail': f"Task with id {pk} is broken. Please, delete and recreate this task"}, status=HTTP_404_NOT_FOUND)
        except Exception as err:
            #TODO log error
            return Response({'detail': "Unkonw error. Contact with administrator"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'detail': "ok"})


class TaskResultView(ModelViewSet):
    serializer_class = TaskResultSerializer
    queryset = OSMTaskResult.objects.all()
