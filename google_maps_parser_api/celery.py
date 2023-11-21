import os
from celery import Celery
from gmaps_collector.collector import Collector
from celery.signals import task_success, task_failure, task_retry
from django.conf import settings
from django import setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "google_maps_parser_api.settings")

app = Celery("celery_app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task
def send_task_to_collector(task_id: int, gmaps_token: str, type_: str, location: tuple[float, float], radius: int):
    from gmaps.models import TaskResult
    task_result = TaskResult.objects.create(task_id=task_id)
    task_result.save()
    collector = Collector(task_result, gmaps_token, type_, location, radius)
    collector.collect()
