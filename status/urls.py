from django.urls import path
from status.views import task_statuses
urlpatterns = [
    path('task/', task_statuses, name='status'),
]
