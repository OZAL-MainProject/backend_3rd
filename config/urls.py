from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path("admin/", admin.site.urls),

    # Swagger API 문서 URL
    path("ozal/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("ozal/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("ozal/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # 기존 API 엔드포인트
    path("ozal/", include("users.urls")),
    path("ozal/trippost/", include("posts.urls")),
    path("ozal/trippost/", include("likes.urls")),
    path("ozal/travel/", include("locations.urls")),
    path("ozal/users/", include("follows.urls")),
]
