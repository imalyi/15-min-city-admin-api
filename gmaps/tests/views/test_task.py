from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from gmaps.models import TaskResult, TaskTemplate, Coordinate, PlaceType, Credential
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
        self.task = TaskResult.objects.create(template=create_task_template("place", "secret", "secret_name", "every day", "city", 12, 13))

    def test_list_task_authorised(self):
        response = self.client.get(reverse('task-list'), HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)
        serialized_data = TaskSerializer(self.task).data
        self.assertEquals(response.data, [serialized_data])

    def test_create_task_authorised(self):
        TaskResult.objects.all().delete()
        template = create_task_template("place1", "secret", "secret_name", "every day", "city1", 12, 13)

        data = {"template": template.id,
                "status": "waiting",
                }
        response = self.client.post(reverse('task-list'), data=data, HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_201_CREATED)
        self.assertIsInstance(TaskResult.objects.get(template_id=template.id), TaskResult)

    def test_retrieve_task_authorised(self):
        response = self.client.get(reverse('task-detail', str(self.task.id)), HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)
        serialized_data = TaskSerializer(self.task).data
        self.assertEquals(response.data, serialized_data)

    def test_list_task_unauthorised(self):
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, HTTP_401_UNAUTHORIZED)

    def __change_status(self, from_, to, status_code: list):
        STATUS_URL = {
            STOPPED: 'stop',
            CANCELED: 'cancel',
        }
        TaskTemplate.objects.all().delete()
        Coordinate.objects.all().delete()
        Credential.objects.all().delete()
        PlaceType.objects.all().delete()
        template = create_task_template("place4", "secret", "secret_name", "every day", "city", 12, 13)
        TaskResult.objects.all().delete()

        task = TaskResult.objects.create(template=template, status=from_)
        url = reverse("task-detail", args=[str(task.id)]) + STATUS_URL.get(to, to) + '/'
        response = self.client.get(url, HTTP_AUTHORIZATION=self.access_token)
        print(f"Changing status from {task.status} to {to}. Code: {response.status_code}. Url {url}")
        self.assertEquals(response.status_code in status_code, True)

    def _generate_correct_and_incorrect_statuses(self):
        """Only for statuses that can be changed from view"""
        correct_statuses = [[RUNNING, ERROR], [RUNNING, DONE], [RUNNING, STOPPED], [WAITING, CANCELED], [SENT, RUNNING], [SENT, CANCELED]]
        incorrect_statuses = []
        status_list = [RUNNING, ERROR, DONE, STOPPED, WAITING, CANCELED, SENT]
        for from_ in status_list:
            for to in status_list:
                if [from_, to] not in correct_statuses:
                    incorrect_statuses.append([from_, to])
        return correct_statuses, incorrect_statuses

    def test_change_to_incorrect_status_authorised(self):
        correct_statuses, incorrect_statuses = self._generate_correct_and_incorrect_statuses()
        for incorrect_from, incorrect_to in incorrect_statuses:
            self.__change_status(incorrect_from, incorrect_to, [HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST])

    def test_change_to_correct_status_authorised(self):
        correct_statuses, incorrect_statuses = self._generate_correct_and_incorrect_statuses()
        for correct_from, correct_to in correct_statuses:
            self.__change_status(correct_from, correct_to, [HTTP_200_OK])

    def test_task_update_progress_authorised(self):
        TaskResult.objects.all().delete()
        TaskTemplate.objects.all().delete()
        Coordinate.objects.all().delete()
        Credential.objects.all().delete()
        PlaceType.objects.all().delete()
        template = create_task_template("place4", "secret", "secret_name", "every day", "city", 12, 13)
        task = TaskResult.objects.create(template=template, status=RUNNING)
        url = reverse('task-detail', str(task.id)) + 'track/'
        response = self.client.post(url, data={'progress': 124}, HTTP_AUTHORIZATION=self.access_token)
        updated_task = TaskResult.objects.get(id=task.id)
        self.assertEquals(response.status_code, HTTP_200_OK)
        self.assertEquals(updated_task.items_collected, 124)
