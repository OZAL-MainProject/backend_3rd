"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# config url은 뒤에 슬래쉬 붙이고 나머지 url은 앞에 슬래쉬 붙이지마

urlpatterns = [
    path('admin/', admin.site.urls),
    # 이 아랫 부분은 우리가 사용하는 app들의 URL들을 넣습니다.
    path('ozal/', include('users.urls')),
    path('ozal/trippost/', include('posts.urls')),
]
