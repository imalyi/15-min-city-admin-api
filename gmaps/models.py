import json
from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework.reverse import reverse, reverse_lazy
from django.db.models import Model, IntegerField, CharField, ForeignKey, DateTimeField, FloatField, CASCADE
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask, CrontabSchedule
from django.db import transaction
from google_maps_parser_api.settings import URL

WAITING = 'waiting'
RUNNING = 'running'
DONE = 'done'
ERROR = 'error'

STATUS_CHOICES = (
    (WAITING, WAITING),
    (RUNNING, RUNNING),
    (DONE, DONE),
    (ERROR, ERROR)
)

POSSIBLE_STATUSES = {
    WAITING: [RUNNING],
    RUNNING: [ERROR, DONE],
    DONE: [],
    ERROR: [],
}


IS_FINISH_DATE_UPDATE_REQUIRED = {
    WAITING: False,
    RUNNING: False,
    DONE: True,
    ERROR: True,
}

IS_START_DATE_UPDATE_REQUIRED = {
    WAITING: False,
    RUNNING: True,
    DONE: False,
    ERROR: False,
}


class Credential(Model):
    token = CharField(max_length=40)
    name = CharField(max_length=250)

    class Meta:
        unique_together = ('token', 'name')

    def save(self, *args, **kwargs):
        super(Credential, self).save(*args, **kwargs)
        try:
            task_with_this_credentials = Task.objects.filter(credentials=self)
            for task in task_with_this_credentials:
                periodic_task = PeriodicTask.objects.get(name=task.place.value)
                old_periodic_task_args = json.loads(periodic_task.args)
                old_periodic_task_args[1] = self.token
                periodic_task.args = json.dumps(old_periodic_task_args)
                periodic_task.save()
        except Task.DoesNotExist:
            return

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Category(Model):
    value = CharField(max_length=250, unique=True)

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class PlaceType(Model):
    value = CharField(max_length=250, unique=True)
    category = ForeignKey(Category, blank=True, null=True, default=None, on_delete=CASCADE)

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class Coordinate(Model):
    name = CharField(max_length=250)
    lon = FloatField()
    lat = FloatField()
    radius = IntegerField(default=10000)

    class Meta:
        unique_together = ('name', 'lon', 'lat', 'radius', )

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Task(Model):
    credentials = ForeignKey(Credential, on_delete=CASCADE)
    coordinates = ForeignKey(Coordinate, on_delete=CASCADE)
    place = ForeignKey(PlaceType, on_delete=CASCADE, unique=True)
    schedule = ForeignKey(CrontabSchedule, on_delete=CASCADE)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super(Task, self).save(*args, **kwargs)
            PeriodicTask.objects.create(
                name=self.place,
                task="google_maps_parser_api.celery.send_task_to_collector",
                crontab_id=self.schedule.id,
                args=json.dumps([self.pk, self.credentials.token,
                                 self.place.value,
                                 (self.coordinates.lat, self.coordinates.lon),
                                 self.coordinates.radius])
            )


    @property
    def last_status(self):
        try:
            return TaskResult.objects.filter(task=self).order_by('-finish').first().status
        except AttributeError:
            return None

    @property
    def actions(self):
        return {"start:": URL + reverse("task-detail", args=[self.id]) + 'start/'}

    def __repr__(self):
        return self.place.value

    def __str__(self):
        return self.place.value


@receiver(post_delete, sender=Task)
def delete_all_periodic_task_for_task(sender, instance, **kwargs):
    try:
        PeriodicTask.objects.get(name=instance.place.value).delete()
    except PeriodicTask.DoesNotExist:
        pass
        #TODO add sending error to log


class TaskResult(Model):
    class InvalidStatusChange(Exception):
        pass

    class InvalidStatusForProgressTrack(Exception):
        pass

    class InvalidProgressValue(Exception):
        pass

    task = ForeignKey(Task, on_delete=CASCADE)
    start = DateTimeField(null=True, default=None, blank=True)
    finish = DateTimeField(null=True, default=None, blank=True)
    items_collected = IntegerField(default=0)
    status = CharField(choices=STATUS_CHOICES, default=WAITING, max_length=20)
    error = CharField(max_length=2600, default=None, blank=True, null=True)

    def change_status(self, target_status):
        if target_status in POSSIBLE_STATUSES.get(self.status):
            self.status = target_status
        else:
            raise self.InvalidStatusChange(f"Cant change status to {target_status} for task with status {self.status}, start: {self.start}, finish: {self.finish}")
        if IS_FINISH_DATE_UPDATE_REQUIRED.get(target_status, False):
            self.finish = timezone.now()
        if IS_START_DATE_UPDATE_REQUIRED.get(target_status, False):
            self.start = timezone.now()
        self.save()

    def change_status_to_error(self, error=''):
        self.error = error
        self.change_status(ERROR)

    def change_status_to_running(self):
        self.change_status(RUNNING)

    def change_status_to_done(self):
        self.change_status(DONE)

    def update_progress(self, progress):
        try:
            progress = int(progress)
        except ValueError:
            raise self.InvalidProgressValue(f"{progress} cant be converted to int")
        if self.status == RUNNING:
            self.items_collected += int(progress)
            self.save()
        else:
            raise self.InvalidStatusForProgressTrack(f"Cant increment progress for status {self.status}")
