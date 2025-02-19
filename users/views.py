from rest_framework.parsers import MultiPartParser, FormParser
import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from utils import generate_presigned_url, upload_to_s3
from .models import User
from .serializers import UserSerializer, RefreshTokenSerializer
from django.shortcuts import get_object_or_404
from .serializers import UserNicknameUpdateSerializer, UserProfileImageUpdateSerializer


class KakaoLoginView(APIView):
    """카카오 로그인 API"""
    serializer_class = UserSerializer

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


class RefreshTokenView(APIView):
    """리프레시 토큰을 이용해 새로운 액세스 토큰 발급"""
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            refresh = serializer.validated_data["refresh"]
            return Response({"access": str(refresh.access_token)}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class IsOwner(permissions.BasePermission):
    """본인만 프로필을 수정할 수 있도록 하는 권한"""

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class UpdateNicknameView(generics.UpdateAPIView):
    """닉네임 수정 뷰"""

    queryset = User.objects.all()
    serializer_class = UserNicknameUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self):
        return self.request.user


class UserProfileView(generics.RetrieveAPIView):
    """프로필 조회 API - Presigned URL 포함"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        profile_image_url = None

        if user.profile_image:
            profile_image_url = generate_presigned_url(user.profile_image)  # ✅ None 방지

        serializer = self.get_serializer(user)
        return Response({
            **serializer.data,
            "profile_image_url": profile_image_url,
        })


class MyPageView(generics.RetrieveAPIView):
    """로그인한 사용자의 마이페이지 조회 API"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """현재 로그인한 사용자의 정보를 반환"""
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        """Presigned URL을 포함한 마이페이지 정보 반환"""
        user = self.get_object()
        profile_image_url = generate_presigned_url(user.profile_image) if user.profile_image else None

        serializer = self.get_serializer(user)
        return Response({
            **serializer.data,
            "profile_image_url": profile_image_url,  # Presigned URL 추가
        })


class UpdateProfileImageView(generics.UpdateAPIView):
    """프로필 이미지 수정 API (S3 업로드 후 정적 URL 반환)"""

    queryset = User.objects.all()
    serializer_class = UserProfileImageUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        """로그인한 사용자만 자신의 프로필을 수정할 수 있도록 설정"""
        return self.request.user

    def update(self, request, *args, **kwargs):
        try:
            user = self.get_object()

            # S3에 새 이미지 업로드
            if "profile_image" in request.FILES:
                s3_key = upload_to_s3(request.FILES["profile_image"], "profiles")  # S3 키만 반환
                user.profile_image = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{s3_key}"
                user.save()

            return Response({
                "profile_image_url": user.profile_image  # ✅ Presigned URL 대신 S3 정적 URL 반환
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"🔥 프로필 이미지 업데이트 오류: {str(e)}")  # ✅ 에러 로깅 추가
            return Response({"error": "서버 내부 오류 발생", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    """로그아웃 API - 리프레시 토큰 무효화"""
    serializer_class = RefreshTokenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            refresh = serializer.validated_data["refresh"]
            try:
                refresh.blacklist()  # 리프레시 토큰을 블랙리스트에 추가하여 무효화
                return Response({"detail": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)
            except Exception:
                return Response({"error": "유효하지 않은 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
