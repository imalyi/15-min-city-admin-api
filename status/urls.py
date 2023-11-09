from django.urls import path
from status.views import subtask_statuses, task_statuses
urlpatterns = [
    path('subtask/', subtask_statuses),
    path('task/', task_statuses),
]
