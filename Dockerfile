FROM python:3.11

ENV DockerHOME=/home/apps/google_maps_parser_api/

RUN mkdir -p $DockerHOME

RUN apt-get update -y -q
RUN apt-get install python3-dev default-libmysqlclient-dev build-essential -y -q

WORKDIR $DockerHOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . $DockerHOME
RUN pip install -r requirements.txt
EXPOSE 8000


RUN chmod +x /home/apps/google_maps_parser_api/start.sh
CMD ["./start.sh"]
