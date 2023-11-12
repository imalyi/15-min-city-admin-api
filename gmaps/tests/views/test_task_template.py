from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from gmaps.models import TaskTemplate, Schedule, Credential, PlaceType, Coordinate
from gmaps.serializers import TaskTemplateSerializer
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


def create_task_template(place_value, token, token_name, schedule_name, coordinates_name, lon, lat):
    place = PlaceType.objects.create(value=place_value)
    credentials = Credential.objects.create(name=token_name, token=token)
    schedule = Schedule.objects.create(name=schedule_name)
    coordinates = Coordinate.objects.create(name=coordinates_name, lon=lon, lat=lat)
    task_template = TaskTemplate.objects.create(place=place, credentials=credentials, schedule=schedule,
                                                coordinates=coordinates)
    return task_template


class TestTaskTemplate(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin')
        self.access_token = "Bearer " + str(RefreshToken.for_user(self.admin).access_token)
        self.template = create_task_template("place", "secret", "secret_name", "every day", "city", 12, 13)

    def test_list_task_template_authorised(self):
        response = self.client.get(reverse('template-list'),
                                   HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)
        serialized_data = TaskTemplateSerializer(self.template).data
        self.assertEquals(response.data, [serialized_data])

    def test_create_task_template_authorised(self):
        TaskTemplate.objects.all().delete()
        data = {"place": 1,
                "credentials": 1,
                "coordinates": 1,
                "schedule": 1
                }
        response = self.client.post(reverse('template-list'), data=data, HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_201_CREATED)
        self.assertIsInstance(TaskTemplate.objects.get(place=1), TaskTemplate)

    def test_retrieve_task_template_authorised(self):
        response = self.client.get(reverse('template-detail', str(self.template.id)), HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)
        serialized_data = TaskTemplateSerializer(self.template).data
        self.assertEquals(response.data, serialized_data)

    def test_update_task_template_authorised(self):
        url = reverse('template-detail', str(self.template.id))
        new_place = PlaceType.objects.create(value="new1")
        data = {"place": new_place.id,
                "credentials": 1,
                "coordinates": 1,
                "schedule": 1
                }
        response = self.client.put(url, data=data, HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)

    def test_list_task_template_unauthorised(self):
        url = reverse('template-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, HTTP_401_UNAUTHORIZED)
