from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']  # Customize fields as needed




class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims, if needed
        # token['user_info'] = UserSerializer(user).data  # Optional: Add serialized user to the token payload

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add the serialized user data to the response
        data['user'] = UserSerializer(self.user).data

        return data