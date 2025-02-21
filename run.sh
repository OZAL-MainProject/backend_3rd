#!/bin/bash
set -e

echo "🛠 DJANGO_ENV 값: $DJANGO_ENV"  # ✅ 환경 변수 디버깅

if [ -z "$DJANGO_ENV" ]; then
    echo "⚠️  DJANGO_ENV가 설정되지 않았습니다. 기본값(dev) 사용"
    export DJANGO_SETTINGS_MODULE=config.settings.dev
elif [ "$DJANGO_ENV" = "production" ]; then
    echo "✅ production 환경입니다! Django 설정을 prod로 적용합니다."
    export DJANGO_SETTINGS_MODULE=config.settings.prod
else
    echo "⚠️  알 수 없는 DJANGO_ENV 값: $DJANGO_ENV (기본값 dev 적용)"
    export DJANGO_SETTINGS_MODULE=config.settings.dev
fi

echo "🔥 적용된 DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"  # ✅ 최종 적용 확인

poetry run python manage.py collectstatic --no-input
poetry run python manage.py migrate
poetry run gunicorn --workers 3 --bind 0.0.0.0:8000 config.wsgi:application
