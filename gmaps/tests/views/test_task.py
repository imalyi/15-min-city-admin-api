from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from gmaps.models import Task, TaskTemplate
from gmaps.serializers import PlaceTypeSerializer
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class TestTask(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin')
        self.access_token = "Bearer " + str(RefreshToken.for_user(self.admin).access_token)

    def test_get(self):
        pass