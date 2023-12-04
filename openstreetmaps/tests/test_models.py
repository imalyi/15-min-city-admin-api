from django.test import TestCase, Client
from django.contrib.auth.models import User
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from openstreetmaps.models import OSMTask, OSMTaskResult, OSMError
import json
import datetime

class OSMTaskModelTest(TestCase):
    def setUp(self):
        # Create a CrontabSchedule for testing
        self.schedule = CrontabSchedule.objects.create(
            minute='0',
            hour='0',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
        )

    def test_osm_task_status(self):
        osm_task = OSMTask.objects.create(region="Test Region", schedule=self.schedule)
        self.assertEqual(osm_task.status, "NEVER RUN")

        # Create a running result
        running_result = OSMTaskResult.objects.create(task=osm_task)
        self.assertEqual(osm_task.status, "RUNNING")

        # Complete the running result with no errors
        running_result.finish_date = datetime.datetime.now()
        running_result.save()
        self.assertEqual(osm_task.status, "DONE")

        # Create a result with errors
        error_result = OSMTaskResult.objects.create(task=osm_task)
        OSMError.objects.create(task_result=error_result, data="Error data", type="Error type")
        self.assertEqual(osm_task.status, "DONE_WITH_ERRORS")


class OSMTaskResultModelTest(TestCase):
    def test_osm_task_result_errors(self):
        osm_task = OSMTask.objects.create(region="Test Region", schedule=CrontabSchedule.objects.create())
        osm_task_result = OSMTaskResult.objects.create(task=osm_task)

        # Test errors property
        self.assertEqual(osm_task_result.errors, 0)

        # Add an error and test errors property again
        OSMError.objects.create(task_result=osm_task_result, data="Error data", type="Error type")
        self.assertEqual(osm_task_result.errors, 1)

    def test_osm_task_result_update_progress(self):
        osm_task = OSMTask.objects.create(region="Test Region", schedule=CrontabSchedule.objects.create())
        osm_task_result = OSMTaskResult.objects.create(task=osm_task, items_collected=10)

        # Test initial items_collected value
        self.assertEqual(osm_task_result.items_collected, 10)

        # Update progress and test items_collected value
        osm_task_result.update_progress(5)
        self.assertEqual(osm_task_result.items_collected, 15)

    def test_osm_task_result_mark_as_done(self):
        osm_task = OSMTask.objects.create(region="Test Region", schedule=CrontabSchedule.objects.create())
        osm_task_result = OSMTaskResult.objects.create(task=osm_task)

        # Test initial finish_date value
        self.assertIsNone(osm_task_result.finish_date)

        # Mark as done and test finish_date value
        osm_task_result.mark_as_done()
        self.assertIsNotNone(osm_task_result.finish_date)

class OSMErrorModelTest(TestCase):
    def test_osm_error_creation(self):
        osm_task = OSMTask.objects.create(region="Test Region", schedule=CrontabSchedule.objects.create())
        osm_task_result = OSMTaskResult.objects.create(task=osm_task)

        # Test error creation
        error = OSMError.objects.create(task_result=osm_task_result, data="Error data", type="Error type")
        self.assertEqual(error.task_result, osm_task_result)
        self.assertEqual(error.data, "Error data")
        self.assertEqual(error.type, "Error type")


class OSMTaskSignalTest(TestCase):
    def setUp(self):
        PeriodicTask.objects.all().delete()

    def test_add_periodic_task_signal(self):
        osm_task = OSMTask.objects.create(region="Test Region", schedule=CrontabSchedule.objects.create())

        # Check if the periodic task is created when the OSMTask is saved
        periodic_task = PeriodicTask.objects.get(name=osm_task.region)
        self.assertEqual(periodic_task.args, json.dumps([osm_task.id]))

    def test_add_periodic_task_signal_existing_task(self):
        osm_task = OSMTask.objects.create(region="Test Region", schedule=CrontabSchedule.objects.create())
        periodic_task = PeriodicTask.objects.get(name="Test Region")

        osm_task.schedule.minute = '30'
        osm_task.schedule.save()
        osm_task.save()
        periodic_task.refresh_from_db()
        self.assertEqual(periodic_task.args, json.dumps([osm_task.id]))

    def test_add_periodic_task_signal_task_not_found(self):
        # Check if the signal handles the case when the periodic task is not found
        osm_task = OSMTask.objects.create(region="Test Region", schedule=CrontabSchedule.objects.create())
        PeriodicTask.objects.filter(name=osm_task.region).delete()
        osm_task.save()
        self.assertTrue(PeriodicTask.objects.filter(name=osm_task.region).exists())
