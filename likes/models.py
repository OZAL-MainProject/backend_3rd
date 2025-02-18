from django.db import models
from posts.models import Post
from users.models import User

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="unique_like")
        ]
        ordering = ["-created_at"]  # 최신 좋아요가 먼저 정렬됨

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"
