import datetime
import json
from django.utils import timezone


from google_maps_parser_api.settings import URL
from gmaps.models import PlaceType, Coordinate, TaskResult, TaskTemplate, Credential, Schedule
from gmaps.models import WAITING, CANCELED, RUNNING, DONE, ERROR, STOPPED, SENT
from django.test import TestCase

from gmaps.models import POSSIBLE_STATUSES, IS_START_DATE_UPDATE_REQUIRED, IS_FINISH_DATE_UPDATE_REQUIRED


class TestAction(TestCase):
    def setUp(self):
        self.place = PlaceType.objects.create(value="test_place")
        self.coordinates = Coordinate.objects.create(name="test_coords", lat=12.1, lon=24.1)
        self.credentials = Credential.objects.create(token="secret", name="token_name")
        self.schedule = Schedule.objects.create(name="test_schedule")
        self.task_template = TaskTemplate.objects.create(place=self.place, coordinates=self.coordinates, credentials=self.credentials, schedule=self.schedule)

    def __create_task_with_status(self, status):
        task = TaskResult.objects.create(template=self.task_template, status=status)
        task.save()
        if IS_FINISH_DATE_UPDATE_REQUIRED.get(status):
            task.finish = timezone.now()
        if IS_START_DATE_UPDATE_REQUIRED.get(status):
            task.start = timezone.now()
        task.save()
        return task

    def test_status_change_methods(self):
        for status, next_statuses in POSSIBLE_STATUSES.items():
            for next_status in next_statuses:
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
                with self.assertRaises(TaskResult.InvalidStatusChange):
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

    def test_to_json(self):
        task = self.__create_task_with_status(WAITING)
        self.assertEquals(json.dumps(task), '{"template": {"place": "test_place", "coordinates": {"name": "test_coords", "lon": 24.1, "lat": 12.1, "radius": 10000}, "token": "secret"}, "id": 1}')

    def test_actions_for_task_with_status_waiting(self):
        task = self.__create_task_with_status(WAITING)
        self.assertEquals(task.actions, {'cancel': f"{URL}/gmaps/task/1/cancel"})

    def test_actions_for_task_with_status_sent(self):
        task = self.__create_task_with_status(SENT)
        self.assertEquals(task.actions, {'cancel': f"{URL}/gmaps/task/1/cancel"})

    def test_actions_for_task_with_status_running(self):
        task = self.__create_task_with_status(RUNNING)
        self.assertEquals(task.actions, {'stop': f"{URL}/gmaps/task/1/stop"})

    def test_actions_for_task_with_status_error(self):
        task = self.__create_task_with_status(ERROR)
        self.assertEquals(task.actions, {})

    def test_change_status_to_stopped_from_correct_status(self):
        task = self.__create_task_with_status(RUNNING)
        task.change_status_to_stopped()
        self.assertEquals(task.status, STOPPED)

    def test_change_status_to_sent(self):
        task = self.__create_task_with_status(WAITING)
        task.change_status_to_sent()
        self.assertEquals(task.status, SENT)

    def test_change_status_to_running(self):
        task = self.__create_task_with_status(SENT)
        task.change_status_to_running()
        self.assertEquals(task.status, RUNNING)

    def test_change_status_to_canceled(self):
        task = self.__create_task_with_status(WAITING)
        task.change_status_to_canceled()
        self.assertEquals(task.status, CANCELED)

    def test_change_status_to_done(self):
        task = self.__create_task_with_status(RUNNING)
        task.change_status_to_done()
        self.assertEquals(task.status, DONE)

    def test_change_status_to_error(self):
        task = self.__create_task_with_status(RUNNING)
        task.change_status_to_error()
        self.assertEquals(task.status, ERROR)
