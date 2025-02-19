import re

from locations.models import Location
from post_locations.models import PostLocation
from rest_framework import serializers
from .models import Post



class PostCreateSerializer(serializers.ModelSerializer):
    """게시글 작성 Serializer (장소 포함)"""
    locations = serializers.ListField(child=serializers.DictField(), required=False)

    class Meta:
        model = Post
        fields = ("title", "content", "is_public", "locations")

    def create(self, validated_data):
        """게시글 생성 시 장소 정보도 함께 저장"""
        locations_data = validated_data.pop("locations", [])
        user = self.context["request"].user

        if not user.is_authenticated:
            raise serializers.ValidationError({"error": "로그인이 필요합니다."})

        post = Post.objects.create(user=user, **validated_data)

        for seq, location_data in enumerate(locations_data, start=1):
            location, created = Location.objects.get_or_create(
                detail_address=location_data["detail_address"],
                address=location_data["address"],
                defaults={
                    "latitude": location_data["latitude"],
                    "longitude": location_data["longitude"]
                }
            )
            PostLocation.objects.create(post=post, location=location, sequence=seq)

        return post


class PostDetailSerializer(serializers.ModelSerializer):
    """게시글 상세 조회 Serializer"""
    user = serializers.StringRelatedField()
    like_count = serializers.IntegerField(source="likes_count", read_only=True)


    class Meta:
        model = Post
        fields = ("id", "title", "content", "user", "created_at", "updated_at", "like_count", "view_count")

class PostModifySerializer(serializers.ModelSerializer):
    locations = serializers.ListField(child=serializers.DictField(), required=False)  # 장소 리스트 필드 추가

    class Meta:
        model = Post
        fields = ("title", "content", "locations")

    def update(self, instance, validated_data):
        """게시글 수정 시 제목, 내용, 장소만 수정 가능 (작성자 변경 불가)"""
        locations_data = validated_data.pop("locations", None)  # 장소 데이터 가져오기

        # 수정 가능한 필드만 업데이트 (user는 변경하지 않음)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 장소 정보 수정
        if locations_data:
            instance.post_location.all().delete()  # 기존 장소 삭제
            for seq, location_data in enumerate(locations_data, start=1):
                location, _ = Location.objects.get_or_create(
                    detail_address=location_data["detail_address"],
                    address=location_data["address"],
                    defaults={
                        "latitude": location_data["latitude"],
                        "longitude": location_data["longitude"]
                    }
                )
                PostLocation.objects.create(post=instance, location=location, sequence=seq)

        return instance


class PostListSerializer(serializers.ModelSerializer):
    """게시글 목록 Serializer (좋아요 수 포함)"""
    first_image_url = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()
    likes_count = serializers.IntegerField(read_only=True)  # 좋아요 수 추가

    class Meta:
        model = Post
        fields = ["id", "title", "content", "user", "likes_count", "first_image_url"]

    def get_first_image_url(self, obj):
        """content에서 첫 번째 S3 URL을 추출"""
        urls = re.findall(r"https?://[^\s]+", obj.content)
        return urls[0] if urls else None


class MyPostListSerializer(serializers.ModelSerializer):
    first_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["title", "content", "first_image_url"]

    def get_first_image_url(self, obj):
        """content에서 첫 번째 S3 URL을 추출"""
        urls = re.findall(r"https?://[^\s]+", obj.content)
        return urls[0] if urls else None


class MyPostListSerializer(serializers.ModelSerializer):
    """내 게시글 목록 Serializer"""

    class Meta:
        model = Post
        fields = ("id", "title", "content")