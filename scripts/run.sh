#!/bin/bash
set -e

export PYTHONPATH="/app"
export DJANGO_SETTINGS_MODULE=config.settings.dev

poetry run python manage.py collectstatic --noinput
poetry run python manage.py migrate
poetry run gunicorn --workers 3 --bind 0.0.0.0:8000 config.wsgi:application