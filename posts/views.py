from locations.models import Location
from post_locations.models import PostLocation
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied

from .models import Post
from .serializers import (
    PostCreateSerializer,
    PostDetailSerializer,
    PostModifySerializer,
    PostListSerializer,
    MyPostListSerializer  # 내 게시글 목록 Serializer 추가
)

class TripPostCreateView(generics.CreateAPIView):
    """게시글 생성 API"""
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class TripPostDetailView(generics.RetrieveAPIView):
    """게시글 상세 조회 API (조회 시 view_count 증가)"""
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_url_kwarg = "post_id"

    def get_object(self):
        """is_public이 False면 작성자만 볼 수 있도록 제한 + view_count 증가"""
        post = super().get_object()

        if not post.is_public and post.user != self.request.user:
            raise PermissionDenied("비공개 게시물입니다.")

        return post


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


# 전체 게시글 조회 - likes counts 볼 수 있게
class TripPostListView(generics.ListAPIView):
    """게시글 목록 조회 및 검색 API"""
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get("q", "").strip()
        user_id = self.request.query_params.get("user_id", None)

        base_queryset = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_public=True,
        )

        return base_queryset.order_by("-created_at")


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