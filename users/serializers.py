from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "nickname", "profile_image", "provider")


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate_refresh(self, value):
        """리프레시 토큰 검증"""
        try:
            return RefreshToken(value)
        except Exception:
            raise ValidationError("리프레시 토큰이 유효하지 않거나 만료되었습니다. 다시 로그인하세요.")


class UserNicknameUpdateSerializer(serializers.ModelSerializer):
    """닉네임 수정 Serializer"""

    class Meta:
        model = User
        fields = ["nickname"]

    def validate_nickname(self, value):
        if not value.strip():
            raise serializers.ValidationError("닉네임을 입력해주세요.")
        return value


class UserProfileImageUpdateSerializer(serializers.ModelSerializer):
    """프로필 이미지 수정 Serializer"""

    class Meta:
        model = User
        fields = ["profile_image"]

    def validate_profile_image(self, value):
        if not value.startswith("http"):
            raise serializers.ValidationError("올바른 URL을 입력해주세요.")
        return value