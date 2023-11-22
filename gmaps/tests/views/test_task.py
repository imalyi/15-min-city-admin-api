from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from gmaps.models import PlaceType
from gmaps.serializers import CategoryPlaceSerializer
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class TestTask(APITestCase):
    def setUp(self):
        pass

    def test_list_tasks_authorised(self):
        pass

    def test_create_tasks_authorised(self):
        pass

    def test_retrieve_task_authorised(self):
        pass

    def test_start_task_authorised(self):
        pass

    def test_update_task_authorised(self):
        pass

    def test_delete_task_authorised(self):
        pass
