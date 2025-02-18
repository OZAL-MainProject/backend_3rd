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
