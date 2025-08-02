from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from travel.serializers import TravelStyleSerializer, UserTravelStyleSerializer, DestinationSerializer, ActivitySerializer

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


recommendation_schema = extend_schema(
    summary="Get destination recommendations",
    description="Returns a list of suggested destinations with score and reasoning, based on the user's travel styles.",
    responses={200: DestinationSerializer(many=True)}
)

destination_list_schema = extend_schema(summary="List all destinations", responses={
    200: DestinationSerializer(many=True)})

activity_list_schema = extend_schema(summary="List all activities", responses={
    200: ActivitySerializer(many=True)})

aii_service_schema = extend_schema(
    summary="Refine raw itinerary with AI",
    description="Accepts raw itinerary text and refines it with AI in Persian based on user travel styles.",
    request={"application/json": {"type": "object", "properties": {
        "destination": {"type": "string"},
        "raw_itinerary": {"type": "string"},
        "daily_budget": {"type": "number"}
    }}},
    responses={200: OpenApiResponse(description="Refined Persian itinerary")}
)
