from django.urls import path
from .views import (
    TripPostCreateView,
    TripPostDetailView,
    TripPostUpdateView,
    TripPostDeleteView,
    TripPostListView,
)

urlpatterns = [
    # 게시글 작성 (Create)
    path("", TripPostCreateView.as_view(), name="create_post"),

    # 상세 게시글 조회 (Read)
    path("<int:post_id>", TripPostDetailView.as_view(), name="post_detail"),

    # 게시글 수정 (Update)
    path("<int:post_id>/modify", TripPostUpdateView.as_view(), name="post_update"),

    # 게시글 삭제 (Delete)
    path("<int:post_id>/delete", TripPostDeleteView.as_view(), name="post_delete"),

    # 전체 게시글 목록 조회 (All Posts)
    path("all", TripPostListView.as_view(), name="all_post_list"),

]
