from django.urls import path
from rest_framework import routers
from openstreetmaps.views import TaskView

router = routers.SimpleRouter()
router.register('task', TaskView, 'osm-task')


urlpatterns = [] + router.urls
