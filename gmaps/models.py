from datetime import datetime

from django.db.models import Model, IntegerField, CharField, ManyToManyField, ForeignKey, DateTimeField, Choices, FloatField, DO_NOTHING, CASCADE
from django.db.models import Sum, Manager
from django.db.models.signals import pre_save
from django.dispatch import receiver

WAITING = 'waiting'
DONE = 'done'
RUNNING = 'running'
ERROR = 'error'
STOPPED = 'stopped'
CANCELED = 'canceled'




class Credential(Model):
    token = CharField(max_length=560)
    name = CharField(max_length=500)
    request_limit = IntegerField(default=5000)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class PlaceType(Model):
    value = CharField(max_length=250, unique=True)

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class Coordinate(Model):
    name = CharField(max_length=250)
    lon = FloatField()
    lat = FloatField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class SubTask(Model):
    class InvalidStatusChange(Exception):
        pass

    class InvalidStatusForProgressTrack(Exception):
        pass

    class InvalidProgressValue(Exception):
        pass


    STATUS = (
        (WAITING, 'waiting'),
        (DONE, 'done'),
        (RUNNING, 'running'),
        (ERROR, 'error'),
        (STOPPED, 'stopped'),
        (CANCELED, 'canceled')
    )

    place = ForeignKey(PlaceType, on_delete=DO_NOTHING)
    coordinates = ForeignKey(Coordinate, on_delete=DO_NOTHING)
    status = CharField(choices=STATUS, default=WAITING, max_length=20)
    start = DateTimeField(null=True, default=None, blank=True)
    finish = DateTimeField(null=True, default=None, blank=True)
    created = DateTimeField(auto_now=True)
    items_collected = IntegerField(default=0) # received items on task(count of api tokens used)

    def __str__(self):
        return f"{self.place}-{str(self.created)}"

    def __repr__(self):
        return  f"{self.place}-{str(self.created)}"


    #TODO rewrite this
    def change_status_to_error(self):
        if self.status == RUNNING:
            self.status = ERROR
            self.finish = datetime.now()
            self.save()
        else:
            raise self.InvalidStatusChange(f"Cant change status to {ERROR} for task with status {self.status}")

    def change_status_to_done(self):
        if self.status == RUNNING:
            self.status = DONE
            self.finish = datetime.now()
            self.save()
        else:
            raise self.InvalidStatusChange(f"Cant change status to {DONE} for task with status {self.status}")

    def start_if_waiting(self):
        if self.status == WAITING:
            self.status = RUNNING
            self.start = datetime.now()
            self.save()
        else:
            raise self.InvalidStatusChange(f"Cant change status to {RUNNING} for task with status {self.status} and finish data {self.finish}")

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

    def cancel_if_waiting(self):
        if self.status == WAITING:
            self.status = CANCELED
            self.finish = datetime.now()
            self.save()
        else:
            raise self.InvalidStatusChange(f"Cant change status to {CANCELED} for task with status {self.status}")


class Task(Model):
    STATUS = (
        (WAITING, 'waiting'),
        (DONE, 'done'),
        (RUNNING, 'running'),
        (ERROR, 'error'),
        (STOPPED, 'stopped'),
        (CANCELED, 'canceled')
    )

    name = CharField(max_length=250)
    sub_task = ManyToManyField(SubTask)
    date = DateTimeField(auto_now=True)
    credentials = ForeignKey(Credential, on_delete=DO_NOTHING)
    status = CharField(choices=STATUS, default=WAITING, max_length=20)

    @property
    def subtask_count(self):
        return self.sub_task.count()

    @property
    def items_collected(self):
        return self.sub_task.aggregate(Sum('items_collected'))['items_collected__sum']
    #TODO: change on start_date, finish_date, which can be Null if not started and not finished
    @property
    def is_start(self):
        return self.sub_task.filter('start')

    @property
    def is_start(self):
        return self.sub_task.filter(start__isnull=False).exists()

    @property
    def is_finish(self):
        return self.sub_task.filter(finish__isnull=False).exists()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
