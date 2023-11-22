import json
from gmaps.models import Credential, Task, PeriodicTask, Coordinate, PlaceType, Category, CrontabSchedule
from django.test import TestCase


class TestCredentials(TestCase):
    def setUp(self):
        self.token_name = "test_name"
        self.secret_token = "secret_token"

        self.credentials = Credential.objects.create(name=self.token_name, token=self.secret_token)
        self.coordinates = Coordinate.objects.create(lon=12, lat=13, radius=142)
        self.category = Category.objects.create(value="category")
        self.place = PlaceType.objects.create(value="place", category=self.category)
        self.schedule = CrontabSchedule.objects.create()
        self.task = Task.objects.create(credentials=self.credentials, coordinates=self.coordinates, place=self.place,
                                        schedule=self.schedule)

    def test_str_method(self):
        self.assertEquals(str(self.credentials), self.token_name)

    def test_repr_method(self):
        self.assertEquals(repr(self.credentials), self.token_name)

    def test_api_key_update(self):
        new_secret_token = "new_secret_token"
        self.credentials.token = new_secret_token
        self.credentials.save()

        periodic_task = PeriodicTask.objects.get(name=self.task.place.value)
        periodic_task_args = json.loads(periodic_task.args)
        self.assertEquals(periodic_task_args[1], new_secret_token)
