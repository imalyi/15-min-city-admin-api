from django.urls import path
from rest_framework import routers
from openstreetmaps.views import TaskView, TaskResultView

router = routers.SimpleRouter()
router.register('task', TaskView, 'osm-task')
router.register('result', TaskResultView, 'osm-result')


urlpatterns = [] + router.urls
