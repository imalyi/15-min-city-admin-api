from django.urls import path
from gmaps.views import CredentialView, PlaceTypeView, CoordinatesView, TaskView, TaskResult, ScheduleView
from rest_framework import routers


router = routers.SimpleRouter()
router.register('credential', CredentialView, basename='credential')
router.register('place', PlaceTypeView, basename='place'),
router.register('task', TaskView, basename='task')
router.register('schedule', ScheduleView, basename='schedule')


urlpatterns = [
    path('coordinates/', CoordinatesView.as_view()),
    path('result/', TaskResult.as_view(), name='result')
] + router.urls
