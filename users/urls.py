from django.urls import path
from .views import KakaoLoginView

urlpatterns = [
    path("auth/login/kakao/", KakaoLoginView.as_view()),  # 카카오 로그인 API
]
