import datetime
import json

from google_maps_parser_api.settings import URL
from gmaps.models import PlaceType, Coordinate, TaskResult, TaskTemplate, Credential, Schedule
from gmaps.models import WAITING, CANCELED, RUNNING, DONE, ERROR, STOPPED, SENT
from django.test import TestCase

from gmaps.models import POSSIBLE_STATUSES, IS_START_DATE_UPDATE_REQUIRED, IS_FINISH_DATE_UPDATE_REQUIRED


class TestAction(TestCase):
    def setUp(self):
        self.value = "place_type"
        self.place = PlaceType.objects.create(value=self.value)

    def test_str_method(self):
        self.assertEquals(str(self.place), self.value)

    def test_repr_method(self):
        self.assertEquals(repr(self.place), self.value)

    def test_to_json(self):
        self.assertEquals(json.dumps(self.place), f'"{self.value}"')
