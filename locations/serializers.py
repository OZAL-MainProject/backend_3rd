from rest_framework import serializers
from .models import Location

class LocationSerializer(serializers.ModelSerializer):
    """장소 정보를 처리하는 Serializer"""
    class Meta:
        model = Location
        fields = ("id", "detail_address", "address", "latitude", "longitude")
