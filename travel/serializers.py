from rest_framework import serializers
from .models import TravelStyle, UserTravelStyle

class TravelStyleSerializer(serializers.ModelSerializer):

    class Meta:
        model = TravelStyle
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class UserTravelStyleSerializer(serializers.ModelSerializer):
    travel_style = serializers.PrimaryKeyRelatedField(queryset=TravelStyle.objects.all())

    class Meta:
        model = UserTravelStyle
        fields = ['styles']
