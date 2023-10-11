import datetime
from django.core import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView, CreateAPIView, UpdateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from task_sender import TaskSender
from gmaps.serializers import CredentialSerializer, PlaceTypeSerializer, CoordinateSerializer, SubTaskSerializer, TaskSerializer
from gmaps.models import Credential, PlaceType, Coordinate, SubTask, Task
from gmaps.models import ERROR, WAITING, RUNNING, STOPPED, DONE, CANCELED
from rest_framework import status

import functools


class CredentialView(ListCreateAPIView):
    serializer_class = CredentialSerializer
    queryset = Credential.objects.all()


class PlaceTypeView(ListCreateAPIView):
    serializer_class = PlaceTypeSerializer
    queryset = PlaceType.objects.all()


class CoordinatesView(ListCreateAPIView):
    serializer_class = CoordinateSerializer
    queryset = Coordinate.objects.all()


class SubTaskView(ListCreateAPIView):
    serializer_class = SubTaskSerializer
    queryset = SubTask.objects.all()


class TaskActionView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    @action(detail=True, methods=['get'])
    def start(self, request, pk=None):
        task = self.get_object()
        if task.status == WAITING:
            task_sender = TaskSender()
            task_json = JSONRenderer().render(TaskSerializer(task).data)
            task_sender.send(task_json)
            return Response({'detail': f"Task {task} added to queue"})
        return Response({'detail': f"Task {task} has status {task.status}"})


def handle_subtask_action(view_func):
    @functools.wraps(view_func)
    def wrapper(self, request, pk=None):
        subtask = self.get_object()
        try:
            return view_func(self, subtask, request, pk)
        except (SubTask.InvalidStatusChange,SubTask.InvalidProgressValue) as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return wrapper


class SubTaskActionView(viewsets.ModelViewSet):
    serializer_class = SubTaskSerializer
    queryset = SubTask.objects.all()

    @action(detail=True, methods=['get'])
    @handle_subtask_action
    def error(self, subtask, request, pk=None):
        subtask.change_status_to_error()
        return Response({'detail': 'ok'})

    @action(detail=True, methods=['get'])
    @handle_subtask_action
    def done(self, subtask, request, pk=None):
        subtask.change_status_to_done()
        return Response({'detail': 'ok'})

    @action(detail=True, methods=['get'])
    @handle_subtask_action
    def start(self, subtask, request, pk=None):
        subtask.start_if_waiting()
        return Response({'detail': 'ok'})

    @action(detail=True, methods=['get'])
    @handle_subtask_action
    def cancel(self, subtask, request, pk=None):
        subtask.cancel_if_waiting()
        return Response({'detail': 'ok'})

    @action(detail=True, methods=['post'])
    @handle_subtask_action
    def track(self, subtask, request, pk=None):
        subtask.update_progress(request.data.get('progress', 0))
        return Response({'detail': 'ok'})


class TaskView(ListCreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

