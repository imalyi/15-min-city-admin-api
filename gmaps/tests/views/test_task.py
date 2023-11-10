from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from gmaps.models import Task
from gmaps.serializers import TaskSerializer
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from gmaps.tests.views.test_task_template import create_task_template


class TestTask(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin')
        self.access_token = "Bearer " + str(RefreshToken.for_user(self.admin).access_token)
        self.task = Task.objects.create(template=create_task_template("place", "secret", "secret_name", "every day", "city", 12, 13))

    def test_get(self):
        response = self.client.get(reverse('task-list'), HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)
        serialized_data = TaskSerializer(self.task).data
        self.assertEquals(response.data, [serialized_data])