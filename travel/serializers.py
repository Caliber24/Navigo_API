from rest_framework import serializers
from .models import TravelStyle, UserTravelStyle, Destination


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

    class Meta:
        model = Destination
        fields = '__all__'


# class RecommendationRequestSerializer(serializers.Serializer):
#     origin = serializers.CharField()
#     travel_style = serializers.CharField(required=False)
#     travel_days = serializers.IntegerField(required=False)
#     transport_mode = serializers.CharField(
#         required=False, choices=['car', 'bus', 'train', 'flight'])

#     weather_type = serializers.ChoiceField(choices=['hot', 'cold', 'moderate', 'dry', 'humid'], required=False)
#     budget_level = serializers.CharField(required=False)
#     tags = serializers.ListField(child=serializers.CharField(), required=False)
