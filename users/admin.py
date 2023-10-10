from django.contrib import admin
from django.apps import apps

from users.models import NewUser
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    list_display = ('username','last_login')


admin.site.register(NewUser, UserAdminConfig)
