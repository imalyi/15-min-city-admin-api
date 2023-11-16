import os

from celery import Celery
from task_sender import get_task_sender

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "google_maps_parser_api.settings")
app = Celery("celery_app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task
def send_task_to_collector(template_id):
    task_sender = get_task_sender()
    task_sender.send(template_id)