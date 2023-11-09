from rest_framework.serializers import ModelSerializer
from gmaps.models import Credential, PlaceType, Coordinate, Task, TaskTemplate


class CredentialSerializer(ModelSerializer):
    class Meta:
        model = Credential
        fields = '__all__'


class PlaceTypeSerializer(ModelSerializer):
    class Meta:
        model = PlaceType
        fields = "__all__"


class CoordinateSerializer(ModelSerializer):
    class Meta:
        model = Coordinate
        fields = '__all__'


class TaskTemplateSerializer(ModelSerializer):
    place = PlaceTypeSerializer()
    class Meta:
        model = TaskTemplate
        fields = "__all__"


class TaskSerializer(ModelSerializer):
    template = TaskTemplateSerializer()
    class Meta:
        model = Task
        fields = "__all__"

