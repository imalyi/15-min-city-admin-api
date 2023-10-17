import datetime

from gmaps.models import SubTask, PlaceType, Coordinate
from gmaps.models import WAITING, CANCELED, RUNNING, DONE, ERROR, STOPPED
from django.test import TestCase

from gmaps.models import POSSIBLE_STATUSES, IS_START_DATE_UPDATE_REQUIRED, IS_FINISH_DATE_UPDATE_REQUIRED


class TestAction(TestCase):
    def setUp(self):
        self.place = PlaceType.objects.create(value="test_place")
        self.coordinates = Coordinate.objects.create(name="test_coords", lat=12.1, lon=24.1)

    def __create_subtask_with_status(self, status):
        subtask = SubTask.objects.create(place=self.place, coordinates=self.coordinates, status=status)
        if IS_FINISH_DATE_UPDATE_REQUIRED.get(status):
            subtask.finish = datetime.datetime.now()
        if IS_START_DATE_UPDATE_REQUIRED.get(status):
            subtask.start = datetime.datetime.now()
        subtask.save()
        return subtask

    def test_status_change_methods(self):
        for status, next_statuses in POSSIBLE_STATUSES.items():
            for next_status in next_statuses:
                # create subtask with proper start, finish properties for status
                subtask = self.__create_subtask_with_status(status)
                subtask.change_status(next_status)

                self.assertEquals(subtask.status, next_status)
                if next_status in IS_START_DATE_UPDATE_REQUIRED:
                    self.assertIsInstance(subtask.start, datetime.datetime)

    def test_update_progress(self):
        subtask = self.__create_subtask_with_status(WAITING)
        with self.assertRaises(subtask.InvalidStatusForProgressTrack):
            subtask.update_progress(15)

        subtask = self.__create_subtask_with_status(RUNNING)
        with self.assertRaises(subtask.InvalidProgressValue):
            subtask.update_progress('14f')

        subtask.update_progress(15)
        self.assertEquals(subtask.items_collected, 15)
