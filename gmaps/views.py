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
            task.status = RUNNING
            task.save()
            return Response({'detail': f"Task {task} added to queue"})
        return Response({'detail': f"Task {task} has status {task.status}"})


class SubTaskActionView(viewsets.ModelViewSet):
    serializer_class = SubTaskSerializer
    queryset = SubTask.objects.all()

    @action(detail=True, methods=['get'])
    def error(self, request, pk=None):
        subtask = self.get_object()
        subtask.change_status_to_error()
        return Response({'detail': 'ok'})

    @action(detail=True, methods=['get'])
    def done(self, request, pk=None):
        subtask = self.get_object()
        subtask.change_status_to_done()
        return Response({'detail': 'ok'})

    @action(detail=True, methods=['get'])
    def start(self, request, pk=None):
        subtask = self.get_object()
        subtask.start_if_waiting()
        return Response({'detail': 'ok'})

    @action(detail=True, methods=['post'])
    def track(self, request, pk=None):
        subtask = self.get_object()
        subtask.update_progress(request.data.get('progress', 0))
        return Response({'detail': 'ok'})


class TaskView(ListCreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

