from django.contrib import admin
from django.urls import path

from gmaps.views import CredentialView, PlaceTypeView, StatusView, CoordinatesView, SubTaskView, TaskView

urlpatterns = [
    path('credential/', CredentialView.as_view()),
    path('status/', StatusView.as_view()),
    path('coordinates/', CoordinatesView.as_view()),
    path('subtask/', SubTaskView.as_view()),
    path('task/', TaskView.as_view()),
    path('place/', PlaceTypeView.as_view())
]