from django.urls import path
from .views import KakaoLoginView, RefreshTokenView, UpdateNicknameView, UpdateProfileImageView

urlpatterns = [
    path("auth/login/kakao/", KakaoLoginView.as_view()),  # 카카오 로그인 API
    path("refresh/", RefreshTokenView.as_view(), name="token_refresh"),
    path("mypage/update/", UpdateNicknameView.as_view(), name="update-nickname"),
    path("mypage/update/image/", UpdateProfileImageView.as_view(), name="update-profile-image"),
]