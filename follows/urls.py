from django.urls import path
from .views import FollowView, UnfollowView, FollowStatusView, FollowingView, FollowersView

urlpatterns = [
    path("<int:user_id>/follow/", FollowView.as_view(), name="follow"),
    path("<int:user_id>/unfollow/", UnfollowView.as_view(), name="unfollow"),
    path("follow/status/", FollowStatusView.as_view(), name="follow-status"),
    path("following/", FollowingView.as_view(), name="following"),
    path("followers/", FollowersView.as_view(), name="followers")
]
