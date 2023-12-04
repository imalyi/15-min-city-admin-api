import json
import unittest
from datetime import datetime
from django.test import TestCase
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from openstreetmaps.models import OSMTask, OSMTaskResult, OSMError, add_periodic_task


class OSMTaskModelTest(TestCase):

    def setUp(self):
        # Create a CrontabSchedule for testing
        self.schedule = CrontabSchedule.objects.create(
            minute="0",
            hour="0",
            day_of_month="1",
            month_of_year="*",
            day_of_week="*",
        )


    @unittest.skip("bad test")
    def test_osm_task_status(self):
        #TODO fix this test
        # Create an OSMTask with a related CrontabSchedule
        osm_task = OSMTask.objects.create(region="Test Region", schedule=self.schedule)

        # Test the status property
        self.assertEqual(osm_task.status, "NEVER RUN")

        # Create an OSMTaskResult related to the OSMTask
        osm_task_result = OSMTaskResult.objects.create(task=osm_task)

        # Update progress and mark as done
        osm_task_result.update_progress(50)
        osm_task_result.mark_as_done()

        # Test the status property again
        self.assertEqual(osm_task.status, "DONE")

    def test_osm_task_result_methods(self):
        osm_task = OSMTask.objects.create(region="Test Region", schedule=self.schedule)
        osm_task_result = OSMTaskResult.objects.create(task=osm_task)

        # Test update_progress method
        osm_task_result.update_progress(25)
        self.assertEqual(osm_task_result.items_collected, 25)

        # Test add_error method
        osm_task_result.add_error(data="Test Error", type="Sample Type")
        self.assertEqual(osm_task_result.errors.count(), 1)

        # Test mark_as_done method
        osm_task_result.mark_as_done()
        self.assertIsNotNone(osm_task_result.finish_date)


class OSMErrorModelTest(TestCase):

    def test_osm_error_model(self):
        osm_task = OSMTask.objects.create(region="Test Region", schedule=CrontabSchedule.objects.create())
        osm_task_result = OSMTaskResult.objects.create(task=osm_task)

        # Test OSMError model
        osm_error = OSMError.objects.create(task_result=osm_task_result, data="Error Data", type="Error Type")

        self.assertEqual(osm_error.task_result, osm_task_result)
        self.assertEqual(osm_error.data, "Error Data")
        self.assertEqual(osm_error.type, "Error Type")


class SignalTest(TestCase):

    def test_add_periodic_task_signal(self):
        osm_task = OSMTask.objects.create(region="Test Region", schedule=CrontabSchedule.objects.create())

        # Call the signal directly to simulate post_save
        add_periodic_task(sender=OSMTask, instance=osm_task)

        # Check if PeriodicTask has been created
        periodic_task = PeriodicTask.objects.get(name=osm_task.region)
        self.assertIsNotNone(periodic_task)
        self.assertEqual(json.loads(periodic_task.args), [osm_task.id])
