#!/bin/bash

cd /app

echo @@@@@@@@@@@@@@@ preparing migrations and run pytest @@@@@@@@@@@@@@@@@@

poetry run python manage.py makemigrations
poetry run python manage.py migrate
sleep 10


echo @@@@@@@@@@@@@@@@@@@ collecting backend static @@@@@@@@@@@@@@@@@@@@@@@

poetry run python manage.py collectstatic --noinput

echo @@@@@@@@@@@@@@@@@@@@@@@@@ run gunicorn @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

poetry run gunicorn --bind 0.0.0.0:8000 --reload backend.wsgi:application