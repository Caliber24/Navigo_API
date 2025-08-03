from django.urls import path
from travel.views import TravelStyleListView, UserTravelStyleView, RecommendationView, ActivityListView, DestinationListView, AIRecommenderView 

urlpatterns = [
    path('travel-styles/', TravelStyleListView.as_view(), name='travel-style-list'),
    path('my-travel-style/', UserTravelStyleView.as_view(), name='user-travel-style'),
    path('recommendations/', RecommendationView.as_view(), name='recommendations'),
    path('activities/', ActivityListView.as_view(), name='activity-list'),
    path('destinations/', DestinationListView.as_view(), name='destination-list'),
    path('ai_refine/', AIRecommenderView.as_view(), name='ai-itinerary-refine'),
]
