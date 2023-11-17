from gmaps.models import Credential
from django.test import TestCase


class TestCredentials(TestCase):
    def setUp(self):
        self.token_name = "test_name"
        self.secret_token = "secret_token"
        self.credentials = Credential.objects.create(name=self.token_name, token=self.secret_token)

    def test_str_method(self):
        self.assertEquals(str(self.credentials), self.token_name)

    def test_repr_method(self):
        self.assertEquals(repr(self.credentials), self.token_name)
