import datetime
from django.test import TestCase
from openstreetmaps.models import OSMTask, OSMTaskResult, OSMError


class TaskModelTests(TestCase):
    def test_task_status_running(self):
        task = OSMTask.objects.create(region="Test Region")
        OSMTaskResult.objects.create(task=task)  # Create a running task result
        self.assertEqual(task.status, "RUNNING")

    def test_task_status_done(self):
        task = OSMTask.objects.create(region="Test Region")
        result = OSMTaskResult.objects.create(task=task, finish_date=datetime.datetime.now())
        self.assertEqual(task.status, "DONE")

    def test_task_status_done_with_errors(self):
        task = OSMTask.objects.create(region="Test Region")
        result = OSMTaskResult.objects.create(task=task, finish_date=datetime.datetime.now())
        OSMError.objects.create(task_result=result, data="Error Data", type="Error Type")
        self.assertEqual(task.status, "DONE_WITH_ERRORS")

    def test_task_status_unknown(self):
        task = OSMTask.objects.create(region="Test Region")
        self.assertEqual(task.status, "NEVER RUN")


class TaskResultModelTests(TestCase):
    def test_task_result_errors(self):
        task = OSMTask.objects.create(region="Test Region")
        result = OSMTaskResult.objects.create(task=task)
        self.assertEqual(result.errors, 0)

        # Add an error and check again
        OSMError.objects.create(task_result=result, data="Error Data", type="Error Type")
        self.assertEqual(result.errors, 1)

class ErrorModelTests(TestCase):
    def test_error_creation(self):
        task = OSMTask.objects.create(region="Test Region")
        result = OSMTaskResult.objects.create(task=task)
        error = OSMError.objects.create(task_result=result, data="Error Data", type="Error Type")

        self.assertEqual(error.task_result, result)
        self.assertEqual(error.data, "Error Data")
        self.assertEqual(error.type, "Error Type")
