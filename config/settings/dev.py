from .base import *

DEBUG = True # ALLOWED_HOSTS = ["*"]

CUSTOM_APPS += [
    'drf_yasg', # swaggerUI 보게 해주는 라이브러리
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


CORS_ALLOWED_ORIGINS += [
    "http://localhost:5173",  # 프론트엔드 주소
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]