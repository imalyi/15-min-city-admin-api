from rest_framework.serializers import ModelSerializer, SerializerMethodField, PrimaryKeyRelatedField, IntegerField, StringRelatedField, CharField, DateTimeField
from gmaps.models import Credential, PlaceType, Coordinate, TaskResult, Task, Category
from django_celery_beat.models import IntervalSchedule


class CredentialSerializer(ModelSerializer):
    class Meta:
        model = Credential
        fields = '__all__'


class PlaceTypeSerializer(ModelSerializer):
    category = StringRelatedField(source='category.value')

    class Meta:
        model = PlaceType
        fields = "__all__"


class CoordinateSerializer(ModelSerializer):
    class Meta:
        model = Coordinate
        fields = '__all__'


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = "__all__"


class TaskSerializer(ModelSerializer):
    place = PlaceTypeSerializer()
    credentials = CredentialSerializer()
    coordinates = CoordinateSerializer()
    schedule = ScheduleSerializer()
    last_status = SerializerMethodField()

    class Meta:
        model = Task
        fields = ("place", "credentials", "coordinates", "schedule", "id", "last_status")

    def get_last_status(self, obj):
        return obj.last_status


class TaskCreateSerializer(ModelSerializer):
    place = PrimaryKeyRelatedField(queryset=PlaceType.objects.all())
    credentials = PrimaryKeyRelatedField(queryset=Credential.objects.all())
    coordinates = PrimaryKeyRelatedField(queryset=Coordinate.objects.all())
    schedule = PrimaryKeyRelatedField(queryset=IntervalSchedule.objects.all())

    class Meta:
        model = Task
        fields = "__all__"


class TaskResultSerializer(ModelSerializer):
    task = TaskSerializer()
    items_collected = IntegerField(read_only=True)
    status = CharField(read_only=True)
    start = DateTimeField(read_only=True)
    finish = DateTimeField(read_only=True)

    class Meta:
        model = TaskResult
        fields = "__all__"
