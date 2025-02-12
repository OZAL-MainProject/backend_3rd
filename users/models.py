from django.db import models

class User(models.Model):
    email = models.CharField(max_length=200, unique=True, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    profile_image = models.CharField(max_length=250, null=True, blank=True)
    provider = models.CharField(max_length=50)  # "kakao" 값이 들어갈 예정
    provider_id = models.CharField(max_length=255, unique=True)  # 카카오에서 받은 유저 ID
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nickname if self.nickname else "No Nickname"
