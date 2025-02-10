from django.urls import path
from .views import kakao_login
from .views import kakao_callback

urlpatterns = [
    path("ozal/auth/login/kakao/", kakao_login),  # 카카오 로그인 API
    path("accounts/kakao/login/callback", kakao_callback),  # 카카오 로그인 콜백
]
