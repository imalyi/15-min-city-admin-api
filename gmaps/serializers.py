import datetime

from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
from gmaps.models import Credential, PlaceType, Coordinate, SubTask, Task
from gmaps.models import DONE, RUNNING, ERROR, STOPPED, WAITING


class CredentialSerializer(ModelSerializer):
    class Meta:
        model = Credential
        fields = ('name')


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
    credentials = SerializerMethodField()

    def get_credentials(self, obj):
        return obj.credentials

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

    def get_waiting_subtask_count(self, obj):
        return obj.waiting_subtask_count

    def get_running_subtask_count(self, obj):
        return obj.running_subtask_count

    def get_done_subtask_count(self, obj):
        return obj.done_subtask_count

    def get_canceled_subtask_count(self, obj):
        return obj.canceled_subtask_count

    def get_stopped_subtask_count(self, obj):
        return obj.stopped_subtask_count

    def get_error_subtask_count(self, obj):
        return obj.error_subtask_count
