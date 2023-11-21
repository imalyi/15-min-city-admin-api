from django.urls import path
from gmaps.views import CredentialView, PlaceTypeView, CoordinatesView, TaskView, ScheduleView, TaskResultView
from rest_framework import routers


router = routers.SimpleRouter()
router.register('credential', CredentialView, basename='credential')
router.register('place', PlaceTypeView, basename='place'),
router.register('task', TaskView, basename='task')
router.register('schedule', ScheduleView, basename='schedule')


urlpatterns = [
    path('coordinates/', CoordinatesView.as_view()),
    path('result/<int:task_id>', TaskResultView.as_view()),
] + router.urls
