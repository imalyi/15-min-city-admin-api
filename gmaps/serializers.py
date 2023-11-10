from rest_framework.serializers import ModelSerializer, SerializerMethodField, PrimaryKeyRelatedField
from gmaps.models import Credential, PlaceType, Coordinate, Task, TaskTemplate, Schedule


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


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('name', )


class TaskTemplateSerializer(ModelSerializer):
    place = PrimaryKeyRelatedField(queryset=PlaceType.objects.all())
    credentials = PrimaryKeyRelatedField(queryset=Credential.objects.all())
    coordinates = PrimaryKeyRelatedField(queryset=Coordinate.objects.all())
    schedule = PrimaryKeyRelatedField(queryset=Schedule.objects.all())

    class Meta:
        model = TaskTemplate
        fields = ("place", "credentials", "coordinates", "schedule", "id")


class TaskSerializer(ModelSerializer):
    template = TaskTemplateSerializer()
    actions = SerializerMethodField()

    def get_actions(self, obj):
        return obj.actions

    class Meta:
        model = Task
        fields = "__all__"