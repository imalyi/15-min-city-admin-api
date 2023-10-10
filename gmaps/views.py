from rest_framework.generics import ListCreateAPIView

from gmaps.serializers import CredentialSerializer, PlaceTypeSerializer, StatusSerializer, CoordinateSerializer, SubTaskSerializer, TaskSerializer
from gmaps.models import Credential, PlaceType, Status, Coordinate, SubTask, Task



class CredentialView(ListCreateAPIView):
    serializer_class = CredentialSerializer
    queryset = Credential.objects.all()


class PlaceTypeView(ListCreateAPIView):
    serializer_class = PlaceTypeSerializer
    queryset = PlaceType.objects.all()


class StatusView(ListCreateAPIView):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()


class CoordinatesView(ListCreateAPIView):
    serializer_class = CoordinateSerializer
    queryset = Coordinate.objects.all()


class SubTaskView(ListCreateAPIView):
    serializer_class = SubTaskSerializer
    queryset = SubTask.objects.all()


class TaskView(ListCreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

