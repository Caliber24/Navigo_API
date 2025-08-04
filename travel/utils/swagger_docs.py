from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from travel.serializers import TravelStyleSerializer, UserTravelStyleSerializer, DestinationSerializer

# Documentation for listing travel styles
travel_style_list_schema = extend_schema(
    summary="List available travel styles",
    description="Returns all available travel styles that users can choose from.",
    responses={200: TravelStyleSerializer(many=True)}
)

# Documentation for retrieving and updating user's travel style
user_travel_style_schema = extend_schema(
    summary="Retrieve or update user's selected travel style",
    description="Allows the authenticated user to view or update their selected travel style.",
    responses={
        200: UserTravelStyleSerializer,
        404: OpenApiResponse(description="User travel style not found")
    },
    request=UserTravelStyleSerializer
)

destination_list_schema = extend_schema(summary="List all destinations", responses={
    200: DestinationSerializer(many=True)})
