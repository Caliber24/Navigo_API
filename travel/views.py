from rest_framework import generics, permissions
from .models import TravelStyle, UserTravelStyle
from .serializers import TravelStyleSerializer, UserTravelStyleSerializer
from travel.utils.swagger_docs import travel_style_list_schema, user_travel_style_schema

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
