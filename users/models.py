from django.db import models

class User(models.Model):
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    profile_image = models.CharField(max_length=250)
    provider = models.CharField(max_length=50)
    provider_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nickname
