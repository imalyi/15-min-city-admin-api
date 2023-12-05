from django.test import TestCase
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from openstreetmaps.models import OSMTask, OSMTaskResult, OSMError
from django.utils import timezone
import json

class OSMTaskModelTests(TestCase):
    def setUp(self):
        self.schedule = CrontabSchedule.objects.create(
            minute="0",
            hour="0",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*"
        )

        self.osm_task = OSMTask.objects.create(
            region="TestRegion",
            schedule=self.schedule
        )

    def test_osm_task_status_never_run(self):
        self.assertEqual(self.osm_task.status, "NEVER RUN")

    def test_osm_task_status_running(self):
        osm_task_result = OSMTaskResult.objects.create(
            task=self.osm_task
        )
        self.assertEqual(self.osm_task.status, "RUNNING")

    def test_osm_task_status_done(self):
        osm_task_result = OSMTaskResult.objects.create(
            task=self.osm_task,
            addresses_items_collected=10,
            amenity_items_collected=5,
            finish_date=timezone.now()
        )
        self.assertEqual(self.osm_task.status, "DONE")

    def test_osm_task_status_done_with_errors(self):
        osm_task_result = OSMTaskResult.objects.create(
            task=self.osm_task,
            finish_date=timezone.now()
        )
        OSMError.objects.create(task_result=osm_task_result, data="test", type="test")
        self.assertEqual(self.osm_task.status, "DONE_WITH_ERRORS")


class OSMTaskResultModelTests(TestCase):

    def setUp(self):
        self.schedule = CrontabSchedule.objects.create(
            minute="0",
            hour="0",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*"
        )

        self.osm_task = OSMTask.objects.create(
            region="TestRegion",
            schedule=self.schedule
        )

    def test_update_address_progress(self):
        osm_task_result = OSMTaskResult.objects.create(
            task=self.osm_task
        )
        osm_task_result.update_address_progress(5)
        self.assertEqual(osm_task_result.addresses_items_collected, 5)

    def test_update_amenity_progress(self):
        osm_task_result = OSMTaskResult.objects.create(
            task=self.osm_task
        )
        osm_task_result.update_amenity_progress(3)
        self.assertEqual(osm_task_result.amenity_items_collected, 3)

    def test_add_error(self):
        osm_task_result = OSMTaskResult.objects.create(
            task=self.osm_task
        )
        osm_task_result.add_error(data="Error data", type="Error type")
        self.assertEqual(osm_task_result.errors.count(), 1)

    def test_mark_as_done(self):
        osm_task_result = OSMTaskResult.objects.create(
            task=self.osm_task
        )
        osm_task_result.mark_as_done()
        self.assertIsNotNone(osm_task_result.finish_date)


class OSMErrorModelTests(TestCase):

    def setUp(self):
        self.schedule = CrontabSchedule.objects.create(
            minute="0",
            hour="0",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*"
        )

        self.osm_task = OSMTask.objects.create(
            region="TestRegion",
            schedule=self.schedule
        )

        self.osm_task_result = OSMTaskResult.objects.create(
            task=self.osm_task
        )

    def test_osm_error_creation(self):
        OSMError.objects.create(
            task_result=self.osm_task_result,
            data="Error data",
            type="Error type"
        )
        self.assertEqual(self.osm_task_result.errors.count(), 1)


class OSMTaskSignalTests(TestCase):

    def setUp(self):
        self.schedule = CrontabSchedule.objects.create(
            minute="0",
            hour="0",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*"
        )

        self.osm_task = OSMTask.objects.create(
            region="TestRegion",
            schedule=self.schedule
        )

    def test_add_periodic_task_existing(self):

        self.assertEqual(PeriodicTask.objects.filter(name=self.osm_task.region).count(), 1)

        # Trigger the signal
        self.osm_task.save()

        # Ensure the PeriodicTask is updated
        periodic_task = PeriodicTask.objects.get(name=self.osm_task.region)
        self.assertEqual(periodic_task.args, json.dumps([self.osm_task.id]))

    def test_add_periodic_task_non_existing(self):
        PeriodicTask.objects.all().delete()
        self.assertEqual(PeriodicTask.objects.filter(name=self.osm_task.region).count(), 0)
        self.osm_task.save()

        # Ensure a new PeriodicTask is created
        self.assertEqual(PeriodicTask.objects.filter(name=self.osm_task.region).count(), 1)
