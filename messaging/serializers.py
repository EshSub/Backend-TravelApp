from rest_framework import serializers
from .models import Conversation, Message
from cms.models import Place
from django.contrib.auth.models import User

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'user_id', 'isAI']

class MessageSerializer(serializers.ModelSerializer):
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())
    place_id = serializers.PrimaryKeyRelatedField(queryset=Place.objects.all(), allow_null=True, required=False)
    guide_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Message
        fields = ['date', 'time', 'conversation', 'message', 'place_id', 'guide_id']
