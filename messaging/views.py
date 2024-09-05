from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from datetime import datetime
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from gemini.gemini import *
from django.forms.models import model_to_dict
from cms.models import Place

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        # add user to request data
        request.data['user'] = user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)            
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(user=user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filterset_fields = ["conversation"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # message = serializer.validated_data
        # Save the new message
        message = serializer.save()
        
        # Get the conversation ID from the newly created message
        conversation_id = serializer.validated_data['conversation'].id  # Corrected field reference
        current_message = serializer.validated_data['message']

        place_id = request.data.get('place_id', None)
        # print("place_id", place_id)

        messages = Message.objects.filter(conversation_id=conversation_id).order_by('-date', '-time')[:5]
        # message_history = messages.values('message')
        message_history = self.create_conversation_json(messages)

        conversation = Conversation.objects.get(id=conversation_id)  # Corrected field reference
        # print("conversation", conversation)
        if(place_id):
            place = Place.objects.get(place_id=place_id)
            # print("place", place)
            ai_response = chat_ai_response1(message_history, place)

        else:
            ai_response = chat_ai_response1(message_history, None)
        # print("ai_response", ai_response)

        res_message = Message.objects.create(
            conversation_id=conversation.id,  # Corrected field reference  
            date=datetime.now().date(),  # Current date
            time=datetime.now().time(),  # Current time
            message=ai_response,
            guide_id=1
        )

        return Response({"res_message": MessageSerializer(res_message).data, 'message': MessageSerializer(message).data}, status=status.HTTP_201_CREATED)

    def create_conversation_json(self, messages):
        conversation_history = []
        for message in messages:
            conversation_history.append({
                'message': message.message,
            })
        return conversation_history
    
    def get_response_AI(self, conversation_id, current_message):
        # Placeholder function for AI response
        return "This is an AI generated response"
