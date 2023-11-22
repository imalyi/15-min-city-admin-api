import re

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

from gmaps.models import PlaceType, Category, Task, Credential, Coordinate, CrontabSchedule, PeriodicTask
from gmaps.serializers import TaskSerializer
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch


class TestTask(APITestCase):
    def setUp(self):
        self.credential = Credential.objects.create(name="token_name", token="secret")
        self.coordinates = Coordinate.objects.create(lon=12, lat=13, radius=142)
        self.category = Category.objects.create(value="category")
        self.place = PlaceType.objects.create(value="place", category=self.category)
        self.schedule = CrontabSchedule.objects.create()
        self.task = Task.objects.create(credentials=self.credential, coordinates=self.coordinates, place=self.place, schedule=self.schedule)
        self.admin = User.objects.create_superuser('admin', 'admin')
        self.access_token = "Bearer " + str(RefreshToken.for_user(self.admin).access_token)

    def test_list_tasks_authorised(self):
        response = self.client.get(reverse("task-list"), HTTP_AUTHORIZATION=self.access_token)
        self.assertEqual(response.status_code, HTTP_200_OK)
        serialized_task_data = TaskSerializer([self.task], many=True).data
        self.assertEqual(response.data, serialized_task_data)

    def test_create_tasks_authorised(self):
        new_credentials = Credential.objects.create(name="new_name", token="new_secret")
        new_place = PlaceType.objects.create(value="new_place")
        data = {
            "credentials": new_credentials.id,
            "place": new_place.id,
            "schedule": self.schedule.id,
            "coordinates": self.coordinates.id
        }
        response = self.client.post(reverse("task-list"), data=data, HTTP_AUTHORIZATION=self.access_token)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_retrieve_task_authorised(self):
        response = self.client.get(reverse("task-detail", str(self.task.id)), HTTP_AUTHORIZATION=self.access_token)
        self.assertEqual(response.status_code, HTTP_200_OK)
        serialized_task_data = TaskSerializer(self.task).data
        self.assertEqual(response.data, serialized_task_data)

    @patch('google_maps_parser_api.celery.send_task_to_collector.delay')
    def test_start_task_authorised(self, mock_send_task):
        response = self.client.get(reverse("task-start", str(self.task.id)), HTTP_AUTHORIZATION=self.access_token)
        mock_send_task.assert_called_once_with(self.task.id, self.credential.token, self.place.value, [self.coordinates.lat, self.coordinates.lon], self.coordinates.radius)
        self.assertEquals(response.status_code, HTTP_200_OK)

    def test_update_task_authorised(self):
        pass

    def test_delete_task_authorised(self):
        response = self.client.delete(reverse("task-detail", str(self.task.id)), HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_204_NO_CONTENT)
        response = self.client.delete(reverse("task-detail", str(self.task.id)), HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_404_NOT_FOUND)
