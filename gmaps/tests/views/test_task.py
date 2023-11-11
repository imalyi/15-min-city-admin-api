from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from gmaps.models import Task, TaskTemplate, Coordinate, PlaceType, Credential
from gmaps.serializers import TaskSerializer
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from gmaps.tests.views.test_task_template import create_task_template
from gmaps.models import POSSIBLE_STATUSES
from status.TASK_STATUSES import ERROR, DONE, CANCELED, STOPPED, RUNNING, SENT, WAITING


class TestTask(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin')
        self.access_token = "Bearer " + str(RefreshToken.for_user(self.admin).access_token)
        self.task = Task.objects.create(template=create_task_template("place", "secret", "secret_name", "every day", "city", 12, 13))

    def test_list_task_authorised(self):
        response = self.client.get(reverse('task-list'), HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)
        serialized_data = TaskSerializer(self.task).data
        self.assertEquals(response.data, [serialized_data])

    def test_create_task_authorised(self):
        Task.objects.all().delete()
        template = create_task_template("place1", "secret", "secret_name", "every day", "city1", 12, 13)

        data = {"template": template.id,
                "status": "waiting",
                }
        response = self.client.post(reverse('task-list'), data=data, HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_201_CREATED)
        self.assertIsInstance(Task.objects.get(template_id=template.id), Task)

    def test_retrieve_task_authorised(self):
        response = self.client.get(reverse('task-detail', str(self.task.id)), HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)
        serialized_data = TaskSerializer(self.task).data
        self.assertEquals(response.data, serialized_data)

    def test_list_task_unauthorised(self):
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_change_to_correct_status(self):
        TaskTemplate.objects.all().delete()
        Coordinate.objects.all().delete()
        Credential.objects.all().delete()
        PlaceType.objects.all().delete()
        template = create_task_template("place4", "secret", "secret_name", "every day", "city", 12, 13)
        Task.objects.all().delete()

        for status in [[RUNNING, ERROR], [RUNNING, DONE], [RUNNING, STOPPED], [WAITING, CANCELED], [SENT, RUNNING], [SENT, CANCELED], [ERROR, WAITING]]:
            # [[from, to], ...]

            current_status = status[0]
            next_status = status[1]
            url_task_create = reverse("task-list")
            data = {"template": template.id,
                    "status": current_status,
                    }
            task = self.client.post(url_task_create, data).data.get('id')
            url = reverse("task-detail", str(task)) + next_status
            response = self.client.get(url, HTTP_AUTHORIZATION=self.access_token)
            print(f"Changing status from {current_status} to {next_status}. Code: {response.status_code}. Url {url}")
#            self.assertEquals(response.status_code, HTTP_200_OK, )
