from django.db.models import CharField, DateTimeField, BooleanField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)

        if not username:
            raise ValueError(f"Username cant be {username}")
        user = self.model(username=username, is_superuser=True, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = CharField(max_length=150, unique=True)
    start_date = DateTimeField(auto_now=True, blank=True)
    is_staff = BooleanField(default=True)
    is_active = BooleanField(default=True)

    USERNAME_FIELD = 'username'
    objects = CustomAccountManager()

    def __str__(self):
        return self.username

    def __repr__(self):
        return self.username
