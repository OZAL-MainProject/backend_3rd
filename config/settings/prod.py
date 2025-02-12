from .base import *

ALLOWED_HOSTS = ["127.0.0.1"]

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

]