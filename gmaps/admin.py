from gmaps.models import Coordinate, Credential, TaskTemplate, PlaceType, TaskResult, Category
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin


@admin.register(Coordinate)
class CoordinateAdmin(admin.ModelAdmin):
    list_display = ('name', 'lon', 'lat')


@admin.register(TaskTemplate)
class TaskTemplateAdmin(admin.ModelAdmin):
    list_display = ('place', 'coordinates', 'credentials')


@admin.register(PlaceType)
class PlaceTypeAdmin(admin.ModelAdmin):
    list_display = ("category", )


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(TaskResult)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('template', 'status', 'start', 'finish', 'items_collected')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass