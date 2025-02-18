from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    """좋아요 정보를 반환하는 Serializer"""
    user = serializers.StringRelatedField(read_only=True)
    post = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
