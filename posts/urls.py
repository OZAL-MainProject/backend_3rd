from django.urls import path
from .views import TripPostView, PostDetailView, PostListView, Thumbnail
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('', TripPostView.as_view(), name='post-list'),
    path('login/', TokenObtainPairView.as_view(), name='post-login'),
    path('<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
    path('list/<int:user_id>/', PostListView.as_view(), name='post-list'),
    path('thumbnails/', Thumbnail.as_view(), name='post-thumbnails'),
]