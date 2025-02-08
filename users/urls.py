from django.urls import path
from .views import kakao_login

urlpatterns = [
    path("auth/login/kakao/", kakao_login),  # 요청을 받을 API 경로
]