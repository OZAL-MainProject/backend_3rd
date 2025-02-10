from django.urls import path
from .views import (
    TripPostCreateView,
    TripPostDetailView,
    TripPostUpdateView,
    TripPostDeleteView,
    TripPostLikeCreateView,
    TripPostLikeDeleteView,
    TripPostCommentCreateView,
    TripPostSearchView,
    TripPostListView,
    TripPostUserListView,
)

urlpatterns = [
    # 게시글 작성 (Create)
    path("ozal/trippost", TripPostCreateView.as_view(), name="create_post"),

    # 상세 게시글 조회 (Read)
    path("ozal/trippost/<int:post_id>", TripPostDetailView.as_view(), name="post_detail"),

    # 게시글 수정 (Update)
    path("ozal/trippost/<int:post_id>/modify", TripPostUpdateView.as_view(), name="post_update"),

    # 게시글 삭제 (Delete)
    path("ozal/trippost/<int:post_id>/delete", TripPostDeleteView.as_view(), name="post_delete"),

    # 게시글 좋아요 (Like)
    path("ozal/trippost/<int:post_id>/like", TripPostLikeCreateView.as_view(), name="post_like_create"),

    # 게시글 좋아요 삭제 (Unlike)
    path("ozal/trippost/<int:post_id>/unlike", TripPostLikeDeleteView.as_view(), name="post_like_delete"),

    # 게시글 댓글 작성 (Comment)
    path("ozal/trippost/<int:post_id>/comment", TripPostCommentCreateView.as_view(), name="post_comment_create"),

    # 내 게시글 목록 조회 (My Posts)
    path("ozal/trippost/<int:user_id>", TripPostUserListView.as_view(), name="user_post_list"),

    # 전체 게시글 목록 조회 (All Posts)
    path("ozal/trippost/all", TripPostListView.as_view(), name="all_post_list"),

    # 게시글 검색 (Search)
    path("ozal/trippost/search", TripPostSearchView.as_view(), name="post_search"),
]
