from gmaps.models import Coordinate, Credential, SubTask, Task, PlaceType
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin


class CoordinateConfig(admin.ModelAdmin):
    list_display = ('name', 'lon', 'lat')


class SubTaskConfig(admin.ModelAdmin):
    list_display = ('place', 'coordinates', 'status', 'start', 'finish', 'created', 'items_collected')


class TaskConfig(admin.ModelAdmin):
    list_display = ('name', 'date', 'credentials', 'subtask_count', 'items_collected')


admin.site.register(Coordinate, CoordinateConfig)
admin.site.register(SubTask, SubTaskConfig)
admin.site.register(Task, TaskConfig)
admin.site.register(PlaceType)
admin.site.register(Credential)
