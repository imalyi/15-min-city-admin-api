from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from gmaps.models import PlaceType
from gmaps.serializers import CategoryPlaceSerializer
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class TestTaskResult(APITestCase):
    def setUp(self):
        pass

    def test_list_task_results_authorised(self):
        pass
