from gmaps.models import Coordinate
from django.test import TestCase


class TestCoordinates(TestCase):
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
