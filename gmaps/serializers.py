from rest_framework.serializers import ModelSerializer, SerializerMethodField, PrimaryKeyRelatedField, IntegerField, StringRelatedField, CharField, DateTimeField, DateField
from gmaps.models import Credential, PlaceType, Coordinate, TaskResult, TaskTemplate, Category
from django.db.utils import IntegrityError
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


class TaskTemplateSerializer(ModelSerializer):
    place = PlaceTypeSerializer()
    credentials = CredentialSerializer()
    coordinates = CoordinateSerializer()
    schedule = ScheduleSerializer()

    class Meta:
        model = TaskTemplate
        fields = ("place", "credentials", "coordinates", "schedule", "id")


class TaskTemplateCreateSerializer(ModelSerializer):
    place = PrimaryKeyRelatedField(queryset=PlaceType.objects.all())
    credentials = PrimaryKeyRelatedField(queryset=Credential.objects.all())
    coordinates = PrimaryKeyRelatedField(queryset=Coordinate.objects.all())

    class Meta:
        model = TaskTemplate
        fields = "__all__"


class TaskSerializer(ModelSerializer):
    template = TaskTemplateSerializer()
    actions = SerializerMethodField()
    items_collected = IntegerField(read_only=True)
    status = CharField(read_only=True)
    start = DateTimeField(read_only=True)
    finish = DateTimeField(read_only=True)
    planned_exec_date = DateField(read_only=True)
    
    def get_actions(self, obj):
        return obj.actions

    class Meta:
        model = TaskResult
        fields = "__all__"


class TaskCreateSerializer(ModelSerializer):
    template = PrimaryKeyRelatedField(queryset=TaskTemplate.objects.all())

    class Meta:
        model = TaskResult
        fields = "__all__"
