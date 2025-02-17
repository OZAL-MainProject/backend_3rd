from django.urls import path
from .views import (
    TripPostCreateView,
    TripPostDetailView,
    TripPostUpdateView,
    TripPostDeleteView,
    TripPostListView,
    UserPostListView
)

urlpatterns = [
    path("", TripPostCreateView.as_view(), name="create_post"),
    path("<int:post_id>", TripPostDetailView.as_view(), name="post_detail"),
    path("<int:post_id>/modify", TripPostUpdateView.as_view(), name="post_update"),
    path("<int:post_id>/delete", TripPostDeleteView.as_view(), name="post_delete"),
    path("all", TripPostListView.as_view(), name="all_post_list"),
    path("<int:user_id>/post/", UserPostListView.as_view(), name="user_post_list"),
]
