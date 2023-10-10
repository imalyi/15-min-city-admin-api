from django.test import TestCase
from django.contrib.auth import get_user_model


class UserAccountTests(TestCase):
    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser('igor', 'test')
        self.assertEquals(super_user.username, 'igor')
        self.assertEquals(super_user.is_superuser, True)

        with self.assertRaises(ValueError):
            super_user = db.objects.create_superuser('', 'test')
