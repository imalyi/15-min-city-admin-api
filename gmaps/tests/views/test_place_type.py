from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from gmaps.models import PlaceType
from gmaps.serializers import PlaceTypeSerializer
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class TestPlaceType(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin')
        self.access_token = "Bearer " + str(RefreshToken.for_user(self.admin).access_token)
        self.place = PlaceType.objects.create(value="test_place")

    def test_get_authorised(self):
        response = self.client.get(reverse('place-list'), HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)
        serialized_data = PlaceTypeSerializer(self.place).data
        self.assertEquals(response.data, [serialized_data])

    def test_post_authorised(self):
        value = 'test2'
        response = self.client.post(reverse('place-list'), data={'value': value}, HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_201_CREATED)
        self.assertEquals(PlaceType.objects.get(value=value).value, value)

    def test_retrieve_credential_authorised(self):
        response = self.client.get(reverse('place-detail', str(self.place.id)), HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)
        serialized_data = PlaceTypeSerializer(self.place).data
        self.assertEquals(response.data, serialized_data)

    def test_update_credential_authorised(self):
        url = reverse('place-detail', str(self.place.id))
        response = self.client.put(url, data={'value': 'new'}, HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)

    def test_get_unauthorised(self):
        url = reverse('place-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, HTTP_401_UNAUTHORIZED)
