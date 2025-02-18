from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "created_at", "updated_at")  # 목록에서 보이는 필드
    search_fields = ("title", "user")  # 검색 가능 필드
    list_filter = ("created_at", "updated_at")  # 필터링 옵션
    ordering = ("-created_at",)  # 최신 게시글 우선 정렬
