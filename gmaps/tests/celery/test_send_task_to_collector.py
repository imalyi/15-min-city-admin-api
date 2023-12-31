from google_maps_parser_api.celery import send_gmaps_task_to_collector
from django.test import TestCase
from gmaps.models import PlaceType, Coordinate, Task, TaskResult, Credential, CrontabSchedule
import unittest
import os


class TestCeleryTasks(TestCase):
    def __create_task(self):
        secret = os.environ.get("GMAPS_TOKEN", "secret")
        place = PlaceType.objects.create(value="doctor")
        coordinates = Coordinate.objects.create(name="gdansk", lat=54.3520500, lon=18.6463700, radius=1000)
        credentials = Credential.objects.create(name="test", token=secret)
        schedule = CrontabSchedule.objects.create()
        self.task = Task.objects.create(place=place, coordinates=coordinates, credentials=credentials, schedule=schedule)
        self.task.save()

    def setUp(self):
        self.__create_task()

    @unittest.skipIf(os.environ.get("GMAPS_TOKEN", True), 'To run tests, set a Google Maps API key to OS variable GMAPS_TOKEN')
    def test_send_task_to_collector_with_no_errors(self):
        send_gmaps_task_to_collector(self.task.id, self.task.credentials.token, self.task.place.value,
                                     (self.task.coordinates.lat, self.task.coordinates.lon), self.task.coordinates.radius)
        task_result = TaskResult.objects.get(task=self.task)
        self.assertEquals(task_result.items_collected, 60)
        self.assertEquals(task_result.error, None)
        self.assertNotEquals(task_result.start, None)
        self.assertNotEquals(task_result.finish, None)

    def test_send_task_to_collector_with_invalid_api_key(self):
        self.task.credentials.token = "invalid"
        self.task.save()
        self.task.credentials.save()
        self.task.refresh_from_db()

        send_gmaps_task_to_collector(self.task.id, self.task.credentials.token, self.task.place.value,
                                     (self.task.coordinates.lat, self.task.coordinates.lon), self.task.coordinates.radius)
        self.assertNotEqual(TaskResult.objects.get(task=self.task).error, None)

    @unittest.skipIf(os.environ.get("GMAPS_TOKEN", True), 'To run tests, set a Google Maps API key to OS variable GMAPS_TOKEN')
    def test_send_task_to_collector_with_invalid_place(self):
        self.task.place.value = "incorrect"
        self.task.place.save()
        send_gmaps_task_to_collector(self.task.id, self.task.credentials.token, self.task.place.value,
                                     (self.task.coordinates.lat, self.task.coordinates.lon), self.task.coordinates.radius)
        self.assertNotEqual(TaskResult.objects.get(task=self.task).error, None)

    @unittest.skipIf(os.environ.get("GMAPS_TOKEN", True), 'To run tests, set a Google Maps API key to OS variable GMAPS_TOKEN')
    def test_send_task_to_collector_with_invalid_coordinates(self):
        self.task.coordinates.lon = 1421
        self.task.coordinates.lat = 2521
        self.task.coordinates.save()
        send_gmaps_task_to_collector(self.task.id, self.task.credentials.token, self.task.place.value,
                                     (self.task.coordinates.lat, self.task.coordinates.lon), self.task.coordinates.radius)
        self.assertNotEqual(TaskResult.objects.get(task=self.task).error, None)

