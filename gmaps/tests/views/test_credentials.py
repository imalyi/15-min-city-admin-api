from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from gmaps.models import Credential
from gmaps.serializers import CredentialSerializer
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class TestCredential(APITestCase):
    def setUp(self):
        self.name = "test"
        self.token = "secret"
        self.admin = User.objects.create_superuser('admin', 'admin')
        self.access_token = "Bearer " + str(RefreshToken.for_user(self.admin).access_token)
        self.credential = Credential.objects.create(name=self.name, token=self.token)

    def test_list_credential_authorised(self):
        response = self.client.get(reverse('credential-list'), HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)
        serialized_data = CredentialSerializer(self.credential).data
        self.assertEquals(response.data, [serialized_data])

    def test_create_credential_authorised(self):
        name = 'test1'
        token = 'token2'
        response = self.client.post(reverse('credential-list'), data={'name': name, 'token': token}, HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_201_CREATED)
        self.assertEquals(Credential.objects.get(name=name).name, name)

    def test_retrieve_credential_authorised(self):
        response = self.client.get(reverse('credential-detail', str(self.credential.id)), HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)
        serialized_data = CredentialSerializer(self.credential).data
        self.assertEquals(response.data, serialized_data)

    def test_update_credential_authorised(self):
        url = reverse('credential-detail', str(self.credential.id))
        response = self.client.put(url, data={'name': 'new_name', 'token': "new_token"}, HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)

    def test_list_credential_unauthorised(self):
        url = reverse('credential-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, HTTP_401_UNAUTHORIZED)
