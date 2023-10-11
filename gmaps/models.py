import datetime

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

    #TODO: add constraint: if finished, then status cant be waiting, stopped or error. if
    def __str__(self):
        return str(self.start)

    def __repr__(self):
        return str(self.start)

    def change_status_to_error(self):
        if self.status == RUNNING:
            self.status = ERROR
            self.finish = datetime.now()
            self.save()

    def change_status_to_done(self):
        if self.status == RUNNING:
            self.status = DONE
            self.finish = datetime.now()
            self.save()

    def start_if_waiting(self):
        if self.status == WAITING and not self.finish:
            self.status = RUNNING
            self.start = datetime.now()
            self.save()

    def update_progress(self, progress):
        if self.status == RUNNING:
            try:
                self.items_collected += int(progress)
                self.save()
            except ValueError:
                pass  # Handle the error or log it here if necessary


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