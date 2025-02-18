from django.db import models
from users.models import User

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # 중복 방지

    def __str__(self):
        return f"{self.follower.nickname} follows {self.following.nickname}"
