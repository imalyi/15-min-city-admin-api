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

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if instance.status == DONE:
            instance.finish = datetime.datetime.now()
        if instance.status == RUNNING:
            instance.start = datetime.datetime.now()

        instance.save()
        return instance

class TaskSerializer(ModelSerializer):
    sub_task = SubTaskSerializer(many=True)
    credentials = CredentialSerializer()
    subtask_count = SerializerMethodField()
    items_collected = SerializerMethodField()
    is_start = SerializerMethodField()
    is_finish = SerializerMethodField()

    class Meta:
        model = Task
        fields = "__all__"

    def get_subtask_count(self, obj):
        return obj.subtask_count

    def get_items_collected(self, obj):
        return obj.items_collected

    def get_is_start(self, obj):
        return obj.is_start

    def get_is_finish(self, obj):
        return obj.is_finish

