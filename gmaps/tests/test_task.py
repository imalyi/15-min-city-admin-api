import datetime

from gmaps.models import SubTask, PlaceType, Coordinate, Task, Credential
from gmaps.models import WAITING, CANCELED, RUNNING, DONE, ERROR, STOPPED
from django.test import TestCase

from gmaps.models import IS_START_DATE_UPDATE_REQUIRED, IS_FINISH_DATE_UPDATE_REQUIRED


class TestTaskModel(TestCase):
    def setUp(self):
        self.place = PlaceType.objects.create(value="test_place")
        self.coordinates = Coordinate.objects.create(name="test_coords", lat=12.1, lon=24.1)
        self.credentials = Credential.objects.create(token='asf', name='asf')

    def __create_subtask_with_status(self, status):
        subtask = SubTask.objects.create(place=self.place,
                                         coordinates=self.coordinates,
                                         status=status)
        if IS_FINISH_DATE_UPDATE_REQUIRED.get(status):
            subtask.finish = datetime.datetime.now()
        if IS_START_DATE_UPDATE_REQUIRED.get(status):
            subtask.start = datetime.datetime.now()
        subtask.save()
        return subtask

    def __create_subtasks(self, status):
        subtasks = []
        for i in range(3):
            subtasks.append(self.__create_subtask_with_status(status))
        return subtasks

    def test_subtask_count(self):
        for status in [WAITING, RUNNING, ERROR, DONE, STOPPED, CANCELED]:
            subtasks = self.__create_subtasks(status)
            task = Task.objects.create(name='Test', credentials=self.credentials)
            task.sub_task.set(subtasks)
            task.save()

            results = {
                WAITING: task.waiting_subtask_count,
                RUNNING: task.running_subtask_count,
                ERROR: task.error_subtask_count,
                DONE: task.done_subtask_count,
                STOPPED: task.stopped_subtask_count,
                CANCELED: task.canceled_subtask_count
            }
            for result_status, value in results.items():
                if result_status == status:
                    self.assertEquals(3, value)
                else:
                    self.assertEquals(0, value)
