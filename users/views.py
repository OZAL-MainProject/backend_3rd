import os
import requests
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

# .env 파일 로드
load_dotenv()

KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")

def get_tokens_for_user(user):
    """JWT 토큰 생성 함수"""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

@api_view(["POST"])
def kakao_login(request):
    """카카오 로그인 API"""
    code = request.data.get("code")
    if not code:
        return Response({"error": "인가 코드가 없습니다."}, status=400)

    # 1️⃣ 카카오에 인가 코드 전송 → 액세스 토큰 요청
    token_url = "https://kauth.kakao.com/oauth/token"
    token_data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "code": code,
    }
    token_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_res = requests.post(token_url, data=token_data, headers=token_headers)
    token_json = token_res.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return Response({"error": "카카오 토큰 발급 실패"}, status=400)

    # 2️⃣ 액세스 토큰을 사용해 사용자 정보 요청
    user_info_url = "https://kapi.kakao.com/v2/user/me"
    user_info_headers = {"Authorization": f"Bearer {access_token}"}
    user_info_res = requests.get(user_info_url, headers=user_info_headers)
    user_info_json = user_info_res.json()

    kakao_id = str(user_info_json.get("id"))
    email = user_info_json["kakao_account"].get("email", None)
    nickname = user_info_json["properties"].get("nickname", None)
    profile_image = user_info_json["properties"].get("profile_image", None)

    # 3️⃣ DB에서 유저 조회 / 생성
    user, created = User.objects.get_or_create(
        provider_id=kakao_id,
        defaults={
            "email": email,
            "nickname": nickname,
            "profile_image": profile_image,
            "provider": "kakao",
        },
    )

    # 4️⃣ JWT 토큰 발급
    tokens = get_tokens_for_user(user)

    return Response({
        "tokens": tokens,
        "user": {
            "email": user.email,
            "nickname": user.nickname,
            "profile_image": user.profile_image,
        },
    })

@api_view(["GET"])
def kakao_callback(request):
    """카카오 로그인 Redirect URI에 대한 처리"""
    return Response({"message": "카카오 로그인 완료!"})

