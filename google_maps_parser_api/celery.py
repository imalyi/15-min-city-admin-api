import os
from celery import Celery
from collectors.gmaps.collector import Collector
from collectors.openstreetmaps.street import Street
from collectors.openstreetmaps.amenity import Amenity

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "google_maps_parser_api.settings")

app = Celery("celery_app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task
def send_gmaps_task_to_collector(task_id: int, gmaps_token: str, type_: str, location: tuple[float, float], radius: int):
    from gmaps.models import TaskResult
    task_result = TaskResult.objects.create(task_id=task_id)
    task_result.save()
    collector = Collector(task_result, gmaps_token, type_, location, radius)
    collector.collect()


@app.task
def send_osm_task_to_collector(task_id: int):
    from openstreetmaps.models import OSMTaskResult
    from openstreetmaps.models import OSMTask
    region = OSMTask.objects.get(id=task_id).region
    task_result = OSMTaskResult.objects.create(task_id=task_id)
    street = Street(region, task_result)
    street.update()
    amenity = Amenity(region)
    amenity.update()
    task_result.mark_as_done()
