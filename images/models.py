from django.db import models
from posts.models import Post

# Create your models here.
class Images(models.Model):
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'images'


class PostImages(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ForeignKey(Images, on_delete=models.CASCADE)

    class Meta:
        db_table = 'post_images'