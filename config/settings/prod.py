from .base import *

ALLOWED_HOSTS = ["127.0.0.1", "3.34.96.155"]

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": ENV.get("POSTGRES_HOST"),  # 기본값 제거
        "USER": ENV.get("POSTGRES_USER"),
        "PASSWORD": ENV.get("POSTGRES_PASSWORD"),
        "NAME": ENV.get("POSTGRES_DBNAME"),
        "PORT": ENV.get("POSTGRES_PORT"),
    }
}

# 나중에 변경
CORS_ALLOWED_ORIGINS += [
    "http://3.34.96.155",
    "http://localhost:5173",  # 프론트엔드 주소
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]