from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from utils import generate_presigned_url, upload_to_s3
from .models import Post
from .serializers import (
    PostCreateSerializer,
    PostDetailSerializer,
    PostModifySerializer,
    PostListSerializer,
    MyPostListSerializer  # 내 게시글 목록 Serializer 추가
)



class TripPostCreateView(generics.CreateAPIView):
    """게시글 생성 API (map_image, post_image 업로드 포함)"""
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # 이미지 업로드 지원

    def create(self, request, *args, **kwargs):
        post_data = request.data.copy()

        # 지도 이미지 업로드
        if "map_image" in request.FILES:
            post_data["map_image"] = upload_to_s3(request.FILES["map_image"], "maps")

        # 게시글 이미지 업로드
        if "post_image" in request.FILES:
            post_data["post_image"] = upload_to_s3(request.FILES["post_image"], "posts")

        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TripPostDetailView(generics.RetrieveAPIView):
    """게시글 상세 조회 API (조회 시 view_count 증가)"""
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_url_kwarg = "post_id"

    def get_object(self):
        """is_public이 False면 작성자만 볼 수 있도록 제한 + view_count 증가"""
        post = super().get_object()

        # 비공개 게시물은 작성자만 조회 가능
        if not post.is_public and post.user != self.request.user:
            raise PermissionDenied("비공개 게시물입니다.")

        # 조회수 증가 후 즉시 저장 (save() 사용)
        post.view_count += 1
        post.save()

        return post

    def retrieve(self, request, *args, **kwargs):
        """게시글 상세 조회 시 S3 Presigned URL 포함"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Presigned URL 생성
        map_image_url = generate_presigned_url(instance.map_image) if instance.map_image else None
        post_image_url = generate_presigned_url(instance.post_image) if instance.post_image else None

        return Response({
            **serializer.data,
            "map_image_url": map_image_url,
            "post_image_url": post_image_url,
        })

class TripPostUpdateView(generics.UpdateAPIView):
    """게시글 수정 API (작성자만 가능)"""
    queryset = Post.objects.all()
    serializer_class = PostModifySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """게시글 작성자만 수정 가능"""
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        if post.user != self.request.user:
            raise PermissionDenied("게시글 작성자만 수정할 수 있습니다.")  # 수정
        return post


class TripPostDeleteView(generics.DestroyAPIView):
    """게시글 삭제 API (작성자만 가능)"""
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """게시글 작성자만 삭제 가능"""
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        if post.user != self.request.user:
            raise PermissionDenied("게시글 작성자만 삭제할 수 있습니다.")  # 수정
        return post


# 전체 게시글 조회
class TripPostListView(generics.ListAPIView):
    """게시글 목록 조회 API (썸네일 포함)"""
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get("q", "").strip()
        return Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_public=True,
        ).order_by("-created_at")

    def list(self, request, *args, **kwargs):
        """게시글 목록 조회 시 썸네일 포함"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # 각 게시글에 대한 Presigned URL 생성 (썸네일 포함)
        posts_data = []
        for post in queryset:
            post_data = serializer.data[queryset.index(post)]
            post_data["thumbnail_url"] = generate_presigned_url(post.post_image, expiration=86400) if post.post_image else None
            posts_data.append(post_data)

        return Response(posts_data, status=status.HTTP_200_OK)


class UserPostListView(generics.ListAPIView):
    """특정 사용자의 게시글 목록 조회 API (비로그인 사용자는 접근 불가)"""
    serializer_class = MyPostListSerializer
    permission_classes = [permissions.IsAuthenticated]  # 로그인 필수

    def get_queryset(self):
        """로그인한 유저만 접근 가능하며, 본인의 게시글은 전체 조회 가능 / 다른 유저의 게시글은 공개된 게시글만 조회"""
        user_id = self.kwargs.get("user_id")

        if self.request.user.id == int(user_id):
            # 본인의 게시글은 모두 조회 가능
            return Post.objects.filter(user_id=user_id).order_by("-created_at")
        else:
            # 다른 사용자의 게시글은 공개된 게시글만 조회 가능
            return Post.objects.filter(user_id=user_id, is_public=True).order_by("-created_at")

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # 방문한 장소 목록 추가
        visited_locations = set()
        for post in queryset:
            for location in post.post_location.all():
                visited_locations.add({
                    "id": location.id,
                    "address": location.address,
                    "latitude": location.latitude,
                    "longitude": location.longitude
                })

        return Response({
            "posts": serializer.data,
            "visited_locations": list(visited_locations)
        }, status=status.HTTP_200_OK)