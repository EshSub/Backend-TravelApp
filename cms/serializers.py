
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, EmailConfirmation, District, Province, Place, Activity, PlaceActivity, Type, Tag, Plan
from math import radians, sin, cos, sqrt, atan2

class UserSerializer(serializers.ModelSerializer):

    is_verified = serializers.SerializerMethodField()

    class Meta :
        model = User
        fields = ["id", "username", "password", "email", "first_name", "last_name", "is_verified"]

        def get_is_verified(self, obj):
            return obj.profile.is_verified
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta :
        model = Profile
        fields = '__all__'

class EmailConfirmationSerializer(serializers.ModelSerializer):
    class Meta : 
        model = EmailConfirmation
        fields = ["id", "user", "code", "created_at", "updated_at"]

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'
class PlaceSerializer(serializers.ModelSerializer):

    district_name = serializers.SerializerMethodField()
    province_name = serializers.SerializerMethodField()
    activity_objects = serializers.SerializerMethodField()
    # accommodation_places_nearby = serializers.SerializerMethodField()
    class Meta:
        model = Place
        fields = '__all__'

    def get_district_name(self, obj):
        return obj.district.name
    def get_province_name(self, obj):
        return obj.province.name
    def get_activity_objects(self, obj):
        return obj.activities.values("activity_id", "activity_name", "description")

    
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

    

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class PlaceActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceActivity
        fields = '__all__'


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'