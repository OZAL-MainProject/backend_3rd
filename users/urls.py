from django.urls import path
from .views import KakaoLoginView, RefreshTokenView

urlpatterns = [
    path("auth/login/kakao/", KakaoLoginView.as_view()),  # 카카오 로그인 API
    path("refresh/", RefreshTokenView.as_view(), name="token_refresh"),
]
