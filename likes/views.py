from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Post, Like


# 게시글 좋아요 API
class TripPostLikeCreateView(generics.GenericAPIView):
    """게시글 좋아요 API"""
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({"message": "이미 좋아요를 눌렀습니다."}, status=status.HTTP_400_BAD_REQUEST)

        post.likes_count = post.post_likes.count()  # 좋아요 개수 업데이트
        post.save()

        return Response({"message": "좋아요를 눌렀습니다."}, status=status.HTTP_201_CREATED)


# 게시글 좋아요 취소 API
class TripPostLikeDeleteView(generics.GenericAPIView):
    """게시글 좋아요 취소 API"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Like.objects.filter(user=request.user, post=post)

        if not like.exists():
            return Response({"message": "좋아요를 누르지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        post.likes_count = post.post_likes.count()  # 좋아요 개수 업데이트
        post.save()

        return Response({"message": "좋아요를 취소했습니다."}, status=status.HTTP_204_NO_CONTENT)
