from django.urls import path
from travel.views import TravelStyleListView, UserTravelStyleView

urlpatterns = [
    path('travel-styles/', TravelStyleListView.as_view(), name='travel-style-list'),
    path('my-travel-style/', UserTravelStyleView.as_view(), name='user-travel-style'),
]
