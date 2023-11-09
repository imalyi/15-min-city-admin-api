import datetime

from gmaps.models import PlaceType, Coordinate, Task, TaskTemplate, Credential
from gmaps.models import WAITING, CANCELED, RUNNING, DONE, ERROR, STOPPED, SENT
from django.test import TestCase

from gmaps.models import POSSIBLE_STATUSES, IS_START_DATE_UPDATE_REQUIRED, IS_FINISH_DATE_UPDATE_REQUIRED


class TestAction(TestCase):
    def setUp(self):
        self.place = PlaceType.objects.create(value="test_place")
        self.coordinates = Coordinate.objects.create(name="test_coords", lat=12.1, lon=24.1)
        self.credentials = Credential.objects.create(token="secret", name="token_name")
        self.task_template = TaskTemplate(place=self.place, coordinates=self.coordinates, credentials=self.credentials)
        self.task_template.save()

    def __create_task_with_status(self, status):
        task = Task.objects.create(template=self.task_template, status=status)
        task.save()
        if IS_FINISH_DATE_UPDATE_REQUIRED.get(status):
            task.finish = datetime.datetime.now()
        if IS_START_DATE_UPDATE_REQUIRED.get(status):
            task.start = datetime.datetime.now()
        task.save()
        return task

    def test_status_change_methods(self):
        for status, next_statuses in POSSIBLE_STATUSES.items():
            for next_status in next_statuses:
                # create subtask with proper start, finish properties for status
                task = self.__create_task_with_status(status)
                task.change_status(next_status)
                self.assertEquals(task.status, next_status)
                if IS_START_DATE_UPDATE_REQUIRED.get(next_status, False):
                    self.assertNotEquals(task.start, None)
                task.delete()

    def test_status_change_method_to_incorrect_status(self):
        statuses = [WAITING, SENT, RUNNING, DONE, CANCELED, STOPPED, ERROR]
        for task_status in statuses:
            task = self.__create_task_with_status(task_status)
            for new_status in statuses:
                if new_status in POSSIBLE_STATUSES.get(task_status):
                    continue
                with self.assertRaises(Task.InvalidStatusChange):
                    task.change_status(new_status)

    def test_update_progress(self):
        task = self.__create_task_with_status(WAITING)
        with self.assertRaises(task.InvalidStatusForProgressTrack):
            task.update_progress(15)

        task = self.__create_task_with_status(RUNNING)
        with self.assertRaises(task.InvalidProgressValue):
            task.update_progress('14f')

        task.update_progress(15)
        self.assertEquals(task.items_collected, 15)