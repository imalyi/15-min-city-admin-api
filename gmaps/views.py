from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from task_sender import TaskSender
from gmaps.serializers import CredentialSerializer, PlaceTypeSerializer, CoordinateSerializer, SubTaskSerializer, TaskSerializer
from gmaps.models import Credential, PlaceType, Coordinate, SubTask, Task
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


def handle_task_action(view_func):
    @functools.wraps(view_func)
    def wrapper(self, request, pk=None):
        task = self.get_object()
        try:
            return view_func(self, task, request, pk)
        except Exception as err:
            print(err)
    return wrapper


class TaskActionView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    @action(detail=True, methods=['get'])
    @handle_task_action
    def start(self, task, request, pk=None):
        """Send all subtask to execution and set status"""
        task_sender = TaskSender()
        task_json = JSONRenderer().render(TaskSerializer(task).data)
        task_sender.send(task_json)
        return Response({'detail': f"Task {task} added to queue"})

    @action(detail=True, methods=['get'])
    @handle_task_action
    def cancel(self, task, request, pk=None):
        """Cancel all subtask with status WAITING"""
        task.cancel()
        return Response({'detail': f"Task {task} canceled"})

    @action(detail=True, methods=['get'])
    @handle_task_action
    def stop(self, task, request, pk=None):
        """Stop all subtask with status RUNNING"""
        task.stop()
        return Response({'detail': f"Task {task} stopped"})


def handle_subtask_action(view_func):
    @functools.wraps(view_func)
    def wrapper(self, request, pk=None):
        subtask = self.get_object()
        try:
            return view_func(self, subtask, request, pk)
        except (SubTask.InvalidStatusChange, SubTask.InvalidProgressValue) as e:
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
        subtask.change_status_to_running()
        return Response({'detail': 'ok'})

    @action(detail=True, methods=['get'])
    @handle_subtask_action
    def cancel(self, subtask, request, pk=None):
        subtask.change_status_to_canceled()
        return Response({'detail': 'ok'})

    @action(detail=True, methods=['get'])
    @handle_subtask_action
    def stop(self, subtask, request, pk=None):
        subtask.change_status_to_stopped()
        return Response({'detail': 'ok'})

    @action(detail=True, methods=['post'])
    @handle_subtask_action
    def track(self, subtask, request, pk=None):
        subtask.update_progress(request.data.get('progress', 0))
        return Response({'detail': 'ok'})


class TaskView(ListCreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
