from gmaps.models import SubTask, PlaceType, Coordinate
from gmaps.models import WAITING, CANCELED, RUNNING, DONE, ERROR
from django.test import TestCase


class TestSubtaksModel(TestCase):
    def setUp(self):
        self.place = PlaceType.objects.create(value="test_place")
        self.coordinates = Coordinate.objects.create(name="test_coords", lat=12.1, lon=24.1)

        self.subtask = SubTask.objects.create(
            place=self.place,
            coordinates=self.coordinates,
            status=WAITING,
        )
        self.subtask.save()

    def test_model_str(self):
        self.assertEquals(str(self.subtask), f"{self.place}-{str(self.subtask.created)}")


class TestAction(TestCase):
    def setUp(self):
        self.place = PlaceType.objects.create(value="test_place")
        self.coordinates = Coordinate.objects.create(name="test_coords", lat=12.1, lon=24.1)
        self.subtask = SubTask.objects.create(place=self.place, coordinates=self.coordinates, status=WAITING)

    def test_status_change_methods(self):
        test_cases = [
            {
                'method': SubTask.change_status_to_error,
                'invalid_status_list': [WAITING, DONE, ERROR, CANCELED],
                'valid_status_list': [RUNNING],
                'new_status': ERROR,
            },
            {
                'method': SubTask.change_status_to_done,
                'invalid_status_list': [ERROR, CANCELED, WAITING],
                'valid_status_list': [RUNNING],
                'new_status': DONE,
            },
            {
                'method': SubTask.start_if_waiting,
                'invalid_status_list': [ERROR, RUNNING, CANCELED, DONE],
                'valid_status_list': [WAITING],
                'new_status': RUNNING,
            },
            {
                'method': SubTask.cancel_if_waiting,
                'invalid_status_list': [ERROR, RUNNING, CANCELED, DONE],
                'valid_status_list': [WAITING],
                'new_status': CANCELED,
            },
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                for invalid_status in test_case['invalid_status_list']:
                    with self.subTest(status=invalid_status):
                        self.subtask.status = invalid_status
                        self.subtask.save()
                        with self.assertRaises(SubTask.InvalidStatusChange):
                            test_case['method'](self.subtask)

                for valid_status in test_case['valid_status_list']:
                    with self.subTest(status=valid_status):
                        self.subtask.status = valid_status
                        self.subtask.save()
                        test_case['method'](self.subtask)
                        self.assertEqual(self.subtask.status, test_case['new_status'])

    def test_update_progress(self):

        with self.assertRaises(self.subtask.InvalidStatusForProgressTrack):
            self.subtask.update_progress(15)


        with self.assertRaises(self.subtask.InvalidProgressValue):
            self.subtask.update_progress('14f')

        self.subtask.status = RUNNING
        self.subtask.save()
        self.subtask.update_progress(15)
        self.assertEquals(self.subtask.items_collected, 15)
