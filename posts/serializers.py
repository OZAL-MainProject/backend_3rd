from rest_framework import serializers
from .models import Post


class PostCreateSerializer(serializers.ModelSerializer):
    """게시글 작성 Serializer"""
    writer = serializers.HiddenField(default=serializers.CurrentUserDefault())  # 로그인한 사용자 자동 설정

    class Meta:
        model = Post
        fields = ("title", "content", "is_public", "user")


class PostDetailSerializer(serializers.ModelSerializer):
    """게시글 상세 조회 Serializer"""
    writer = serializers.StringRelatedField()  # 작성자 이름 표시
    like_count = serializers.IntegerField(source="likes.count", read_only=True)  # 좋아요 개수

    class Meta:
        model = Post
        fields = ("id", "title", "content", "user", "created_at", "updated_at", "like_count")


class PostListSerializer(serializers.ModelSerializer):
    """게시글 목록 Serializer"""
    like_count = serializers.IntegerField(source="likes.count", read_only=True)  # 좋아요 개수

    class Meta:
        model = Post
        fields = ("id", "title", "created_at", "like_count")


class PostLikeSerializer(serializers.Serializer):
    """게시글 좋아요 Serializer"""
    user_id = serializers.IntegerField()
    post_id = serializers.IntegerField()


class PostCommentSerializer(serializers.Serializer):
    """게시글 댓글 Serializer"""
    user_id = serializers.IntegerField()
    post_id = serializers.IntegerField()
    content = serializers.CharField()


class PostModifySerializer(serializers.ModelSerializer):
    """게시글 수정 Serializer"""

    class Meta:
        model = Post
        fields = ("title", "content")


class PostDeleteSerializer(serializers.Serializer):
    """게시글 삭제 Serializer"""
    post_id = serializers.IntegerField()
