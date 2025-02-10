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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)


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



class TripPostLikeCreateView(generics.GenericAPIView):
    """게시글 좋아요 API"""
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.likes.add(request.user)  # 좋아요 추가
        post.likes_count = post.likes.count()  # 좋아요 개수 업데이트
        post.save()
        return Response({"message": "좋아요를 눌렀습니다."}, status=status.HTTP_201_CREATED)

class TripPostLikeDeleteView(generics.GenericAPIView):
    """게시글 좋아요 취소 API"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.likes.remove(request.user)  # 좋아요 삭제
        post.likes_count = post.likes.count()  # 좋아요 개수 업데이트
        post.save()
        return Response({"message": "좋아요를 취소했습니다."}, status=status.HTTP_204_NO_CONTENT)


# 게시글 댓글 작성 API (Comment)
class TripPostCommentCreateView(generics.CreateAPIView):
    """게시글 댓글 작성 API"""
    serializer_class = PostCommentSerializer  # 댓글을 위한 별도 Serializer 필요
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        serializer.save(writer=self.request.user, post=post)


# 게시글 검색 API (Search)
class TripPostSearchView(generics.ListAPIView):
    """게시글 검색 API"""
    serializer_class = PostListSerializer

    def get_queryset(self):
        query = self.request.query_params.get("q", "")
        return Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by("-created_at")

# 전체 게시글 목록 조회 API (All Posts)
class TripPostListView(generics.ListAPIView):
    """전체 게시글 목록 조회 API"""
    serializer_class = PostListSerializer

    def get_queryset(self):
        return Post.objects.filter(is_public=True).order_by("-created_at")



# 특정 사용자의 게시글 목록 조회 API (User Posts)
class TripPostUserListView(generics.ListAPIView):
    """특정 사용자의 게시글 목록 조회 API"""
    serializer_class = PostListSerializer

    def get_queryset(self):
        return Post.objects.filter(writer__id=self.kwargs["user_id"])
