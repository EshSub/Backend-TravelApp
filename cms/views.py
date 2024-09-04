from rest_framework import viewsets
from .models import Profile, EmailConfirmation, District, Province, Place, Activity, PlaceActivity, Type, Tag, Plan
from .serializers import ProfileSerializer, EmailConfirmationSerializer, DistrictSerializer, ProvinceSerializer, PlaceSerializer, ActivitySerializer, PlaceActivitySerializer, TypeSerializer, TagSerializer, PlanSerializer
from math import radians, sin, cos, sqrt, atan2
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from django.core.mail import send_mail


from gemini.gemini import get_plan
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework import status

from django.db.models import Q



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
    
    @action(detail=False, methods=["get"])
    def get_places(self, request, pk=None):
    
        json_input = request.query_params
        SampleInput = {
            "type": "destination",
            "time": "morning",
            "district": "Galle",
            "activities": "Wildlife Safari",
            "props": {
                "type": "adventure",
                "price": "medium"
                }
            }
        
        place_type = json_input.get("type")
        district = json_input.get("district")
        # activities = json_input.get("activities")
        # activity_type = json_input.get("props", {}).get("type")
        # price = json_input.get("price")

        # Construct the query based on the input fields
        query = Q()

        if place_type:
            query &= Q(types__name__icontains=place_type)

        # if activities:
        #     query &= Q(activities__activity_name__icontains=activities)

        # if activity_type:
        #     query &= Q(types__name__icontains=activity_type)

        # if price:
        #     if price == "low":
        #         query &= Q(ticket_price__lt=10)  #  threshold for 'low' price
        #     elif price == "medium":
        #         query &= Q(ticket_price__gte=10, ticket_price__lt=50)  #  threshold for 'medium' price
        #     elif price == "high":
        #         query &= Q(ticket_price__gte=50)  #  threshold for 'high' price

        if district:
            query &= Q(district__name__icontains=district)

        # Filter the places based on the constructed query
        filtered_places = Place.objects.filter(query).distinct()

        # Serialize the result
        serialized_places = PlaceSerializer(filtered_places, many=True)

        # Return the filtered places
        return Response(serialized_places.data)
       
        

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

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    def create(self, request):
        user = request.user
        request_data = request.data

        input_data = {
            "duration": request_data.get("duration", 2),
            "preferred_activities": request_data.get("preferred_activities", ["diving", "snorkelling", "kayaking", "sea bathing", "hiking"]),	
            "description": request_data.get("description", "I want to do some water activities around downsouth area")	
        }
        
        # Extract data from request with default values
        days = input_data.get("duration")
        activities = input_data.get("preferred_activities")
        description = input_data.get("description")
        
        # Call your custom function to get the plan
        created_plan, message = get_plan(days, activities, description)
        
        # Prepare data for the serializer
        plan_data = {
            "user": user.id,
            "Input_data": input_data,
            "created_plan": created_plan
        }
        
        # Create a serializer instance with data to validate and save the plan
        serializer = self.get_serializer(data=plan_data)
        if serializer.is_valid():
            serializer.save()  # Save the validated data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If the serializer is not valid, return the errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


