from rest_framework import serializers
from .models import OSMTask, OSMTaskResult, OSMError


class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = OSMError
        fields = ['id', 'data', 'date', 'type']


class TaskResultSerializer(serializers.ModelSerializer):
    errors = ErrorSerializer(many=True, read_only=True)

    class Meta:
        model = OSMTaskResult
        fields = ['id', 'task', 'start_date', 'finish_date', 'items_collected', 'errors']

    def get_errors(self, obj):
        return obj.errors


class TaskSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    task_results = TaskResultSerializer(many=True, read_only=True)

    class Meta:
        model = OSMTask
        fields = ['id', 'region', 'status', 'task_results', "schedule"]

    def get_status(self, obj):
        return obj.status
