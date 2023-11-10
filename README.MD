### Uruchomienie w lokalnym środowisku
```
python3 -m venv create venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```
### Uruchomienie testów
```
python3 -m coverage run manage.py test
python3 -m coverage report
```

### Wykonać migracje i uruchomić
```
./start.sh
```

W przypadku uruchomienia bez zmiennych otoczenia:
```
- PIKA_USERNAME
- PIKA_PASSWORD
- PIKA_HOST
- PIKA_PORT
- API_DB_NAME
- API_DB_USER
- API_DB_PASSWORD
- API_DB_HOST
- API_DB_PORT
```
będzie używany sqlite3 i drukowanie zadań do terminalu.

Docker-compose file:
```
version: "3.3"
services:
    rabbitmq:
        container_name: "rabbitmq"
        image: rabbitmq:3.8-management-alpine
        environment:
            - RABBITMQ_DEFAULT_USER=django_api
            - RABBITMQ_DEFAULT_PASS=admin
        ports:
            - '5672:5672'

    api:
        container_name: "api"
        image: malyyigor34/15_min_google_maps_parser_api:v1
        ports:
            - "8111:8000"
        environment:
            - PIKA_USERNAME=django_api
            - PIKA_PASSWORD=admin
            - PIKA_HOST=rabbitmq
            - PIKA_PORT=5672
            - API_DB_NAME=google_maps_parser_api
            - API_DB_USER=google_maps_parser_api
            - API_DB_PASSWORD=admin
            - API_DB_HOST=db
            - API_DB_PORT=3306
        depends_on:
            db:
                condition: service_started
            rabbitmq:
                condition: service_started
        volumes:
            db_data:
```
