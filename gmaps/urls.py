from django.urls import path
from gmaps.views import CredentialView, PlaceTypeView, CoordinatesView, TaskTemplateView, TaskActionView
from rest_framework import routers


router = routers.SimpleRouter()
router.register('task', TaskActionView)
router.register('credential', CredentialView, basename='credential')
router.register('place', PlaceTypeView, basename='place'),
router.register('template', TaskTemplateView, basename='template')

urlpatterns = [
    path('coordinates/', CoordinatesView.as_view()),
] + router.urls
