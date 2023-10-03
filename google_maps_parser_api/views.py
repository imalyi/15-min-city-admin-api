from rest_framework.generics import ListCreateAPIView

from google_maps_parser_api.serializers import ClientSerializer
from google_maps_parser_api.models import Client

class ClientView(ListCreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

