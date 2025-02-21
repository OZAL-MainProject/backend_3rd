from rest_framework import serializers

from images.models import PostImages
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content", "map_image")


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "thumbnail", "content", "created_at")

class AuthUserPostListSerializer(serializers.ModelSerializer):

    post_id = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("post_id", "title", "thumbnail", "content", "created_at")

    def get_post_id(self, obj):
        return obj.id


class PostDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ("title", "content", "map_image", "images", "created_at")

    def get_images(self, obj):
        return [post_image.image.url for post_image in PostImages.objects.filter(post=obj)]
