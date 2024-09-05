from rest_framework import serializers
from .models import Conversation, Message
from cms.models import Place
from django.contrib.auth.models import User
from django.forms.models import model_to_dict


class ConversationSerializer(serializers.ModelSerializer):

    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = "__all__"

    def get_last_message(self, obj):
        last_message = obj.message_set.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None


class MessageSerializer(serializers.ModelSerializer):
    conversation = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all()
    )
    # place_id = serializers.PrimaryKeyRelatedField(queryset=Place.objects.all(), allow_null=True, required=False)
    # guide_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Message
        fields = "__all__"
