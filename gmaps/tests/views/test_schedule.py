from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from gmaps.models import CrontabSchedule
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class TestPlaceType(APITestCase):
    def setUp(self):
        self.schedule = CrontabSchedule.objects.create(minute="1", hour="2")
        self.admin = User.objects.create_superuser('admin', 'admin')
        self.access_token = "Bearer " + str(RefreshToken.for_user(self.admin).access_token)

    def test_list_schedule_authorised(self):
        response = self.client.get(reverse("schedule-list"), HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)

    def test_list_schedule_unauthorised(self):
        url = reverse('schedule-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, HTTP_401_UNAUTHORIZED)
