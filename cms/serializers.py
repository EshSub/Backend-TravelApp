
from rest_framework import serializers
from django.contrib.auth.models import User
from cms.models import EmailConfirmation

class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ["id", "username", "password", "email", "first_name", "last_name"]

class EmailConfirmationSerializer(serializers.ModelSerializer):
    class Meta : 
        model = EmailConfirmation
        fields = ["id", "user", "code", "created_at", "updated_at"]

    