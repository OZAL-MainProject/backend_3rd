from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Post
from .serializers import PostCreateSerializer, PostDetailSerializer, PostModifySerializer, PostCommentSerializer, PostListSerializer

# 게시글 작성 API (Create)
class TripPostCreateView(generics.CreateAPIView):
    """게시글 생성 API"""
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
#    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


# 게시글 상세 조회 API (Read)
class TripPostDetailView(generics.RetrieveAPIView):
    """게시글 상세 조회 API"""
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_url_kwarg = "post_id"


# 게시글 수정 API (Update)
class TripPostUpdateView(generics.UpdateAPIView):
    """게시글 수정 API"""
    queryset = Post.objects.all()
    serializer_class = PostModifySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        if post.user != self.request.user:
            self.permission_denied(self.request, message="작성자만 수정할 수 있습니다.")
        return post


# 게시글 삭제 API (Delete)
class TripPostDeleteView(generics.DestroyAPIView):
    """게시글 삭제 API"""
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        if post.user != self.request.user:
            self.permission_denied(self.request, message="작성자만 삭제할 수 있습니다.")
        return post


# 게시글 검색 및 전체 조회 API (통합)
from django.db.models import Q
from .serializers import PostListSerializer


# 전체 게시글 목록 조회, if user.id 가 있으면 해당 유저의 게시글만 조회
# 그리고 검색???
class TripPostListView(generics.ListAPIView):
    """게시글 검색 및 전체 조회 API"""
    serializer_class = PostListSerializer

    def get_queryset(self):
        query = self.request.query_params.get("q", "").strip()
        return (
            Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query),
                is_public=True,
            )
            .order_by("-created_at")
        )
