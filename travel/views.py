from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import TravelStyle, UserTravelStyle, Destination
from .serializers import TravelStyleSerializer, UserTravelStyleSerializer, DestinationSerializer
from travel.utils.swagger_docs import travel_style_list_schema, user_travel_style_schema, destination_list_schema
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


@destination_list_schema
class DestinationListView(generics.ListAPIView):
    queryset = Destination.objects.prefetch_related('travel_styles').all()
    serializer_class = DestinationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['travel_styles', 'province']
    search_fields = ['name', 'province']
    ordering_fields = ['name','proximate_nature', 'thrill_activities', 'cultural_sites', 'spa_facilities' ]
    ordering = ['name']
    # permission_classes = [permissions.IsAuthenticated]
    # pagination_class = pagination.StandardResultsSetPagination