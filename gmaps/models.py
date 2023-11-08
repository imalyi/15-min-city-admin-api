
from datetime import datetime
from django.db.models import Model, IntegerField, CharField, ManyToManyField, ForeignKey, DateTimeField, Choices, FloatField, DO_NOTHING, CASCADE
from django.db.models import Sum
from rest_framework.reverse import reverse
from status.SUB_TASK_STATUSES import *
from google_maps_parser_api.settings import URL

STATUS_URL = {
    RUNNING: 'start',
    STOPPED: 'stop',
    CANCELED: 'cancel',
}

POSSIBLE_STATUSES = {
    WAITING: [RUNNING, CANCELED],
    RUNNING: [ERROR, STOPPED, DONE],
    DONE: [],
    ERROR: [],
    STOPPED: [],
    CANCELED: []
}


IS_FINISH_DATE_UPDATE_REQUIRED = {
    WAITING: False,
    RUNNING: False,
    DONE: True,
    ERROR: True,
    STOPPED: True,
    CANCELED: True
}

IS_START_DATE_UPDATE_REQUIRED = {
    WAITING: False,
    RUNNING: True,
    DONE: False,
    ERROR: False,
    STOPPED: False,
    CANCELED: False
}


class Credential(Model):
    token = CharField(max_length=560)
    name = CharField(max_length=500)

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
    radius = IntegerField(default=10000)

    class Meta:
        unique_together = ('name', 'lon', 'lat', 'radius', )

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
    status = CharField(choices=STATUS, default=WAITING, max_length=20)
    start = DateTimeField(null=True, default=None, blank=True)
    finish = DateTimeField(null=True, default=None, blank=True)
    created = DateTimeField(auto_now=True)
    items_collected = IntegerField(default=0)

    @property
    def credentials(self):
        subtask = self.subtask.first()
        if subtask:
            return subtask.credentials.token
        else:
            return None

    def __str__(self):
        return f"{self.place}-{str(self.created)}"

    def __repr__(self):
        return f"{self.place}-{str(self.created)}"

    @property
    def actions(self):
        res = {}
        for possible_status in POSSIBLE_STATUSES.get(self.status):
            if STATUS_URL.get(possible_status):
                res[STATUS_URL.get(possible_status)] = URL + reverse('subtask') + str(self.pk) + "/" +STATUS_URL.get(possible_status)
        return res

    def change_status(self, target_status):
        if target_status in POSSIBLE_STATUSES.get(self.status):
            self.status = target_status
        else:
            raise self.InvalidStatusChange(f"Cant change status to {target_status} for task with status {self.status}, start: {self.start}, finish: {self.finish}")
        if IS_FINISH_DATE_UPDATE_REQUIRED.get(target_status, False):
            self.finish = datetime.now()
        if IS_START_DATE_UPDATE_REQUIRED.get(target_status, False):
            self.start = datetime.now()
        self.save()

    def change_status_to_stopped(self):
        self.change_status(STOPPED)

    def change_status_to_error(self):
        self.change_status(ERROR)

    def change_status_to_running(self):
        self.change_status(RUNNING)

    def change_status_to_done(self):
        self.change_status(DONE)

    def change_status_to_canceled(self):
        self.change_status(CANCELED)

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


class Task(Model):
    name = CharField(max_length=250)
    sub_task = ManyToManyField(SubTask, related_name='subtask')
    create_date = DateTimeField(auto_now=True)
    credentials = ForeignKey(Credential, on_delete=DO_NOTHING)
    coordinates = ForeignKey(Coordinate, on_delete=DO_NOTHING)

    def start(self):
        for subtask in self.sub_task.filter(status=WAITING):
            subtask.status = RUNNING
            subtask.save()

    def cancel(self):
        for subtask in self.sub_task.filter(status=WAITING):
            subtask.status = CANCELED
            subtask.save()

    def stop(self):
        for subtask in self.sub_task.filter(status=RUNNING):
            subtask.status = STOPPED
            subtask.save()

    @property
    def last_change_date(self):
        start = self.sub_task.latest('start').start
        finish = self.sub_task.latest('finish').finish
        try:
            return max([start, finish])
        except TypeError:
            return (start or finish)

    @property
    def subtask_count(self):
        return self.sub_task.count()

    @property
    def items_collected(self):
        return self.sub_task.aggregate(Sum('items_collected'))['items_collected__sum']

    @property
    def waiting_subtask_count(self):
        return self.sub_task.filter(status=WAITING).count()

    @property
    def running_subtask_count(self):
        return self.sub_task.filter(status=RUNNING).count()

    @property
    def done_subtask_count(self):
        return self.sub_task.filter(status=DONE).count()

    @property
    def canceled_subtask_count(self):
        return self.sub_task.filter(status=CANCELED).count()

    @property
    def stopped_subtask_count(self):
        return self.sub_task.filter(status=STOPPED).count()

    @property
    def error_subtask_count(self):
        return self.sub_task.filter(status=ERROR).count()

    @property
    def status(self):
        if self.error_subtask_count > 0:
            return ERROR
        if self.done_subtask_count == self.subtask_count - self.stopped_subtask_count - self.canceled_subtask_count:
            return DONE
        if self.running_subtask_count > 0:
            return RUNNING
        if self.waiting_subtask_count == self.subtask_count - self.stopped_subtask_count - self.canceled_subtask_count:
            return WAITING
        if self.canceled_subtask_count == self.subtask_count:
            return CANCELED
        if self.stopped_subtask_count == self.subtask_count:
            return STOPPED

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
