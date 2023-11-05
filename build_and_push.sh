#!/bin/bash

pip3 freeze > requirements.txt
sudo docker build . -t malyyigor34/15_min_google_maps_parser_api:v1
sudo docker image push malyyigor34/15_min_google_maps_parser_api:v1