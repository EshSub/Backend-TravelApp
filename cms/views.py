from rest_framework import viewsets
from .models import (
    Profile,
    EmailConfirmation,
    District,
    Province,
    Place,
    Activity,
    PlaceActivity,
    Type,
    Tag,
)
from .serializers import (
    ProfileSerializer,
    EmailConfirmationSerializer,
    DistrictSerializer,
    ProvinceSerializer,
    PlaceSerializer,
    ActivitySerializer,
    PlaceActivitySerializer,
    TypeSerializer,
    TagSerializer,
)
from math import radians, sin, cos, sqrt, atan2
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from django.core.mail import send_mail


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class EmailConfirmationViewSet(viewsets.ModelViewSet):
    queryset = EmailConfirmation.objects.all()
    serializer_class = EmailConfirmationSerializer

    @action(detail=False, methods=["get"])
    def test_email(self, request):
        res = (
            send_mail(
                "Test email",
                "This is a test email",
                "touracross@gmail.com",
                ["eshans2000@gmail.com"]
            ),
        )
        return Response({"message": res})


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filterset_fields = ["district", "activities"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["get"])
    def nearby_accommodations(self, request, pk=None):
        place = self.get_object()
        if not place.latitude or not place.longitude:
            return Response(
                {
                    "error": "Place does not have valid latitude and longitude coordinates."
                },
                status=400,
            )

        nearby_places = Place.objects.filter(types__name="Hotel")
        nearby_accommodations = []
        for nearby_place in nearby_places:
            if nearby_place.latitude and nearby_place.longitude:
                distance = self.calculate_distance(
                    place.latitude,
                    place.longitude,
                    nearby_place.latitude,
                    nearby_place.longitude,
                )
                if distance < 10:  # distance in kilometers
                    nearby_accommodations.append(
                        {
                            "place_id": nearby_place.place_id,
                            "place_name": nearby_place.place_name,
                            "description": nearby_place.description,
                            "distance_km": round(distance, 2),
                        }
                    )

        return Response(nearby_accommodations)

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        # Haversine formula to calculate distance between two lat/lon points
        R = 6371  # Radius of the earth in km
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) * sin(dlat / 2) + cos(radians(lat1)) * cos(
            radians(lat2)
        ) * sin(dlon / 2) * sin(dlon / 2)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c  # Distance in km
        return distance


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["places"]
    ordering_fields = [
        "activity_id",
        "activity_name",
        "place_activities",
        "places",
    ]  # Specify the fields that can be used for ordering
    ordering = ["activity_id"]  # Specify the default ordering
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PlaceActivityViewSet(viewsets.ModelViewSet):
    queryset = PlaceActivity.objects.all()
    serializer_class = PlaceActivitySerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
