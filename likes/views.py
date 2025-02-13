from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Post

# 게시글 좋아요 API
class TripPostLikeCreateView(generics.GenericAPIView):
    """게시글 좋아요 API"""
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.likes.add(request.user)  # 좋아요 추가
        post.likes_count = post.likes.count()  # 좋아요 개수 업데이트
        post.save()
        return Response({"message": "좋아요를 눌렀습니다."}, status=status.HTTP_201_CREATED)


# 게시글 좋아요 취소 API
class TripPostLikeDeleteView(generics.GenericAPIView):
    """게시글 좋아요 취소 API"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.likes.remove(request.user)  # 좋아요 삭제
        post.likes_count = post.likes.count()  # 좋아요 개수 업데이트
        post.save()
        return Response({"message": "좋아요를 취소했습니다."}, status=status.HTTP_204_NO_CONTENT)


# 댓글 관련 API (comments/views.py)
from .serializers import PostCommentSerializer

# 게시글 댓글 작성 API
class TripPostCommentCreateView(generics.CreateAPIView):
    """게시글 댓글 작성 API"""
    serializer_class = PostCommentSerializer  # 댓글을 위한 별도 Serializer 필요
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        serializer.save(writer=self.request.user, post=post)



