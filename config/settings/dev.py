from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("POSTGRES_HOST"),  # 기본값 제거
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "NAME": os.getenv("POSTGRES_DBNAME"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}


CORS_ALLOWED_ORIGINS += [
    "http://localhost:5173",  # 프론트엔드 주소
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://3.34.96.155"
]