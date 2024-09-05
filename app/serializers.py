from django.contrib.auth.models import User

from django.forms import model_to_dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from cms.models import Profile

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
        data['user'] = model_to_dict(self.user, fields=['id', 'username', 'email', 'first_name', 'last_name'])

        try:
            profile = Profile.objects.get(user=self.user)
            data['profile'] = model_to_dict(profile)
        except Profile.DoesNotExist:
            data['profile'] = None
            
        return data