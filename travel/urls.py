from django.urls import path
from travel.views import TravelStyleListView, UserTravelStyleView, DestinationListView

urlpatterns = [
    path('travel-styles/', TravelStyleListView.as_view(), name='travel-style-list'),
    path('my-travel-style/', UserTravelStyleView.as_view(), name='user-travel-style'),
    path('destinations/', DestinationListView.as_view(), name='destination-list')
]
