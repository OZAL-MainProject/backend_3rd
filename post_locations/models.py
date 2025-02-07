from django.db import models
from locations.models import Location
from posts.models import Post


class PostLocation(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_location')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='post_location')
    sequence = models.SmallIntegerField()

    def __str__(self):
        return f"Location {self.sequence} for {self.post.title}"
