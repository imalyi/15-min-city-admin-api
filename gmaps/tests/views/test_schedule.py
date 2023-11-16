from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from users.models import User
from gmaps.serializers import ScheduleSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class TestSchedule(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin')
        self.access_token = "Bearer " + str(RefreshToken.for_user(self.admin).access_token)
        self.schedule = Schedule.objects.create(name="test_schedule1")

    def test_list_schedule_authorised(self):
        response = self.client.get(reverse('schedule-list'), HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)
        serialized_data = ScheduleSerializer(self.schedule).data
        self.assertEquals(response.data, [serialized_data])

    def test_create_schedule_authorised(self):
        Schedule.objects.all().delete()
        response = self.client.post(reverse("schedule-list"), data={'name': 'test'}, HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_201_CREATED)
        self.assertIsInstance(Schedule.objects.get(name='test'), Schedule)

    def test_retrieve_schedule_authorised(self):
        response = self.client.get(reverse('schedule-detail', str(self.schedule.id)), HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)
        serialized_data = ScheduleSerializer(self.schedule).data
        self.assertEquals(response.data, serialized_data)

    def test_list_schedule_unauthorised(self):
        url = reverse('schedule-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_update_task_template_authorised(self):
        url = reverse('schedule-detail', str(self.schedule.id))
        data = {
            "name": "new_name",
            "day_of_month": "*",
            "minute": "*",
            "hour": "*"
        }
        response = self.client.put(url, data=data, HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)

        response = self.client.get(reverse('schedule-detail', str(self.schedule.id)),
                                   HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)
        serialized_data = ScheduleSerializer(response.data).data
        self.assertEquals(serialized_data, response.data)
