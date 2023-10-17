import datetime

from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
from gmaps.models import Credential, PlaceType, Coordinate, SubTask, Task
from gmaps.models import DONE, RUNNING, ERROR, STOPPED, WAITING


class CredentialSerializer(ModelSerializer):
    class Meta:
        model = Credential
        fields = ('name', 'request_limit')


class PlaceTypeSerializer(ModelSerializer):
    class Meta:
        model = PlaceType
        fields = ('value', )


class CoordinateSerializer(ModelSerializer):
    class Meta:
        model = Coordinate
        fields = ('name', 'lat', 'lon')


class SubTaskSerializer(ModelSerializer):
    coordinates = CoordinateSerializer()
    place = PlaceTypeSerializer()

    class Meta:
        model = SubTask
        fields = "__all__"


class TaskSerializer(ModelSerializer):
    sub_task = SubTaskSerializer(many=True)
    credentials = CredentialSerializer()
    subtask_count = SerializerMethodField()
    items_collected = SerializerMethodField()
    waiting_subtask_count = SerializerMethodField()
    running_subtask_count = SerializerMethodField()
    done_subtask_count = SerializerMethodField()
    canceled_subtask_count = SerializerMethodField()
    stopped_subtask_count = SerializerMethodField()
    error_subtask_count = SerializerMethodField()

    class Meta:
        model = Task
        fields = "__all__"

    def get_subtask_count(self, obj):
        return obj.subtask_count

    def get_items_collected(self, obj):
        return obj.items_collected
