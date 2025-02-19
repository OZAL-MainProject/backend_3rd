from rest_framework import serializers
from .models import Follow, User


class FollowSerializer(serializers.ModelSerializer):
    # 팔로우 관계를 직렬화하는 Serializer
    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "created_at"]
        read_only_fields = ["follower"]  # 요청하는 사용자가 자동으로 설정됨


class UnfollowSerializer(serializers.Serializer):
    # 언팔로우 요청을 처리하는 Serializer
    detail = serializers.CharField()


class FollowUserSerializer(serializers.ModelSerializer):
    # 사용자 정보를 직렬화하는 Serializer
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "nickname", "follower_count", "following_count"]

    def get_follower_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()


class FollowListSerializer(serializers.ModelSerializer):
    # 사용자의 팔로우/팔로워 목록을 조회하는 Serializer
    user = UserSerializer(source="following", read_only=True)

    class Meta:
        model = Follow
        fields = ["user"]


class FollowStatusSerializer(serializers.Serializer):
    # 특정 사용자에 대한 팔로우 상태를 반환하는 Serializer
    is_following = serializers.BooleanField()
