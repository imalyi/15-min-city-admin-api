from rest_framework.serializers import ModelSerializer, SerializerMethodField, PrimaryKeyRelatedField, IntegerField, CharField, DateTimeField
from gmaps.models import Credential, PlaceType, Coordinate, TaskResult, Task, Category, CrontabSchedule


class CredentialSerializer(ModelSerializer):
    class Meta:
        model = Credential
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PlaceTypeSerializer(ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = PlaceType
        fields = "__all__"


class CategoryPlaceSerializer(ModelSerializer):
    places = PlaceTypeSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        category_representation = super().to_representation(instance)
        places = PlaceType.objects.filter(category_id=instance.id)
        places_serialized = PlaceTypeSerializer(places, many=True).data
        return {"category_name": category_representation['value'], "places": places_serialized}

    class Meta:
        model = PlaceType
        fields = "__all__"


class CoordinateSerializer(ModelSerializer):
    class Meta:
        model = Coordinate
        fields = '__all__'


class ScheduleSerializer(ModelSerializer):
    human_readable = CharField(read_only=True)

    class Meta:
        model = CrontabSchedule
        exclude = ('timezone', )


class TaskSerializer(ModelSerializer):
    place = PlaceTypeSerializer()
    credentials = CredentialSerializer()
    coordinates = CoordinateSerializer()
    schedule = ScheduleSerializer()
    last_status = SerializerMethodField()
    actions = SerializerMethodField()

    def get_actions(self, obj):
        return obj.actions

    class Meta:
        model = Task
        fields = "__all__"

    def get_last_status(self, obj):
        return obj.last_status


class TaskCreateSerializer(ModelSerializer):
    place = PrimaryKeyRelatedField(queryset=PlaceType.objects.all())
    credentials = PrimaryKeyRelatedField(queryset=Credential.objects.all())
    coordinates = PrimaryKeyRelatedField(queryset=Coordinate.objects.all())
    schedule = PrimaryKeyRelatedField(queryset=CrontabSchedule.objects.all())

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


class TaskResultSerializer(ModelSerializer):
    task = TaskSerializer()
    items_collected = IntegerField(read_only=True)
    status = CharField(read_only=True)
    start = DateTimeField(read_only=True)
    finish = DateTimeField(read_only=True)

    class Meta:
        model = TaskResult
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['task'] = instance.task.place.value
        return representation