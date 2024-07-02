
from rest_framework import serializers
from django.contrib.auth.models import User
from cms.models import EmailConfirmation, Profile

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

    