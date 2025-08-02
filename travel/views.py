from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import TravelStyle, UserTravelStyle, Destination, Activity
from .serializers import TravelStyleSerializer, UserTravelStyleSerializer, DestinationSerializer, ActivitySerializer
from .recommendation import recommend_destinations
from .ai_service import AIRecommender
from travel.utils.swagger_docs import travel_style_list_schema, user_travel_style_schema, recommendation_schema, destination_list_schema, activity_list_schema, aii_service_schema
from .utils import pagination



class TravelStyleListView(generics.ListAPIView):
    queryset = TravelStyle.objects.all()
    serializer_class = TravelStyleSerializer
    permission_classes = [permissions.AllowAny]

    @travel_style_list_schema
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserTravelStyleView(generics.RetrieveUpdateAPIView):
    serializer_class = UserTravelStyleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj, _ = UserTravelStyle.objects.get_or_create(user=self.request.user)
        return obj

    @user_travel_style_schema
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @user_travel_style_schema
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

@recommendation_schema
class RecommendationView(generics.ListAPIView):
    serializer_class = DestinationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.StandardResultsSetPagination

    def get_queryset(self):
        min_cost = self.request.query_params.get('min_cost', 0)
        max_cost = self.request.query_params.get('max_cost', float('inf'))
        preferred_activity = self.request.query_params.getlist('activity', [])
        recommendations = recommend_destinations(self.request.user)
        if min_cost :
            recommendations = [dest for dest in recommendations if dest.average_cost >= float(min_cost)]
        if max_cost:
            recommendations = [dest for dest in recommendations if dest.average_cost <= float(max_cost)]
        if preferred_activity:
            recommendations = [dest for dest in recommendations if preferred_activity.lower() in dest.reason.lower()]
        
        return recommendations
        
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@destination_list_schema
class DestinationListView(generics.ListAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [permissions.IsAuthenticated]

@activity_list_schema
class ActivityListView(generics.ListAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]


@aii_service_schema
class AIRecommenderView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        destination = request.data.get('destination')
        raw_itinerary = request.data.get('rae_itinerary')
        daily_budget = request.data.get('daily_budget')
        styles_qs = request.user.styles.travel_style.all().only('name')
        styles = ', '.join([style.name for style in styles_qs])
        result = AIRecommender.refine_itinerary(destination, raw_itinerary, styles,daily_budget)
        return Response({"refined_itinerary": result}, status=status.HTTP_200_OK)