import json

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework import viewsets
from gmaps.serializers import CredentialSerializer, CategoryPlaceSerializer, CoordinateSerializer, TaskResultSerializer, TaskSerializer, TaskCreateSerializer
from gmaps.serializers import TaskCreateSerializer, ScheduleSerializer
from gmaps.models import Credential, Coordinate, Task, TaskResult, Category
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from google_maps_parser_api.celery import send_task_to_collector


class CredentialView(viewsets.ModelViewSet):
    serializer_class = CredentialSerializer
    queryset = Credential.objects.all()


class PlaceTypeView(viewsets.ModelViewSet):
    serializer_class = CategoryPlaceSerializer
    queryset = Category.objects.all()


class CoordinatesView(ListCreateAPIView):
    serializer_class = CoordinateSerializer
    queryset = Coordinate.objects.all()


class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        return TaskSerializer

    @action(methods=['get'], detail=True)
    def start(self, request, pk=None):
        try:
            task = Task.objects.get(id=pk)
            periodic_task = PeriodicTask.objects.get(name=task.place.value)
            send_task_to_collector.delay(*json.loads(periodic_task.args))
        except Task.DoesNotExist:
            return Response({'detail': f"Task with id {pk} does not exists"})
        return Response({'detail': "ok"})


class ScheduleView(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    queryset = IntervalSchedule.objects.all()


class TaskResultView(ListAPIView):
    serializer_class = TaskResultSerializer
    lookup_field = "task_id"

    def get_queryset(self):
        task_id = self.kwargs.get(self.lookup_field)
        return TaskResult.objects.filter(task_id=task_id)
