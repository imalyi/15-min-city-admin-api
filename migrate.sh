rm db.sqlite3
rm -r google_maps_parser_api/migrations/

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py makemigrations google_maps_parser_api
python3 manage.py migrate google_maps_parser_api

DJANGO_SUPERUSER_USERNAME=igor \
DJANGO_SUPERUSER_PASSWORD=343877 \
DJANGO_SUPERUSER_EMAIL="admin@admin.com" \
python manage.py createsuperuser --noinput