from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from gmaps.models import PlaceType, Category
from gmaps.serializers import CategoryPlaceSerializer
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class TestPlaceType(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(value="test_cat")
        self.place = PlaceType.objects.create(value="test_place", category=self.category)
        self.admin = User.objects.create_superuser('admin', 'admin')
        self.access_token = "Bearer " + str(RefreshToken.for_user(self.admin).access_token)

    def test_list_place_type_authorised(self):
        response = self.client.get(reverse("place-list"), HTTP_AUTHORIZATION=self.access_token)
        self.assertEquals(response.status_code, HTTP_200_OK)
        self.assertIn("category_name", response.data[0])
        self.assertIn("places", response.data[0])

    def test_list_place_type_unauthorised(self):
        url = reverse('place-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, HTTP_401_UNAUTHORIZED)
