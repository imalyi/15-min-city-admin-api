from google_maps_parser_api.celery import send_task_to_collector
from django.test import TestCase
from gmaps.models import PlaceType, Coordinate, Task, TaskResult, Credential
from django_celery_beat.models import IntervalSchedule


class TestCeleryTasks(TestCase):
    def __create_task(self):
        place = PlaceType.objects.create(value="doctor")
        coordinates = Coordinate.objects.create(name="gdansk", lat=54.3520500, lon=18.6463700, radius=1000)
        credentials = Credential.objects.create(name="test", token="AIzaSyD-3QHRKuWp8ddXkpe8EIifKOkJ2SkfmOM")
        schedule = IntervalSchedule.objects.create(every=100, period=IntervalSchedule.DAYS)
        self.task = Task.objects.create(place=place, coordinates=coordinates, credentials=credentials, schedule=schedule)

    def setUp(self):
        self.__create_task()

    def test_send_task_to_collector(self):
        send_task_to_collector(self.task.id, self.task.credentials.token, self.task.place.value,
                               (self.task.coordinates.lat, self.task.coordinates.lon), self.task.coordinates.radius)

        task_result = TaskResult.objects.get(task=self.task)
        self.assertGreaterEqual(task_result.items_collected, 1)
        self.assertEquals(task_result.error, None)
        self.assertNotEquals(task_result.start, None)
        self.assertNotEquals(task_result.finish, None)
