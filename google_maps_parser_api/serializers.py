from rest_framework.serializers import Serializer, ModelSerializer
from google_maps_parser_api.models import Credential, PlaceType, Status, Coordinate, SubTask, Task



class CredentialSerializer(ModelSerializer):
    class Meta:
        model = Credential
        fields = "__all__"


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
    class Meta:
        model = Task
        fields = "__all__"

