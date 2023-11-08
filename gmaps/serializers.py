from rest_framework.serializers import ModelSerializer, SerializerMethodField, Serializer, ListField, CharField, IntegerField, ValidationError
from gmaps.models import Credential, PlaceType, Coordinate, SubTask, Task


class CredentialSerializer(ModelSerializer):
    class Meta:
        model = Credential
        fields = '__all__'


class PlaceTypeSerializer(ModelSerializer):
    class Meta:
        model = PlaceType
        fields = ('value', )
        read_only_fiedls = ('value', )


class CoordinateSerializer(ModelSerializer):
    class Meta:
        model = Coordinate
        fields = '__all__'


class SubTaskSerializer(ModelSerializer):
    place = PlaceTypeSerializer()
    actions = SerializerMethodField(read_only=True)

    def get_actions(self, obj):
        return obj.actions

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
    status = SerializerMethodField()
    last_change_date = SerializerMethodField()
    coordinates = CoordinateSerializer()

    def create(self, validated_data):
        for sub_task in validated_data.pop('sub_task'):
            place_data = sub_task.get('place')
            place_value = place_data.get('value')
            try:
                # Try to get the PlaceType object by 'value'
                place = PlaceType.objects.get(value=place_value)
            except PlaceType.DoesNotExist:
                # If it doesn't exist, create it
                place = PlaceType.objects.create(value=place_value)
            print(place)

    class Meta:
        model = Task
        fields = "__all__"

    def get_last_change_date(self, obj):
        return obj.last_change_date

    def get_status(self, obj):
        return obj.status

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


class CreateTaskSerializer(Serializer):
    places = ListField()  # list of ids of places
    name = CharField()
    credentials = IntegerField()
    coordinates = IntegerField()

    def create(self, validated_data):
        subtasks = []
        for place in validated_data.get('places'):
            try:
                place_obj = PlaceType.objects.get(id=place)
                subtasks.append(SubTask.objects.create(place=place_obj))
            except PlaceType.DoesNotExist:
                raise ValidationError(f"{place} does not exists")
        try:
            credentials = Credential.objects.get(id=validated_data.get('credentials'))
        except Credential.DoesNotExist:
            raise ValidationError(f"Credential with id {validated_data.get('credentials')} does not exists")

        try:
            coordinates = Coordinate.objects.get(id=validated_data.get('coordinates'))
        except Coordinate.DoesNotExist:
            raise ValidationError(f"Coordinates with id {validated_data.get('coordinates')} does not exists")

        task = Task.objects.create(name=validated_data.get('name'), credentials=credentials,
                            coordinates=coordinates)
        task.sub_task.set(subtasks)
        return task