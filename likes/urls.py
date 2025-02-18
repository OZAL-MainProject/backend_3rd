from django.urls import path
from .views import (

    TripPostLikeCreateView,
    TripPostLikeDeleteView,
)

urlpatterns = [
    # 게시글 좋아요 (Like)
    path("<int:post_id>/like/", TripPostLikeCreateView.as_view(), name="post_like_create"),

    # 게시글 좋아요 삭제 (Unlike)
    path("<int:post_id>/unlike/", TripPostLikeDeleteView.as_view(), name="post_like_delete"),

]