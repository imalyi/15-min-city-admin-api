import json
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets
from task_sender import get_task_sender
from gmaps.serializers import CredentialSerializer, PlaceTypeSerializer, CoordinateSerializer, TaskSerializer, TaskTemplateSerializer, TaskTemplateCreateSerializer
from gmaps.models import Credential, PlaceType, Coordinate, TaskTemplate, Task
from rest_framework import status
import functools


class CredentialView(viewsets.ModelViewSet):
    serializer_class = CredentialSerializer
    queryset = Credential.objects.all()


class PlaceTypeView(viewsets.ModelViewSet):
    serializer_class = PlaceTypeSerializer
    queryset = PlaceType.objects.all()


class CoordinatesView(ListCreateAPIView):
    serializer_class = CoordinateSerializer
    queryset = Coordinate.objects.all()


def handle_task_action(view_func):
    @functools.wraps(view_func)
    def wrapper(self, request, pk=None):
        task = self.get_object()
        try:
            view_func(self, task, request, pk)
            return Response({'detail': 'ok'})
        except (Task.InvalidStatusChange, Task.InvalidProgressValue) as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return wrapper


class TaskActionView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    @action(detail=True, methods=['get'])
    @handle_task_action
    def stop(self, task, request, pk=None):
        task.stop()
        return Response({'detail': f"Task {task} stopped"})

    @action(detail=True, methods=['get'])
    @handle_task_action
    def error(self, task, request, pk=None):
        task.change_status_to_error()

    @action(detail=True, methods=['get'])
    @handle_task_action
    def done(self, task, request, pk=None):
        task.change_status_to_done()

    @action(detail=True, methods=['get'])
    @handle_task_action
    def running(self, task, request, pk=None):
        task.change_status_to_running()

    @action(detail=True, methods=['get'])
    @handle_task_action
    def cancel(self, task, request, pk=None):
        task.change_status_to_canceled()

    @action(detail=True, methods=['get'])
    @handle_task_action
    def stop(self, task, request, pk=None):
        task.change_status_to_stopped()

    @action(detail=True, methods=['post'])
    @handle_task_action
    def track(self, task, request, pk=None):
        task.update_progress(request.data.get('progress', 0))


class TaskTemplateView(viewsets.ModelViewSet):
    serializer_class = TaskTemplateSerializer
    queryset = TaskTemplate.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskTemplateCreateSerializer
        return TaskTemplateSerializer
