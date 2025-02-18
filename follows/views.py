from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Follow, User
from .serializers import (
    FollowSerializer, UnfollowSerializer, UserSerializer,
    FollowListSerializer, FollowStatusSerializer
)


class FollowView(generics.CreateAPIView):
    # 특정 사용자를 팔로우하는 뷰
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        following_user = get_object_or_404(User, id=kwargs["user_id"])

        if request.user == following_user:
            return Response({"detail": "자기 자신을 팔로우할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        if Follow.objects.filter(follower=request.user, following=following_user).exists():
            return Response({"detail": "이미 팔로우 중입니다."}, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.create(follower=request.user, following=following_user)
        return Response(FollowSerializer(follow).data, status=status.HTTP_201_CREATED)


class UnfollowView(generics.DestroyAPIView):
    # 특정 사용자에 대한 팔로우를 취소하는 뷰
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        following_user = get_object_or_404(User, id=kwargs["user_id"])
        follow = Follow.objects.filter(follower=request.user, following=following_user)

        if not follow.exists():
            return Response({"detail": "팔로우하지 않은 사용자입니다."}, status=status.HTTP_400_BAD_REQUEST)

        follow.delete()
        return Response(UnfollowSerializer({"detail": "언팔로우 완료"}).data, status=status.HTTP_204_NO_CONTENT)


class FollowStatusView(generics.GenericAPIView):
    """
    특정 유저와의 팔로우 상태 확인
    - GET /follow/status/?user_id=<user_id> : 특정 유저를 팔로우하는지 확인
    - GET /follow/status/?type=following : 내가 팔로우하는 목록 조회
    - GET /follow/status/?type=followers : 나를 팔로우하는 목록 조회
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get("user_id")
        follow_type = request.query_params.get("type")

        if user_id:
            target_user = get_object_or_404(User, id=user_id)
            is_following = Follow.objects.filter(follower=request.user, following=target_user).exists()
            return Response(FollowStatusSerializer({"is_following": is_following}).data, status=status.HTTP_200_OK)

        if follow_type == "following":
            following_users = Follow.objects.filter(follower=request.user)
            return Response(FollowListSerializer(following_users, many=True).data, status=status.HTTP_200_OK)

        elif follow_type == "followers":
            follower_users = Follow.objects.filter(following=request.user)
            return Response(FollowListSerializer(follower_users, many=True).data, status=status.HTTP_200_OK)

        return Response({"detail": "올바른 type 파라미터가 필요합니다. ('following' 또는 'followers')"},
                        status=status.HTTP_400_BAD_REQUEST)


from rest_framework.exceptions import NotFound

class FollowingView(generics.ListAPIView):
    # 내가 팔로우하는 사용자 목록 조회
    serializer_class = FollowListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Follow.objects.filter(follower=self.request.user)
        if not queryset.exists() and not Follow.objects.filter(following=self.request.user).exists():
            raise NotFound("팔로우, 팔로잉을 하고 있는 사람이 없습니다.")
        if not queryset.exists():
            raise NotFound("팔로우하고 있는 사람이 없습니다.")
        return queryset


class FollowersView(generics.ListAPIView):
    # 나를 팔로우하는 사용자 목록 조회
    serializer_class = FollowListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Follow.objects.filter(following=self.request.user)
        if not queryset.exists() and not Follow.objects.filter(follower=self.request.user).exists():
            raise NotFound("팔로우, 팔로잉을 하고 있는 사람이 없습니다.")
        if not queryset.exists():
            raise NotFound("나를 팔로우하는 사람이 없습니다.")
        return queryset
