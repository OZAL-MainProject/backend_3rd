import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer


class KakaoLoginView(APIView):
    """카카오 로그인 API"""

    def post(self, request):
        code = request.data.get("code")
        if not code:
            return Response({"error": "인가 코드가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 1️⃣ 카카오 토큰 요청
        token_url = "https://kauth.kakao.com/oauth/token"
        token_data = {
            "grant_type": "authorization_code",
            "client_id": settings.KAKAO_CLIENT_ID,
            "redirect_uri": settings.KAKAO_REDIRECT_URI,
            'client_secret':settings.KAKAO_SECRET,
            "code": code,
        }
        token_headers = {"Content-Type": "application/x-www-form-urlencoded"}
        token_res = requests.post(token_url, data=token_data, headers=token_headers)

        if token_res.status_code != 200:
            return Response({"error": "카카오 토큰 요청 실패"}, status=status.HTTP_400_BAD_REQUEST)

        access_token = token_res.json().get("access_token")

        if not access_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)


        # 2️⃣ 유저 정보 요청
        user_info_url = "https://kapi.kakao.com/v2/user/me"
        user_info_headers = {"Authorization": f"Bearer {access_token}"}
        user_info_res = requests.get(user_info_url, headers=user_info_headers)

        if user_info_res.status_code != 200:
            return Response({"error": "카카오 사용자 정보 요청 실패"}, status=status.HTTP_400_BAD_REQUEST)

        user_info_json = user_info_res.json()
        kakao_id = str(user_info_json.get("id"))

        # 필수 정보 확인 (email, nickname)
        email = user_info_json["kakao_account"].get("email")
        nickname = user_info_json["properties"].get("nickname")

        if not email or not nickname:
            return Response({"error": "이메일 또는 닉네임이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        profile_image = user_info_json["properties"].get("profile_image", "")

        # 3️⃣ 유저 저장
        user, created = User.objects.update_or_create(
            provider_id=kakao_id,
            defaults={
                "email": email,
                "nickname": nickname,
                "profile_image": profile_image,
                "provider": "kakao",
            },
        )

        # 4️⃣ JWT 토큰 발급
        refresh = RefreshToken.for_user(user)
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response({
            "tokens": tokens,
            "user": UserSerializer(user).data,
        }, status=status.HTTP_200_OK)