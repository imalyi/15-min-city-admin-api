import datetime
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.db import models
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json


class OSMTask(models.Model):
    region = models.CharField(max_length=250)
    schedule = models.ForeignKey(CrontabSchedule, on_delete=models.CASCADE)

    @property
    def status(self):
        running_results = OSMTaskResult.objects.filter(finish_date=None, task=self)
        if running_results.exists():
            return "RUNNING"
        latest_result = OSMTaskResult.objects.filter(task=self).order_by('-finish_date').first()
        if not latest_result:
            return "NEVER RUN"
        elif latest_result.addresses_items_collected > 0 and latest_result.amenity_items_collected > 0 and latest_result.errors.count() == 0 and latest_result.finish_date is not None:
            return "DONE"
        elif latest_result.finish_date and latest_result.errors.count() > 0:
            return "DONE_WITH_ERRORS"


class OSMTaskResult(models.Model):
    task = models.ForeignKey(OSMTask, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now=True)
    finish_date = models.DateTimeField(null=True, blank=True, default=None, unique=True)
    addresses_items_collected = models.IntegerField(default=0)
    amenity_items_collected = models.IntegerField(default=0)

    @property
    def errors(self):
        return OSMError.objects.filter(task_result=self)

    def update_address_progress(self, progress: int):
        self.addresses_items_collected += progress
        self.save()

    def update_amenity_progress(self, progress: int):
        self.amenity_items_collected += progress
        self.save()

    def add_error(self, data: str, type: str) -> None:
        OSMError.objects.create(task_result=self, data=data, type=type)

    def mark_as_done(self):
        self.finish_date = datetime.datetime.now()
        self.save()


class OSMError(models.Model):
    task_result = models.ForeignKey(OSMTaskResult, on_delete=models.CASCADE)
    data = models.CharField(max_length=800)
    date = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=260)


@receiver(post_save, sender=OSMTask)
def add_periodic_task(sender, instance, **kwargs):
    try:
        periodic_task = PeriodicTask.objects.get(name=instance.region)
        periodic_task.args = json.dumps([instance.id])
        periodic_task.save()
    except PeriodicTask.DoesNotExist:
        PeriodicTask.objects.create(
            name=instance.region,
            task="google_maps_parser_api.celery.send_osm_task_to_collector",
            crontab_id=instance.schedule.id,
            args=json.dumps([instance.id])
        )
