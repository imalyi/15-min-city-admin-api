from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED


class TestTaskStatus(APITestCase):
    def test_list_status(self):
        response = self.client.get(reverse('status'))
        self.assertEquals(response.status_code, HTTP_200_OK)