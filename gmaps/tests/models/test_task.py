from gmaps.models import Task, Credential, Coordinate, Category, PlaceType, CrontabSchedule, PeriodicTask
from django.test import TestCase


class TestTask(TestCase):
    def setUp(self):
        self.credential = Credential.objects.create(name="token_name", token="secret")
        self.coordinates = Coordinate.objects.create(lon=12, lat=13, radius=142)
        self.category = Category.objects.create(value="category")
        self.place = PlaceType.objects.create(value="place", category=self.category)
        self.schedule = CrontabSchedule.objects.create()
        self.task = Task.objects.create(credentials=self.credential, coordinates=self.coordinates, place=self.place,
                                        schedule=self.schedule)

    def test_periodic_task_creation(self):
        self.assertNotEquals(PeriodicTask.objects.get(name=self.task.place.value).name, None)

    def test_periodic_task_deletion(self):
        self.task.delete()
        self.assertEquals(Task.objects.all().count(), 0)
        self.assertEquals(PeriodicTask.objects.all().count(), 0)

    def test_task_deletion_with_no_periodic_task(self):
        PeriodicTask.objects.all().delete()
        self.task.delete()
        self.assertEquals(Task.objects.all().count(), 0)