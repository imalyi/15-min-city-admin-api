import datetime
import unittest

import googlemaps.client
from django.test import TestCase
from collectors.gmaps.response import Response, generate_date, InvalidAPIKey
from unittest.mock import MagicMock, patch, PropertyMock
import os


class TestResponse(TestCase):
    def setUp(self):
        secret = os.environ.get("GMAPS_TOKEN", "secret")
        self.response = Response(MagicMock(), secret, "type", 1000, (123, 132))

    def test_generate_date(self):
        date_from_func = generate_date()
        self.assertIsInstance(date_from_func, datetime.datetime)
        self.assertEquals(date_from_func.day, datetime.datetime.today().day)
        self.assertEquals(date_from_func.hour, 0)

    def test_create_gmaps_client_with_invalid_key(self):
        self.response.token = "token"
        with self.assertRaises(InvalidAPIKey):
            self.response._create_gmaps_client()

    @unittest.skipIf(os.environ.get("GMAPS_TOKEN", True), 'To run tests, set a Google Maps API key to OS variable GMAPS_TOKEN')
    def test_create_gmaps_client_with_valid_key(self):
        self.response._create_gmaps_client()
        self.assertIsInstance(self.response.client, googlemaps.client.Client)

    @unittest.skipIf(os.environ.get("GMAPS_TOKEN", True), 'To run tests, set a Google Maps API key to OS variable GMAPS_TOKEN')
    @patch("gmaps.response.googlemaps.Client.places_nearby")
    def test_make_request_with_no_next_page(self, mock_places_nearby):
        self.response._create_gmaps_client()
        mock_response = {'results': ""}
        mock_places_nearby.return_value = mock_response

        self.response._make_request()
        self.assertEquals(mock_places_nearby.call_count, 1)
        mock_places_nearby.assert_called_with(location=self.response.location, type=self.response.type_, radius=self.response.radius)

    @unittest.skipIf(os.environ.get("GMAPS_TOKEN", True), 'To run tests, set a Google Maps API key to OS variable GMAPS_TOKEN')
    @patch("gmaps.response.Response._next_page", new_callable=PropertyMock)
    @patch("gmaps.response.googlemaps.Client.places")
    def test_make_request_with_next_page(self, mock_client, mock_next_page):
        self.response._create_gmaps_client()
        mock_next_page.return_value = "mock_next_page_token"
        mock_client.return_value = {}
        self.response._make_request()
        mock_client.assert_called_with(page_token="mock_next_page_token")
