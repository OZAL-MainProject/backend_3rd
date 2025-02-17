from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    """커스텀 유저 매니저"""

    def create_user(self, email, password=None, **extra_fields):
        """일반 유저 생성"""
        if not email:
            raise ValueError("Please enter your email address")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_password("")  # 빈 비밀번호 허용
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """슈퍼유저 생성"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """사용자 모델 (기존 DB 유지)"""

    username = None  # 기본 username 필드 제거
    email = models.EmailField(unique=True)  # 이메일을 로그인 ID로 사용
    password = models.CharField(max_length=128, default="")  # 🔥 기본값 추가하여 마이그레이션 오류 방지
    name = models.CharField(max_length=50, null=True, blank=True)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    profile_image = models.CharField(max_length=250, null=True, blank=True)
    provider = models.CharField(max_length=50, null=True, blank=True)  # ex) "kakao"
    provider_id = models.CharField(max_length=255, unique=True, null=True, blank=True)  # 카카오 ID
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"  # 이메일을 로그인 ID로 사용
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.nickname if self.nickname else self.email
