from rest_framework.serializers import ModelSerializer, SerializerMethodField
from gmaps.models import Credential, PlaceType, Status, Coordinate, SubTask, Task


class CredentialSerializer(ModelSerializer):
    class Meta:
        model = Credential
        fields = ('name', 'request_limit')


class PlaceTypeSerializer(ModelSerializer):
    class Meta:
        model = PlaceType
        fields = "__all__"


class StatusSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class CoordinateSerializer(ModelSerializer):
    class Meta:
        model = Coordinate
        fields = "__all__"


class SubTaskSerializer(ModelSerializer):
    class Meta:
        model = SubTask
        fields = "__all__"


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
