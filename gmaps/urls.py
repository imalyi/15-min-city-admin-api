from django.urls import path
from gmaps.views import CredentialView, PlaceTypeView, CoordinatesView, TaskTemplateView, TaskActionView
from rest_framework import routers


router = routers.SimpleRouter()
router.register('task', TaskActionView)

urlpatterns = [
    path('credential/', CredentialView.as_view()),
    path('coordinates/', CoordinatesView.as_view()),
    path('template/', TaskTemplateView.as_view(), name='template'),
    path('place/', PlaceTypeView.as_view()),
] + router.urls
