import datetime
import json

from google_maps_parser_api.settings import URL
from gmaps.models import PlaceType, Coordinate, Task, TaskTemplate, Credential, Schedule
from django.test import TestCase


class TestAction(TestCase):
    def setUp(self):
        credentials = Credential.objects.create(name="credentials_name", token="secret")
        coordinates = Coordinate.objects.create(name="city", lon=12.1, lat=13.1, radius=1)
        self.place = PlaceType.objects.create(value="place_test")
        schedule = Schedule.objects.create(name="every week")
        self.task_template = TaskTemplate.objects.create(credentials=credentials, coordinates=coordinates, place=self.place, schedule=schedule)

    def test_str_method(self):
        self.assertEquals(str(self.task_template), self.place.value)

    def test_repr_method(self):
        self.assertEquals(repr(self.task_template), self.place.value)

    def test_to_json(self):
        self.assertEquals(json.dumps(self.task_template), '{"place": "place_test", "coordinates": {"name": "city", "lon": 12.1, "lat": 13.1, "radius": 1}, "token": "secret"}')