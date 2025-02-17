from rest_framework import serializers
from .models import Post


class PostCreateSerializer(serializers.ModelSerializer):
    """게시글 작성 Serializer"""

    class Meta:
        model = Post
        fields = ("title", "content", "is_public")

    def create(self, validated_data):
        """로그인한 사용자를 자동으로 user 필드에 추가"""
        user = self.context["request"].user
        if not user.is_authenticated:
            raise serializers.ValidationError({"error": "로그인이 필요합니다."})

        validated_data["user"] = user
        return super().create(validated_data)


class PostDetailSerializer(serializers.ModelSerializer):
    """게시글 상세 조회 Serializer"""
    user = serializers.StringRelatedField()
    like_count = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "content", "user", "created_at", "updated_at", "like_count")


class PostListSerializer(serializers.ModelSerializer):
    """게시글 목록 Serializer"""
    like_count = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "created_at", "like_count")


class PostModifySerializer(serializers.ModelSerializer):
    """게시글 수정 Serializer"""

    class Meta:
        model = Post
        fields = ("title", "content")


class MyPostListSerializer(serializers.ModelSerializer):
    """내 게시글 목록 Serializer"""

    class Meta:
        model = Post
        fields = ("id", "title", "content")