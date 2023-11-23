from gmaps.models import PlaceType
from django.test import TestCase


class TestPlaceType(TestCase):
    def setUp(self):
        self.value = "place_type"
        self.place = PlaceType.objects.create(value=self.value)

    def test_str_method(self):
        self.assertEquals(str(self.place), self.value)

    def test_repr_method(self):
        self.assertEquals(repr(self.place), self.value)
