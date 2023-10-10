from django.db.models import Model, IntegerField, CharField, ManyToManyField, ForeignKey, DateTimeField, Choices, FloatField, DO_NOTHING, CASCADE


class Credential(Model):
    token = CharField(max_length=560)
    name = CharField(max_length=500)
    request_limit = IntegerField(default=5000) # per day

    def __repr__(self):
        return f"{self.name}(limit: {self.request_limit})"

    def __str__(self):
        return f"{self.name}(limit: {self.request_limit})"


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
    start = DateTimeField()  # make null true
    finish = DateTimeField()  # make null true
    created = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.place}, {self.coordinates}, {self.coordinates}, {self.start} - {self.finish}"

    def __repr__(self):
        return f"{self.place}, {self.coordinates}, {self.coordinates}, {self.start} - {self.finish}"


class RequestData(Model):
    """ Store info about amount of request to api"""
    key = ForeignKey(Credential, on_delete=DO_NOTHING)
    count = IntegerField(default=0)
    time = DateTimeField(auto_now=True)


class Task(Model):
    name = CharField(max_length=250)

    sub_task = ManyToManyField(SubTask)
    date = DateTimeField(auto_now=True)
    credentials = ForeignKey(Credential, on_delete=DO_NOTHING)

    def __repr__(self):
        return f"{self.client} - {self.date} - {self.credentials}"
