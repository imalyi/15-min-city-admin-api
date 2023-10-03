
from django.contrib import admin
from django.urls import path

from google_maps_parser_api.views import ClientView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('client/', ClientView.as_view())
]
