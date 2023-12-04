#!/bin/bash

rm db.sqlite3
rm -r google_maps_parser_api/migrations/
rm -r gmaps/migrations
rm -r google_maps_parser_api/migrations
rm -r status/migrations
rm -r users/migrations

pip3 freeze > requirements.txt
sudo docker build . -t malyyigor34/15_min_google_maps_parser_api:v1
sudo docker image push malyyigor34/15_min_google_maps_parser_api:v1
