import datetime
import json

from google_maps_parser_api.settings import URL
from gmaps.models import PlaceType, Coordinate, Task, TaskTemplate, Credential, Schedule
from gmaps.models import WAITING, CANCELED, RUNNING, DONE, ERROR, STOPPED, SENT
from django.test import TestCase

from gmaps.models import POSSIBLE_STATUSES, IS_START_DATE_UPDATE_REQUIRED, IS_FINISH_DATE_UPDATE_REQUIRED


class TestAction(TestCase):
    def setUp(self):
        self.name = "name"
        self.lon = 123.1
        self.lat = 124.1
        self.radius = 1414
        self.coordinate = Coordinate.objects.create(name=self.name, lon=self.lon, lat=self.lat, radius=self.radius)

    def test_str_method(self):
        self.assertEquals(str(self.coordinate), self.name)

    def test_repr_method(self):
        self.assertEquals(repr(self.coordinate), self.name)

    def test_to_json(self):
        self.assertEquals(json.dumps(self.coordinate), '{"name": "name", "lon": 123.1, "lat": 124.1, "radius": 1414}')
