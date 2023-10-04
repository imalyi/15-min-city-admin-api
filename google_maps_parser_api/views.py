from rest_framework.generics import ListCreateAPIView

from google_maps_parser_api.serializers import ClientSerializer, CredentialSerializer, PlaceTypeSerializer, StatusSerializer, CoordinateSerializer
from google_maps_parser_api.models import Client, Credential, PlaceType, Status, Coordinate


class ClientView(ListCreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class CredentialView(ListCreateAPIView):
    serializer_class = CredentialSerializer
    queryset = Credential.objects.all()

class PlaceTypeView(ListCreateAPIView):
    serializer_class = PlaceTypeSerializer
    queryset = PlaceType.objects.all()


class StatusView(ListCreateAPIView):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()

class CoordinatesView(ListCreateAPIView):
    serializer_class = CoordinateSerializer
    queryset = Coordinate.objects.all()