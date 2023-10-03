from django.db.models import Model, IntegerField, CharField, ManyToManyField, ForeignKey, DateTimeField, Choices, FloatField


class Client(Model):
    name = CharField(max_length=250)
    last_online = DateTimeField(blank=True, default=None)

    def __str__(self):
        return f"{self.name}({self.last_online})"

    def __repr__(self):
        return f"{self.name}({self.last_online})"


class Credentials(Model):
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
    values = CharField(choices=STATUS, max_length=1)


class Coordinate(Model):
    name = CharField(max_length=250)
    lon = FloatField()
    lat = FloatField()


class SubTask(Model):
    place = ForeignKey(PlaceType)
    coordinates = ForeignKey(Coordinate)
    status = ForeignKey(Status)
    start = DateTimeField()
    finish = DateTimeField()
    created = DateTimeField(auto_now=True)


class RequestData(Model):
    """ Store info about amount of request to api"""
    key = ForeignKey(Credentials)
    count = IntegerField(default=0)
    time = DateTimeField(auto_now=True)


class Task(Model):
    client = ForeignKey(Client)
    sub_task = ManyToManyField(SubTask)
    date = DateTimeField(auto_now=True)
    credentials = ForeignKey(Credentials)

    def __repr__(self):
        return f"{self.client} - {self.date} - {self.credentials}"