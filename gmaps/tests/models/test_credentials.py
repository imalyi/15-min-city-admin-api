import datetime
import json

from google_maps_parser_api.settings import URL
from gmaps.models import PlaceType, Coordinate, TaskResult, TaskTemplate, Credential, Schedule
from gmaps.models import WAITING, CANCELED, RUNNING, DONE, ERROR, STOPPED, SENT
from django.test import TestCase

from gmaps.models import POSSIBLE_STATUSES, IS_START_DATE_UPDATE_REQUIRED, IS_FINISH_DATE_UPDATE_REQUIRED


class TestAction(TestCase):
    def setUp(self):
        self.token_name = "test_name"
        self.secret_token = "secret_token"
        self.credentials = Credential.objects.create(name=self.token_name, token=self.secret_token)

    def test_str_method(self):
        self.assertEquals(str(self.credentials), self.token_name)

    def test_repr_method(self):
        self.assertEquals(repr(self.credentials), self.token_name)

    def test_to_json(self):
        self.assertEquals(json.dumps(self.credentials), f'"{self.secret_token}"')
