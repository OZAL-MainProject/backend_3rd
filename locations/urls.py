from django.urls import path
from .views import RandomTravelRecommendation, LocationCreateView

urlpatterns = [
    path("recommend/", RandomTravelRecommendation.as_view(), name="random_recommend"),
    path("map/", LocationCreateView.as_view(), name="location-create"),
]
