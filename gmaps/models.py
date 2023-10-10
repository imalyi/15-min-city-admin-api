from django.db.models import Model, IntegerField, CharField, ManyToManyField, ForeignKey, DateTimeField, Choices, FloatField, DO_NOTHING, CASCADE

from django.db.models import Sum


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


class Status(Model):
    WAITING = 'W'
    DONE = 'D'
    RUNNING = 'R'
    ERROR = 'E'
    STOPPED = 'S'

    STATUS = (
        (WAITING, 'Waiting'),
        (DONE, 'Done'),
        (RUNNING, 'Running'),
        (ERROR, 'Error'),
        (STOPPED, 'Stopped')
    )
    value = CharField(choices=STATUS, max_length=1, unique=True)

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
    place = ForeignKey(PlaceType, on_delete=DO_NOTHING)
    coordinates = ForeignKey(Coordinate, on_delete=DO_NOTHING)
    status = ForeignKey(Status, on_delete=DO_NOTHING)
    start = DateTimeField(null=True, default=None, blank=True)
    finish = DateTimeField(null=True, default=None, blank=True)
    created = DateTimeField(auto_now=True)
    items_collected = IntegerField(default=0) # received items on task(amount of api keys)

    def __str__(self):
        return str(self.start)

    def __repr__(self):
        return str(self.start)


class Task(Model):
    name = CharField(max_length=250)
    sub_task = ManyToManyField(SubTask)
    date = DateTimeField(auto_now=True)
    credentials = ForeignKey(Credential, on_delete=DO_NOTHING)

    @property
    def subtask_count(self):
        return self.sub_task.count()

    @property
    def items_collected(self):
        return self.sub_task.aggregate(Sum('items_collected'))['items_collected__sum']

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
