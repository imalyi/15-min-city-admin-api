from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework import viewsets
from gmaps.serializers import CredentialSerializer, PlaceTypeSerializer, CoordinateSerializer, TaskResultSerializer, TaskSerializer, TaskCreateSerializer
from gmaps.serializers import TaskCreateSerializer, ScheduleSerializer
from gmaps.models import Credential, PlaceType, Coordinate, Task, TaskResult
from rest_framework import status
import functools
from django_celery_beat.models import IntervalSchedule


class CredentialView(viewsets.ModelViewSet):
    serializer_class = CredentialSerializer
    queryset = Credential.objects.all()


class PlaceTypeView(viewsets.ModelViewSet):
    serializer_class = PlaceTypeSerializer
    queryset = PlaceType.objects.all()


class CoordinatesView(ListCreateAPIView):
    serializer_class = CoordinateSerializer
    queryset = Coordinate.objects.all()


class TaskResult(ListAPIView):
    serializer_class = TaskResultSerializer
    queryset = TaskResult.objects.all()

    http_method_names = ['get']


class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        return TaskSerializer


class ScheduleView(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    queryset = IntervalSchedule.objects.all()