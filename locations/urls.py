from django.urls import path
from .views import RandomTravelRecommendation

urlpatterns = [
    path("recommend/", RandomTravelRecommendation.as_view(), name="random_recommend"),
]
