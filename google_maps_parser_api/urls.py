from django.contrib import admin
from django.urls import path

from google_maps_parser_api.views import ClientView, CredentialView, PlaceTypeView, StatusView, CoordinatesView, SubTaskView, TaskView, RequestDataView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('client/', ClientView.as_view()),
    path('credential/', CredentialView.as_view()),
    path('status/', StatusView.as_view()),
    path('coordinates/', CoordinatesView.as_view()),
    path('subtask/', SubTaskView.as_view()),
    path('task/', TaskView.as_view()),
    path('request_data/', RequestDataView.as_view()),
    path('place/', PlaceTypeView.as_view())
]