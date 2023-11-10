from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from gmaps.models import TaskTemplate, Schedule, Credential, PlaceType, Coordinate
from gmaps.serializers import TaskTemplateSerializer
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class TestTaskTemplate(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin')
        self.access_token = "Bearer " + str(RefreshToken.for_user(self.admin).access_token)
        self.template = self.__create_task_template("place", "secret", "secret_name", "every day", "city", 12, 13)

    def __create_task_template(self, place_value, token, token_name, schedule_name, coordinates_name, lon, lat):
        place = PlaceType.objects.create(value=place_value)
        credentials = Credential.objects.create(name=token_name, token=token)
        schedule = Schedule.objects.create(name=schedule_name)
        coordinates = Coordinate.objects.create(name=coordinates_name, lon=lon, lat=lat)
        task_template = TaskTemplate.objects.create(place=place, credentials=credentials, schedule=schedule, coordinates=coordinates)
        return task_template

    def test_get(self):
        response = self.client.get(reverse('template-list'),
                                   HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)
        serialized_data = TaskTemplateSerializer(self.template).data
        self.assertEquals(response.data, [serialized_data])
