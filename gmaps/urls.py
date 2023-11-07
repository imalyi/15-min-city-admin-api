from django.urls import path
from gmaps.views import CredentialView, PlaceTypeView, CoordinatesView, SubTaskView, TaskView, SubTaskActionView, TaskActionView
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'subtask', SubTaskActionView)
router.register('task', TaskActionView)

urlpatterns = [
    path('credential/', CredentialView.as_view()),
    path('coordinates/', CoordinatesView.as_view()),
    path('subtask/', SubTaskView.as_view(), name='subtask'),
    path('task/', TaskView.as_view()),
    path('place/', PlaceTypeView.as_view()),
] + router.urls
