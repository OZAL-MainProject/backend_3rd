#!/bin/bash
set -e

export PYTHONPATH="/app"

if [ "$DJANGO_ENV" = "production" ]; then
    export DJANGO_SETTINGS_MODULE=config.settings.prod
else
    export DJANGO_SETTINGS_MODULE=config.settings.dev
fi

poetry run python manage.py collectstatic --noinput
poetry run python manage.py migrate
poetry run gunicorn --workers 3 --bind 0.0.0.0:8000 config.wsgi:application