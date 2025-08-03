from rest_framework import serializers
from .models import TravelStyle, UserTravelStyle, Destination, Activity


class TravelStyleSerializer(serializers.ModelSerializer):

    class Meta:
        model = TravelStyle
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class UserTravelStyleSerializer(serializers.ModelSerializer):
    travel_style = TravelStyleSerializer(many=True, read_only=True)
    travel_style_id = serializers.PrimaryKeyRelatedField(
        many=True, queryset=TravelStyle.objects.all(), source='travel_style', write_only=True
    )

    class Meta:
        model = UserTravelStyle
        fields = ['id', 'user', 'travel_style', 'travel_style_id']
        read_only_fields = ['id', 'user', 'travel_style']


class DestinationSerializer(serializers.ModelSerializer):
    score = serializers.FloatField(
        read_only=True, help_text="Calculated score based on user's travel style preferences")
    reason = serializers.CharField(
        read_only=True, help_text="Reason for the score, e.g., 'High nature proximity'")

    class Meta:
        model = Destination
        fields = ['id', 'name', 'proximate_nature', 'thrill_activities',
                  'average_cost', 'cultural_sites', 'spa_facilities', 'score', 'reason']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"
