from gmaps.models import TaskResult, Task, WAITING, RUNNING, ERROR, DONE, Coordinate, Credential, Category, PlaceType, CrontabSchedule
from django.test import TestCase


CORRECT_STATUS_FLOW = [
    [WAITING, RUNNING],
    [RUNNING, DONE],
    [RUNNING, ERROR]
]


class TestTaskResult(TestCase):
    def setUp(self):
        self.credential = Credential.objects.create(name="token_name", token="secret")
        self.coordinates = Coordinate.objects.create(lon=12, lat=13, radius=142)
        self.category = Category.objects.create(value="category")
        self.place = PlaceType.objects.create(value="place", category=self.category)
        self.schedule = CrontabSchedule.objects.create()
        self.task = Task.objects.create(credentials=self.credential, coordinates=self.coordinates, place=self.place,
                                        schedule=self.schedule)
        self.task_result = TaskResult.objects.create(task=self.task)

    def test_incorrect_status_change(self):
        incorrect_status_pairs = []

        for status1 in [WAITING, RUNNING, ERROR, DONE]:
            for status2 in [WAITING, RUNNING, ERROR, DONE]:
                if status1 == status2:
                    continue
                if [status1, status2] in CORRECT_STATUS_FLOW:
                    continue
                incorrect_status_pairs.append([status1, status2])

        for from_, to in incorrect_status_pairs:
            with self.assertRaises(TaskResult.InvalidStatusChange):
                task_result = TaskResult.objects.create(task=self.task, status=from_)
                task_result.change_status(to)

    def test_correct_status_change(self):
        for from_, to in CORRECT_STATUS_FLOW:
            task_result = TaskResult.objects.create(task=self.task, status=from_)
            task_result.change_status(to)

    def test_update_progress_with_incorrect_value(self):
        with self.assertRaises(TaskResult.InvalidProgressValue):
            self.task_result.update_progress("124f")

    def test_update_progress_with_incorrect_status(self):
        for status in [WAITING, DONE, ERROR]:
            with self.assertRaises(TaskResult.InvalidStatusForProgressTrack):
                task_result = TaskResult.objects.create(task=self.task, status=status)
                task_result.update_progress(12)

    def test_update_progress(self):
        task_result = TaskResult.objects.create(task=self.task, status=RUNNING)
        task_result.update_progress(14)
        self.assertEquals(task_result.items_collected, 14)